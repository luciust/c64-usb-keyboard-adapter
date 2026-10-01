# PCB Layout Proposal & Design Guide (Pico 2 Edition)

This document presents the simplified PCB layout proposal, KiCad 8 architecture, component floorplan, and routing rules for the **C64 USB Keyboard & Wireless Host Adapter (Pico 2 Edition)**.

---

## 1. PCB Specifications

* **Board Dimensions:** 60.0 mm × 58.0 mm (ultra-compact backpack form factor)
* **Layer Count:** 2 Layers (Top Copper: F.Cu, Bottom Copper: B.Cu)
* **Board Thickness:** 1.6 mm FR-4 standard
* **Copper Weight:** 1 oz (35 µm)
* **Surface Finish:** Lead-free HASL (or ENIG)
* **KiCad Compatibility:** Strictly **KiCad 8.0+** compatible with full UUID tree hierarchy
* **Minimum Trace Width:** 0.25 mm (10 mil) for signal lines; 0.6 mm (24 mil) for +5V power
* **Minimum Clearance:** 0.25 mm (10 mil)
* **Mounting Holes:** 4× 3.2 mm (M3 hardware) positioned at (3.5, 3.5), (56.5, 3.5), (3.5, 54.5), (56.5, 54.5)
* **Component Restriction:** **Strictly DIP and THT (Through-Hole Technology)**

---

## 2. Floorplan & Component Placement Strategy

```
+---------------------------------------------------------------+
| (H1)                                                     (H2) |
|                                                               |
|  [J1: C64 CN8]         [ C1: 100nF ]       +---------------+  |
|  1  GND                [ C2: 47uF  ]       |               |  |
|  2  KEY (cut)                              |  U1: PICO 2   |  |
|  3  /RESTORE ----------------------------> |  (RP2350)     |  |
|  4  +5V ---------------------------------> |  Socketed     |  |
|  5  PB3 ----> [ R4: 100R ] --------------> |  2x20 THT     |  |
|  6  PB6 ----> [ R7: 100R ] --------------> |  Headers      |  |
|  7  PB5 ----> [ R6: 100R ] --------------> |               |  |
|  8  PB4 ----> [ R5: 100R ] --------------> |               |  |
|  9  PB7 ----> [ R8: 100R ] --------------> |               |  |
|  10 PB2 ----> [ R3: 100R ] --------------> |               |  |
|  11 PB1 ----> [ R2: 100R ] --------------> |               |  |
|  12 PB0 ----> [ R1: 100R ] --------------> |               |  |
|  13 PA7 ---------------------------------> |               |  |
|  14 PA6 ---------------------------------> |               |  |
|  ...                                       |               |  |
|  20 PA0 ---------------------------------> +---------------+  |
|                                                               |
|                        [J3: UART DEBUG]                       |
| (H3)                                                     (H4) |
+---------------------------------------------------------------+
```

### 2.1 Placement Zones
1. **Left Edge (C64 Interface Zone):**
   * **J1 (C64 CN8 Connector):** Standard 1×20 (or 2×10) 2.54mm pitch male pin header placed at $X = 7.0\text{ mm}$. A short 20-pin IDC ribbon cable or direct right-angle socket mates to the C64 motherboard.
2. **Center Zone (Safety Resistors & Filtering):**
   * **R1 - R8 (100Ω Safety Resistors):** Arranged in a single neat vertical row at $X = 19.0\text{ mm}$.
   * **C1 (100nF Ceramic Decoupling) & C2 (47µF Bulk Filter):** Placed at $X = 16.0\text{ mm}$ and $X = 24.0\text{ mm}$ directly adjacent to Pin 4 (+5V).
3. **Right Zone (Pico 2 Core):**
   * **U1 (Raspberry Pi Pico 2):** Mounted via two 1×20 female header strips at $X = 34.0\text{ mm}$ and $X = 51.78\text{ mm}$. The micro-USB port faces the top edge for convenient keyboard / wireless dongle connection.
4. **Bottom Zone (Diagnostics):**
   * **J3 (UART Debug):** 1×3 pin header (TX, RX, GND) at $X = 24.0\text{ mm}, Y = 48.0\text{ mm}$.

---

## 3. Power Distribution & Ground Plane Architecture

1. **Power Infeed (+5V):**
   * Derives from C64 CN8 Pin 4.
   * Feeds C2 (47µF bulk capacitor), C1 (100nF high-frequency bypass), and Pico 2 **Pin 40 (VBUS)** via a heavy 0.6 mm (24 mil) copper trace.
   * Pico 2 onboard buck-boost regulator steps 5V down to 3.3V for RP2350 logic, and passes 5V through to the USB port to power connected keyboards.
2. **Ground Plane (B.Cu):**
   * Solid continuous ground copper pour covering the entire bottom layer.
   * All GND pins (J1 Pin 1, Pico 2 Pins 3, 8, 13, 18, 23, 28, 33, 38, C1/C2 negative) connect directly into this ground plane with thermal relief spokes.

---

## 4. Signal Routing Strategy

1. **Columns (C64 PA0-PA7 $\rightarrow$ Pico 2 GP0-GP7):**
   * Direct point-to-point horizontal traces on the top copper layer (F.Cu).
   * Since the RP2350 digital inputs are 5V-tolerant, no divider resistors are required.
2. **Rows (C64 PB0-PB7 $\rightarrow$ Resistors R1-R8 $\rightarrow$ Pico 2 GP8-GP15):**
   * Clean horizontal routing on F.Cu through $100\Omega$ current-limiting resistors.
3. **RESTORE Line:**
   * Direct trace from C64 CN8 Pin 3 to Pico 2 GP16 (Pin 21) in native open-drain mode.
