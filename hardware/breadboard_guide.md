# Breadboard Prototyping & Testing Guide

This guide walks you through building and testing the **C64 USB Keyboard & Wireless Host Adapter** on a standard 830-point solderless breadboard before soldering the final PCB.

---

## 1. Breadboard Bill of Materials

| Item | Component | Package | Quantity | Description / Value |
|:---:|:---|:---:|:---:|:---|
| 1 | Raspberry Pi Pico | 40-pin DIP | 1 | RP2040 microcontroller board (with pin headers) |
| 2 | 74HCT245 | DIP-20 | 1 | Octal 3-state bus transceiver (High-speed CMOS, TTL-compatible) |
| 3 | BAT42 / BAT43 / BAT85 | DO-35 axial | 8 | Small-signal Schottky diodes ($V_F \approx 0.25\text{V}$) |
| 4 | Resistors 1.8 kΩ | Axial 1/4W | 8 | Resistor divider upper stage (5V/4V → 3.3V) |
| 5 | Resistors 3.3 kΩ | Axial 1/4W | 8 | Resistor divider lower stage (to GND) |
| 6 | 2N7000 | TO-92 | 1 | N-channel MOSFET (RESTORE key open-drain) |
| 7 | Ceramic Capacitor | Radial THT | 2 | 100 nF (0.1 µF) decoupling (74HCT245 and 3.3V rail) |
| 8 | Electrolytic Capacitor | Radial THT | 1 | 10 µF to 47 µF 16V (5V rail bulk filter) |
| 9 | USB OTG Cable | Cable | 1 | Micro-USB male to USB-A female adapter |
| 10 | Jumper Wire Ribbon | 20-pin | 1 | 2.54mm pitch female header cable to C64 CN8 connector |
| 11 | Solderless Breadboard | Standard | 1 | 830 tie-point breadboard |

---

## 2. Pinout Reference

### 2.1 Commodore 64 Motherboard Keyboard Connector (CN8)
The connector is a single-row 2.54mm pitch 20-pin header on the C64 mainboard:

```
[ 1] GND (Ground)
[ 2] KEY (Polarization pin - cut/missing pin)
[ 3] /RESTORE (Active-low NMI trigger)
[ 4] +5V DC (Power supply from C64)
[ 5] Row 3 (PB3)
[ 6] Row 6 (PB6)
[ 7] Row 5 (PB5)
[ 8] Row 4 (PB4)
[ 9] Row 7 (PB7)
[10] Row 2 (PB2)
[11] Row 1 (PB1)
[12] Row 0 (PB0)
[13] Col 7 (PA7)
[14] Col 6 (PA6)
[15] Col 5 (PA5)
[16] Col 4 (PA4)
[17] Col 3 (PA3)
[18] Col 2 (PA2)
[19] Col 1 (PA1)
[20] Col 0 (PA0)
```

---

### 2.2 74HCT245 Bus Transceiver (DIP-20)
```
          +---v---+
  DIR   1 |       | 20  VCC (+5V from C64 CN8 Pin 4)
  A1    2 |       | 19  /OE (Ground / Enable)
  A2    3 |       | 18  B1 (Row 0 Diode Cathode)
  A3    4 |       | 17  B2 (Row 1 Diode Cathode)
  A4    5 |       | 16  B3 (Row 2 Diode Cathode)
  A5    6 |       | 15  B4 (Row 3 Diode Cathode)
  A6    7 |       | 14  B5 (Row 4 Diode Cathode)
  A7    8 |       | 13  B6 (Row 5 Diode Cathode)
  A8    9 |       | 12  B7 (Row 6 Diode Cathode)
  GND  10 |       | 11  B8 (Row 7 Diode Cathode)
          +-------+
```

* **DIR (Pin 1):** Connect to `+5V` (transmit direction: A inputs → B outputs).
* **/OE (Pin 19):** Connect to `GND` (outputs always enabled).
* **VCC (Pin 20):** Connect to `+5V` (C64 CN8 Pin 4).
* **GND (Pin 10):** Connect to `GND`.
* **Decoupling:** Place a 100nF ceramic capacitor directly between Pin 20 and Pin 10.

---

## 3. Step-by-Step Breadboard Wiring

