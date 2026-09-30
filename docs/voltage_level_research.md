# Voltage Level Shifting, Matrix Interfacing, and Debounce Research

This document details the engineering research and design decisions for interfacing a modern 3.3V Raspberry Pi Pico (RP2040) with the vintage 5V NMOS architecture of the Commodore 64 (C64) mainboard keyboard connector.

---

## 1. Electrical Architecture: C64 CIA 6526 vs. RP2040

### 1.1 Commodore 64 Keyboard Interface (CN8)
The C64 motherboard connects to the internal keyboard via connector **CN8** (20-pin single row header, 2.54mm pitch):
* **Pin 1:** GND
* **Pin 2:** Key (cut pin for physical polarization)
* **Pin 3:** `/RESTORE` (Active-low, connects to NMI generation circuit / 556 timer)
* **Pin 4:** `+5V DC` (powers keyboard LED, max safe draw ~150-200mA)
* **Pins 5-12:** Rows `PB3, PB6, PB5, PB4, PB7, PB2, PB1, PB0` (CIA 1 Port B)
* **Pins 13-20:** Columns `PA7, PA6, PA5, PA4, PA3, PA2, PA1, PA0` (CIA 1 Port A)

### 1.2 NMOS 6526 / 8520 Signal Characteristics
* **Supply Voltage:** 5.0V ± 5%
* **Input Thresholds:**
  * Low input voltage ($V_{IL}$ max): **0.8 V** (a line must be pulled below 0.8V to register as logic 0).
  * High input voltage ($V_{IH}$ min): **2.0 V** to **2.4 V** (TTL compatibility).
* **Output Levels:**
  * Low output voltage ($V_{OL}$ max): **0.4 V** (sinks ~1.6mA - 3.2mA).
  * High output voltage ($V_{OH}$ min): Nominally **3.8 V to 4.2 V** from the NMOS output stage (typically around **4.0V** when unloaded). When pulled up to +5V via resistor pack RP2 (3.3kΩ / 4.7kΩ), it reaches **5.0 V**.

### 1.3 Raspberry Pi Pico (RP2040) Constraints
* **Operating Logic Level:** 3.3V ($V_{DDIO} = 3.3\text{ V}$)
* **Input Voltage Absolute Maximum:** $V_{DDIO} + 0.5\text{ V} \approx 3.8\text{ V}$ (3.63V recommended maximum operating limit).
* **Danger:** The RP2040 GPIO pins are **NOT 5V tolerant**. Applying 4.0V to 5.0V directly to any Pico GPIO will forward-bias the on-chip ESD protection diodes, leaking current into the 3.3V rail. Over time or under low impedance, this causes permanent gate oxide damage, excessive current draw, or CMOS latch-up.

---

## 2. Research: The "Translating 4V to 3.3V" Challenge (Columns: C64 → Pico)

In standard operation, the C64 CIA 1 Port A drives the columns. To scan, the C64 pulls one column at a time LOW (0V). The unselected columns output between 3.8V and 5.0V (nominally ~4V).

### 2.1 Evaluation of 74xx245 Transceivers for 4V/5V → 3.3V
* **74HCT245 (at 5V VCC):** Accepts 4V TTL inputs reliably, but outputs full 5V logic. Feeding 5V outputs into Pico GPIOs requires another stage of level translation. If powered at 3.3V, 74HCT is out of specification (minimum VCC is 4.5V).
* **74HC245 (at 3.3V VCC):** Standard HC logic powered at 3.3V does **not** have 5V-tolerant inputs. Its internal clamp diodes to VCC would clamp the 4V-5V inputs to ~3.8V, sinking current into the Pico's 3.3V supply rail.
* **74LVC245 (at 3.3V VCC):** Features true 5V-tolerant inputs when powered at 3.3V, making it ideal electronically. However, the LVC logic family is manufactured **almost exclusively in SMD packages** (SOIC, TSSOP), violating the requirement for **DIP and THT only**.
* **74LS245 (at 5V VCC):** Bipolar TTL outputs typically clamp high at $V_{CC} - 2 V_{be} \approx 3.4\text{ V}$. However, with a high-impedance CMOS load (Pico GPIO), leakage can allow the voltage to drift higher (up to 3.8V-4.0V), which is unsafe.

