# PCB Layout Proposal & Design Guide (100% DIP & THT)

This document presents the PCB layout proposal, component placement floorplan, routing rules, and fabrication guidelines for the **C64 USB Keyboard & Wireless Host Adapter**.

---

## 1. PCB Specifications

* **Board Dimensions:** 85.0 mm × 55.0 mm (standard compact rectangular form factor)
* **Layer Count:** 2 Layers (Top Copper: F.Cu, Bottom Copper: B.Cu)
* **Board Thickness:** 1.6 mm FR-4 standard
* **Copper Weight:** 1 oz (35 µm)
* **Surface Finish:** HASL lead-free (or ENIG)
* **Minimum Trace Width:** 0.25 mm (10 mil) for signal lines; 0.6 mm (24 mil) for power lines (+5V, 3.3V)
* **Minimum Clearance:** 0.25 mm (10 mil)
* **Drill Specifications:**
  * Component leads: 0.8 mm - 1.0 mm
  * Header pins: 1.0 mm
  * Mounting holes: 4× 3.2 mm (M3 hardware) positioned with 4.0 mm inset from board edges.
* **Component Restriction:** **Strictly DIP and THT (Through-Hole Technology)**. No SMD parts.

---

## 2. Floorplan & Component Placement Strategy

```
+-----------------------------------------------------------------------+
| (H1)                     [ J2: USB Type-A THT ]                  (H2) |
|                                                                       |
|  [J1: C64 CN8]         [ R1 - R8: Upper 1.8k ]     +---------------+  |
|  1  GND                [ R9 - R16: Lower 3.3k ]    |               |  |
|  2  KEY (cut)                                      |  U1: PICO     |  |
|  3  /RESTORE <-- [Q1: 2N7000]                      |  (Socketed    |  |
|  4  +5V -----------------> [C3: 47uF]              |   2x20 THT    |  |
|  5  PB3                                            |   Headers)    |  |
|  6  PB6                +-------------------+       |               |  |
|  7  PB5                |   U2: 74HCT245    |       |               |  |
|  8  PB4                |   (DIP-20 Socket) | [C1]  |               |  |
|  9  PB7                +-------------------+       |               |  |
|  10 PB2                         |                  |               |  |
|  11 PB1                +-------------------+       |               |  |
|  12 PB0                | D1 - D8: BAT42    |       |               |  |
|  13 PA7                | (Schottky Diodes) |       |               |  |
|  14 PA6                +-------------------+       +---------------+  |
|  ...                                                                  |
|  20 PA0                                          [J3: UART DEBUG]     |
| (H3)                                                             (H4) |
+-----------------------------------------------------------------------+
```

### 2.1 Placement Zones
1. **Left Edge (C64 Interface Zone):**
   * **J1 (C64 CN8 Connector):** Placed directly on the left edge. A standard 1×20 (or 2×10) 2.54mm pitch male header allows a short ribbon cable to mate directly with the C64 motherboard.
   * **Q1 (2N7000) & R17:** Positioned immediately adjacent to Pin 3 (/RESTORE) to minimize NMI trace length.
2. **Center Zone (Level Translation & Open-Drain Buffering):**
   * **U2 (74HCT245 DIP-20):** Placed in the center in a vertical orientation.
   * **C1 (100nF decoupling):** Placed directly across Pin 20 (VCC) and Pin 10 (GND) of U2.
   * **D1 - D8 (Schottky Diodes):** Arranged in a neat axial row between U2 output pins (B1-B8) and J1 row pins (PB0-PB7). Cathode bands face U2.
   * **R1 - R8 (1.8kΩ) and R9 - R16 (3.3kΩ):** Arranged in parallel rows between J1 column pins (PA0-PA7) and the Pico inputs.
3. **Right Zone (Microcontroller Core):**
   * **U1 (Raspberry Pi Pico):** Mounted via two 1×20 female pin header strips. The micro-USB port faces the top edge, allowing the optional use of an OTG adapter cable directly into the Pico, or routing to the onboard THT USB Type-A connector (J2).
4. **Top Edge (USB Host Interface):**
   * **J2 (USB Type-A Female THT):** Positioned along the top edge for convenient keyboard / wireless dongle insertion.
5. **Bottom-Right (Diagnostic & Expansion):**
   * **J3 (UART Debug):** 3-pin header (TX, RX, GND) for connection to a USB-to-Serial adapter for diagnostics at 115200 baud.

---

## 3. Power Distribution & Ground Plane Architecture

1. **Power Infeed (+5V):**
   * Derives from C64 CN8 Pin 4.
   * Feeds directly into:
     * C3 (47µF bulk capacitor)
     * U2 (74HCT245 Pin 20) via a 0.6 mm (24 mil) power trace with C1 (100nF) ceramic bypass.
     * Raspberry Pi Pico **VBUS (Pin 40)**, which powers the internal RT6150 buck-boost regulator and supplies 5V to the USB host port.
2. **Ground Plane (B.Cu):**
   * The entire bottom layer (B.Cu) is configured as a solid, continuous Ground plane fill (copper pour).
   * All GND pins (J1 Pin 1, Pico Pins 3, 8, 13, 18, 23, 28, 33, 38, U2 Pin 10, C1/C2/C3 negative, R9-R16 ground rail) connect directly into this ground pour with thermal relief pads.
   * A solid ground pour prevents ground bounce during high-speed CIA matrix scanning.

---

## 4. Signal Routing Strategy

1. **Columns (C64 PA0-PA7 → Pico GP0-GP7):**
   * Traces route from J1 Pins 13-20 through series resistors R1-R8 ($1.8\text{ k}\Omega$).
   * At the node between $R_{\text{series}}$ and $R_{\text{pull-down}}$, a 0.25 mm trace routes directly to Pico GP0-GP7.
   * Since this is a simple resistor divider with $\tau \approx 5.8\text{ ns}$, trace length matching is not critical.
2. **Rows (Pico GP8-GP15 → 74HCT245 → Diodes → C64 PB0-PB7):**
   * Clean, short 0.25 mm traces connect Pico GP8-GP15 to 74HCT245 A-side inputs (Pins 2-9).
   * Output pins (B1-B8, Pins 11-18) connect directly to the cathodes of D1-D8.
   * Anodes of D1-D8 route to J1 Pins 5-12.
3. **RESTORE Line:**
   * Short trace from Pico GP16 to Gate of Q1.
   * Drain connects directly to J1 Pin 3.
