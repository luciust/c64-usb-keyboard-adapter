# Voltage Level Shifting, Matrix Interfacing, and Debounce Research

This document details the engineering research, electrical analysis, and comparative design decisions for interfacing the Commodore 64 (C64) mainboard keyboard connector (**CN8**) with the **Raspberry Pi Pico 2 (RP2350)** versus the original **Raspberry Pi Pico (RP2040)**.

---

## 1. C64 Keyboard Interface (CN8) Electrical Characteristics

* **Operating Voltage:** +5.0V DC ± 5%
* **Motherboard Connector (CN8):** 20-pin single row 2.54mm pitch header
  * **Pin 1:** GND
  * **Pin 2:** KEY (cut pin for polarization)
  * **Pin 3:** `/RESTORE` (Active-low NMI line, pulled high to +5V)
  * **Pin 4:** `+5V DC` (Supplies ~150-200mA)
  * **Pins 5–12:** Rows `PB3, PB6, PB5, PB4, PB7, PB2, PB1, PB0` (CIA 1 Port B, pulled to +5V by resistor pack RP2)
  * **Pins 13–20:** Columns `PA7, PA6, PA5, PA4, PA3, PA2, PA1, PA0` (CIA 1 Port A, driven active-low)
* **NMOS CIA 6526 Signal Levels:**
  * Low input voltage ($V_{IL}$ max): **0.8 V** (lines must pull below 0.8V to register LOW).
  * High input voltage ($V_{IH}$ min): **2.0 V to 2.4 V** (standard TTL thresholds).
  * High output voltage ($V_{OH}$): **3.8 V to 4.2 V** from the NMOS output stage, pulled up to **5.0 V** by motherboard resistor pack RP2.

---

## 2. Microcontroller Comparison: RP2040 vs. RP2350 (Pico 2)

| Parameter | Raspberry Pi Pico (RP2040) | Raspberry Pi Pico 2 (RP2350) |
|:---|:---|:---|
| **Digital GPIO Voltage Rating** | **3.3V Max** ($V_{DDIO} + 0.5\text{V} \approx 3.8\text{V}$ absolute max) | **Officially 5V-Tolerant** (when $IOVDD = 3.3\text{V}$) |
| **5V Input Tolerance** | ❌ **No.** Direct 5V causes ESD diode forward-bias & latch-up |  **Yes.** Directly accepts 4V-5V logic levels |
| **Open-Drain with 5V Pull-up**| ❌ **No.** Pin cannot sit at 5V in High-Z |  **Yes.** Pin safely sits at 5V in High-Z |
| **Column Level Shifting** | Required 16x Resistors (8 voltage dividers) | **Direct Connection (Zero Resistors!)** |
| **Row Level Shifting** | Required 74HCT245 + 8x Schottky Diodes | **Native Open-Drain (Zero Transceivers!)** |
| **RESTORE Key Buffer** | Required 2N7000 MOSFET + Resistor | **Direct Connection (Native Open-Drain)** |
| **Total Component Count** | **~33 components + Pico** | **2–3 passive parts + Pico 2** |

---

## 3. RP2350 5V-Tolerance Electrical Verification

### 3.1 Digital vs. Analog Pins
* Digital GPIO pins (GP0–GP22) on the RP2350 feature redesigned I/O pad structures with high-voltage tolerance.
* ADC pins (GP26–GP28) are **not** 5V tolerant. Because the keyboard adapter matrix uses only GP0–GP16, no analog pins are exposed to 5V.

### 3.2 Power Sequencing Analysis
* **Rule:** $IOVDD$ (3.3V) must be active whenever external 5V voltages are applied to GPIO pads.
* **C64 Implementation:**
  1. CN8 Pin 4 (+5V) feeds Pico 2 `VBUS` (Pin 40).
  2. When the C64 power switch is toggled ON, +5V powers the Pico 2 regulator, establishing $IOVDD = 3.3\text{V}$ in $< 100\text{ }\mu\text{s}$.
  3. The C64's onboard 556 timer holds the 6510 CPU and CIA 6526 chips in hardware RESET for $\sim 500\text{ ms}$.
  4. The Pico 2 is therefore fully powered and ready **hundreds of milliseconds** before any C64 matrix activity begins.
  5. On power-down, the C64 5V rail collapses simultaneously across both the Pico 2 and the CIA chips.
  6. The power sequencing constraint is **fully satisfied** by design.

---

## 4. Native Open-Drain & Joystick 1 Protection

### 4.1 The Joystick Contention Problem
On the Commodore 64, **Control Port 1 (Joystick 1)** is wired in parallel with keyboard rows PB0–PB4:
* Up: PB0
* Down: PB1
* Left: PB2
* Right: PB3
* Fire: PB4

If a microcontroller actively drives a row HIGH (to 3.3V or 5V) while the user presses the joystick to GND, a direct short circuit occurs.

### 4.2 Native Open-Drain Solution on Pico 2
The Pico 2 implements true open-drain in hardware without external ICs:
* The GPIO output data register (`sio_hw->gpio_out`) is initialized to `0` (GND) on all row pins (GP8–GP15).
* **When Key is Pressed:** The GPIO Output Enable bit (`sio_hw->gpio_oe`) is set to `1`. The pin actively drives 0.0V (sinking current to GND). $V_{OL} \approx 0.05\text{V}$, well below C64 $V_{IL\text{ max}} = 0.8\text{V}$.
* **When Key is Released:** The GPIO Output Enable bit is set to `0`. The pin transitions to High-Z (input). The C64 motherboard resistor pack RP2 pulls the line up to +5V. Since the RP2350 is 5V-tolerant, it sits safely at 5V.
* **When Joystick is Pressed:** The row line is grounded by the joystick switch. Since the Pico 2 is either already driving 0V or sitting in high-impedance input mode, **zero contention current can ever flow**.
* **Optional Safety Resistors:** 8x $100\Omega$ series resistors are included between GP8-GP15 and CN8 PB0-PB7 as extra hardware hardening against accidental software misconfigurations.

---

## 5. Keyboard Debounce & KERNAL Pacing

* **USB HID Filtering:** Modern USB keyboards perform mechanical contact debouncing in their own internal controller and only emit verified state changes.
* **C64 KERNAL Timing ($EA87):** The C64 KERNAL scans the keyboard matrix during the 50Hz/60Hz vertical interrupt routine ($EA87) every 16.6ms / 20ms. The KERNAL requires consecutive identical readings before placing a character into the keyboard FIFO buffer (`$0277-$0280`).
* **Contact Pacing:** To guarantee that quick key taps (< 15ms) are never dropped by the C64 KERNAL, the Pico 2 firmware enforces a **Minimum Contact Hold Time of 35 ms** (`C64_MIN_HOLD_TIME_US = 35000`).