### 2.2 The Selected DIP/THT Solution: Passive Resistor Dividers
A precision passive voltage divider per column line provides the cleanest, fastest, and most reliable DIP/THT solution:
* **Topology:**
  $$\text{C64 Column Pin} \longrightarrow R_{\text{series}} (1.8\text{ k}\Omega) \longrightarrow \text{Pico GPIO} \longrightarrow R_{\text{pull-down}} (3.3\text{ k}\Omega) \longrightarrow \text{GND}$$
* **Divider Ratio:**
  $$K = \frac{3.3\text{ k}\Omega}{1.8\text{ k}\Omega + 3.3\text{ k}\Omega} = \frac{3.3}{5.1} \approx 0.647$$
* **Voltage Translation:**
  * When C64 outputs $5.0\text{ V}$: $V_{\text{Pico}} = 5.0 \times 0.647 = \mathbf{3.235\text{ V}}$ (Safe! Exactly matches 3.3V rail).
  * When C64 NMOS outputs $4.0\text{ V}$: $V_{\text{Pico}} = 4.0 \times 0.647 = \mathbf{2.588\text{ V}}$ (Safe! Substantially above RP2040 $V_{IH\text{ min}} = 2.0\text{ V}$).
  * When C64 outputs $0.4\text{ V}$ (LOW): $V_{\text{Pico}} = 0.4 \times 0.647 = \mathbf{0.259\text{ V}}$ (Safe! Well below RP2040 $V_{IL\text{ max}} = 0.8\text{ V}$).
* **Frequency Response & Latency:**
  The RP2040 pin input capacitance is $\approx 5\text{ pF}$.
  $$R_{\text{thevenin}} = 1.8\text{ k}\Omega \parallel 3.3\text{ k}\Omega = 1.16\text{ k}\Omega$$
  $$\tau = R_{\text{thevenin}} \times C = 1.16\text{ k}\Omega \times 5\text{ pF} \approx \mathbf{5.8\text{ ns}}$$
  A time constant of 5.8 ns is **600 times faster** than the C64 bus cycle ($1000\text{ ns}$), introducing negligible propagation delay.
* **Component Form Factor:** Standard 1/4W axial THT resistors, or two 9-pin SIP resistor network packages.

---

## 3. Research: 3.3V to 5V Open-Drain Emulation (Rows: Pico → C64)

The C64 rows (PB0-PB7) are pulled up to +5V on the motherboard. When a key is pressed, that row line must be pulled LOW to GND.

### 3.1 The Joystick Conflict Hazard
On the C64, **Control Port 1 (Joystick 1)** is wired directly in parallel with keyboard row lines PB0-PB4:
* Up: PB0
* Down: PB1
* Left: PB2
* Right: PB3
* Fire: PB4