### Step 1: Power & Ground Rails
1. Connect breadboard **GND rail** to C64 CN8 Pin 1 (GND) and Pico Pin 38 / 3 (GND).
2. Connect breadboard **+5V rail** to C64 CN8 Pin 4 (+5V).
3. Connect C64 CN8 Pin 4 (+5V) to Raspberry Pi Pico **VBUS (Pin 40)**.
   * *Note:* Feeding 5V into VBUS powers the Pico's onboard buck-boost regulator (generating 3.3V) AND supplies 5V to the micro-USB connector to power your USB keyboard or wireless dongle.
4. Place the **10µF - 47µF electrolytic capacitor** across the +5V and GND power rails (observe polarity: negative stripe to GND).

---

### Step 2: 74HCT245 & Row Output Stage (Pico → C64)
1. Insert the **74HCT245** across the breadboard center trough.
2. Wire Pin 20 (VCC) to +5V rail.
3. Wire Pin 10 (GND) to GND rail.
4. Wire Pin 1 (DIR) to +5V rail (A → B direction).
5. Wire Pin 19 (/OE) to GND rail (always active).
6. Connect the 100nF ceramic capacitor between Pin 20 and Pin 10.
7. Connect Pico Row outputs (GP8 - GP15) to 74HCT245 A-side inputs:
   * **Pico Pin 11 (GP8)**  → 74HCT245 Pin 2 (A1)
   * **Pico Pin 12 (GP9)**  → 74HCT245 Pin 3 (A2)
   * **Pico Pin 14 (GP10)** → 74HCT245 Pin 4 (A3)
   * **Pico Pin 15 (GP11)** → 74HCT245 Pin 5 (A4)
   * **Pico Pin 16 (GP12)** → 74HCT245 Pin 6 (A5)
   * **Pico Pin 17 (GP13)** → 74HCT245 Pin 7 (A6)
   * **Pico Pin 19 (GP14)** → 74HCT245 Pin 8 (A7)
   * **Pico Pin 20 (GP15)** → 74HCT245 Pin 9 (A8)
8. Connect the 8x Schottky diodes (BAT42 / BAT43 / BAT85):
   * **D1:** Cathode (black band) to 74HCT245 Pin 18 (B1) → Anode to C64 CN8 Pin 12 (Row 0 / PB0)
   * **D2:** Cathode (black band) to 74HCT245 Pin 17 (B2) → Anode to C64 CN8 Pin 11 (Row 1 / PB1)
   * **D3:** Cathode (black band) to 74HCT245 Pin 16 (B3) → Anode to C64 CN8 Pin 10 (Row 2 / PB2)
   * **D4:** Cathode (black band) to 74HCT245 Pin 15 (B4) → Anode to C64 CN8 Pin 5  (Row 3 / PB3)
   * **D5:** Cathode (black band) to 74HCT245 Pin 14 (B5) → Anode to C64 CN8 Pin 8  (Row 4 / PB4)
   * **D6:** Cathode (black band) to 74HCT245 Pin 13 (B6) → Anode to C64 CN8 Pin 7  (Row 5 / PB5)
   * **D7:** Cathode (black band) to 74HCT245 Pin 12 (B7) → Anode to C64 CN8 Pin 6  (Row 6 / PB6)
   * **D8:** Cathode (black band) to 74HCT245 Pin 11 (B8) → Anode to C64 CN8 Pin 9  (Row 7 / PB7)

> **CRITICAL DIODE ORIENTATION:**
> The **Cathode** (marked with a black band on the glass DO-35 body) **MUST** point towards the 74HCT245!
> The **Anode** connects to the C64 CN8 pin.
> If inverted, the circuit will short the C64 rows to +5V when keys are released!

---

### Step 3: Column Voltage Dividers (C64 → Pico)
For each column line (PA0 - PA7), assemble a two-resistor divider ($1.8\text{ k}\Omega$ upper, $3.3\text{ k}\Omega$ lower):