If an active push-pull logic buffer drives a row line HIGH (5.0V), and the player pushes Joystick 1 or presses the fire button, the joystick switch **shorts the line directly to GND**. A push-pull driver would suffer a direct short-circuit ($5\text{V} \rightarrow \text{GND}$ through the driver's output transistor), drawing >60mA, damaging the driver chip, and corrupting the C64 power rail!

### 3.2 Solution: 74HCT245 + Schottky Diode Open-Drain Emulation
To safely emulate passive mechanical switches and prevent bus contention:
1. **74HCT245 in DIP-20:**
   * Powered from the C64’s `+5V` rail.
   * Inputs (A1-A8) connect to Pico GPIOs (GP8-GP15).
   * 74HCT logic has TTL input thresholds ($V_{IH\text{ min}} = 2.0\text{ V}$). The Pico’s 3.3V logic high ($V_{OH} \ge 3.0\text{ V}$) drives it with over $1.0\text{ V}$ of noise margin.
   * Outputs (B1-B8) swing rail-to-rail from 0.1V to 5.0V.
2. **8x Schottky Diodes (BAT42, BAT43, BAT85, or 1N5819 in DO-35 axial THT):**
   * **Cathode:** Connected to 74HCT245 output pin.
   * **Anode:** Connected to C64 Row pin (PB0-PB7).
3. **Operating States:**
   * **Key Pressed (Pico outputs 0V):**
     * 74HCT245 outputs $0.1\text{ V}$.
     * Diode conducts current from C64 pull-up resistor.
     * C64 Row voltage: $V_{\text{Row}} = V_{OL} + V_F \approx 0.1\text{ V} + 0.25\text{ V} = \mathbf{0.35\text{ V}}$.
     * Since $0.35\text{ V} < V_{IL\text{ max}} (0.8\text{ V})$, the C64 detects a valid logic LOW.
   * **Key Released (Pico outputs 3.3V):**
     * 74HCT245 outputs $5.0\text{ V}$.
     * Both Anode and Cathode are at 5.0V. Diode is reverse-biased / OFF.
     * The row line is high-impedance (floats high to 5V via C64 internal pull-up).
   * **Joystick Pressed while Key Inactive:**
     * Anode is grounded by joystick switch ($0\text{ V}$).
     * Cathode is at $5.0\text{ V}$ (74HCT245 output).
     * Diode is strongly reverse-biased (blocking 5V). Zero reverse current flows! No contention, no damage!

---

## 4. Research: Keyboard De-bounce & Contact Pacing

### 4.1 Mechanical vs. Digital Debouncing
* **Mechanical Contacts:** Physical C64 keys bounce mechanically for 5 to 20 ms.
* **USB Keyboards:** Modern USB keyboards have an internal microcontroller scanning keys at 500-1000 Hz. They perform hardware/firmware debouncing internally and transmit only verified state changes via USB HID interrupt packets.
* **Transceiver Debouncing:** A 74245 transceiver is purely combinational logic; it does not perform temporal debouncing or glitch suppression.

### 4.2 Why Debounce/Pacing is Required for the C64 KERNAL
The C64 KERNAL ROM scans the keyboard during the vertical blank interrupt at 60 Hz (NTSC) or 50 Hz (PAL), once every **16.6 ms or 20 ms** ($EA87 routine).
* The KERNAL implements a software filter: a key must be detected across consecutive scans before it is accepted into the 10-byte FIFO keyboard buffer (`$0277-$0280`).
* If a modern USB keyboard sends a rapid keypress and release (e.g., a quick tap < 15ms or a scripted macro), the C64 KERNAL might sample the matrix while the key is already released, completely missing the keystroke!
* **Firmware Hold-Time Pacing:**
  The Pico firmware enforces a **Minimum Contact Hold Time** of **35 ms** (`C64_MIN_HOLD_TIME_US = 35000`).
  When a key is pressed, it is held active on the emulated matrix for at least 35 ms (spanning at least two C64 vertical blank scan frames) before the release is committed. This guarantees 100% key registration accuracy at any typing speed.

---

## 5. Dual-Core RP2040 Real-Time Architecture

The C64 6510 CPU runs at ~1 MHz. The time between CIA Port A column selection (`STA $DC00`) and Port B row reading (`LDA $DC01`) is approximately **3.5 to 4 microseconds** ($3500\text{ - }4000\text{ ns}$).

To ensure deterministic, zero-latency response regardless of USB host processing load:
* **Core 0:** Runs TinyUSB Host stack (`tuh_task()`), HID report parsing, wireless combo interface handling, and key hold-time management.
* **Core 1:** Runs an uninhibited, dedicated real-time matrix loop:
  * Directly polls column input register `sio_hw->gpio_in`.
  * Computes active row outputs in under **15 CPU cycles** (< 120 ns at 125 MHz).
  * Writes to `sio_hw->gpio_out`.
  * Total response latency is **under 50 ns**, more than **70 times faster** than the C64 CPU read cycle!