| Column | C64 CN8 Pin | Series Resistor ($1.8\text{ k}\Omega$) | Junction Node (to Pico GPIO) | Pull-Down Resistor ($3.3\text{ k}\Omega$) |
|:---:|:---:|:---:|:---:|:---:|
| Col 0 (PA0) | Pin 20 | from CN8 Pin 20 | to **Pico Pin 1 (GP0)** | to GND rail |
| Col 1 (PA1) | Pin 19 | from CN8 Pin 19 | to **Pico Pin 2 (GP1)** | to GND rail |
| Col 2 (PA2) | Pin 18 | from CN8 Pin 18 | to **Pico Pin 4 (GP2)** | to GND rail |
| Col 3 (PA3) | Pin 17 | from CN8 Pin 17 | to **Pico Pin 5 (GP3)** | to GND rail |
| Col 4 (PA4) | Pin 16 | from CN8 Pin 16 | to **Pico Pin 6 (GP4)** | to GND rail |
| Col 5 (PA5) | Pin 15 | from CN8 Pin 15 | to **Pico Pin 7 (GP5)** | to GND rail |
| Col 6 (PA6) | Pin 14 | from CN8 Pin 14 | to **Pico Pin 9 (GP6)** | to GND rail |
| Col 7 (PA7) | Pin 13 | from CN8 Pin 13 | to **Pico Pin 10 (GP7)** | to GND rail |

---

### Step 4: RESTORE Key Circuit
1. Insert the **2N7000 N-channel MOSFET** (TO-92 package, flat face facing you: Pin 1 Source, Pin 2 Gate, Pin 3 Drain):
   * **Source (Pin 1):** Connect to GND rail.
   * **Gate (Pin 2):** Connect to Pico Pin 21 (GP16).
   * **Drain (Pin 3):** Connect to C64 CN8 Pin 3 (/RESTORE).
2. *(Optional pull-down):* Connect a 100kΩ resistor between Gate and Source to ensure the transistor stays OFF during microcontroller reset.

---

### Step 5: USB Keyboard & OTG Connection
1. Plug a standard **Micro-USB OTG Cable** (Micro-USB Male to USB-A Female) into the Raspberry Pi Pico's onboard micro-USB connector.
2. Plug your USB keyboard or 2.4GHz wireless combo receiver dongle (e.g. Logitech Unifying) into the USB-A female socket.

---

## 4. Pre-Power Safety Verification (Multimeter Checks)

Before powering on the C64:
1. **Continuity & Short Check:**
   * Test resistance between `+5V rail` and `GND rail`: must be $> 10\text{ k}\Omega$ (no short circuits).
   * Verify all 8 diode cathodes are connected to 74HCT245 pins 11-18, and anodes go to CN8 rows.
2. **Voltage Divider Test:**
   * With C64 powered OFF, disconnect the C64 ribbon cable.
   * Power the Pico via a 5V bench supply or USB charger.
   * Measure the 3.3V rail on Pico Pin 36 ($3.3\text{V} \pm 0.05\text{V}$).
   * Measure 74HCT245 Pin 20 ($5.0\text{V}$).
3. **Flashing Firmware:**
   * Hold the Pico's `BOOTSEL` button and plug into a PC.
   * Drag and drop `bin/c64_usb_keyboard.uf2` onto the `RPI-RP2` drive.
   * Once flashed, the Pico reboots automatically.

---

## 5. Live Testing on the Commodore 64

1. Turn off the Commodore 64.
2. Carefully attach the 20-pin female connector ribbon cable to CN8 on the C64 motherboard (observe Pin 1 alignment!).
3. Turn on the Commodore 64.
4. Observe the C64 boot screen:
   ```
      **** COMMODORE 64 BASIC V2 ****
    64K RAM SYSTEM  38911 BASIC BYTES FREE
   READY.
   ```
5. Plug the USB keyboard or wireless combo dongle into the OTG cable.
6. The Pico onboard LED (GP25) will flash briefly on keypresses.
7. Type `PRINT "HELLO COMMODORE"` and press `Enter`.
8. Verify special keys:
   * `F1`, `F3`, `F5`, `F7` and `F2`, `F4`, `F6`, `F8`
   * Cursor keys: `Down`, `Up`, `Right`, `Left`
   * `Home` (CLR/HOME) and `Shift+Home` (Clear Screen)
   * `Esc` (RUN/STOP)
   * `Page Up` or `F12` while holding `RUN/STOP` (Restore: tests NMI reset!)
   * `Left Alt` (Commodore C= key)
