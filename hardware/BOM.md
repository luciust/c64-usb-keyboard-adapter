# Bill of Materials (BOM) — Raspberry Pi Pico 2 Edition (100% DIP & THT)

By utilizing the **5V-tolerant Raspberry Pi Pico 2 (RP2350)**, all external level-shifter ICs (74HCT245), 16 voltage divider resistors, 8 Schottky diodes, and the RESTORE transistor have been **completely eliminated**.

The entire adapter now requires only the Pico 2, the C64 header, two filter capacitors, and optional series protection resistors.

| RefDes | Component / Value | Description | Package | Generic Part Number / Example | Qty |
|:---:|:---|:---|:---:|:---|:---:|
| **U1** | Raspberry Pi Pico 2 | RP2350 Dual ARM Cortex-M33 (5V-Tolerant) | 40-Pin DIP Module (2.54mm pitch) | SC1631 (Raspberry Pi Pico 2) | 1 |
| **J1** | 1x20 Pin Header | C64 Motherboard Keyboard Header (CN8) | 2.54mm pitch THT Pin Header (Pin 2 cut) | Standard 2.54mm 1x20 Breakaway Header | 1 |
| **R1-R8** | 100 Ω 5% 1/4W | *(Optional)* Row Series Safety Resistors | Axial Leaded 0207 / 1/4W (or 8-pin SIP) | CFR-25JB-52-100R | 8 |
| **C1** | 100 nF (0.1 µF) 50V | High-Frequency Ceramic Decoupling Capacitor | Radial Leaded (2.54mm pitch) | K104K15X7RF53L2 | 1 |
| **C2** | 22 µF to 47 µF 16V | Bulk +5V Filter Capacitor | Radial Electrolytic (2.54mm pitch) | UVZ1C470MDD | 1 |
| **J3** | 1x3 Pin Header | UART Debug Diagnostic Header | 2.54mm pitch THT Male Pin Header | Standard 1x3 Breakaway Header | 1 |
| **SOCKET1**| 2x 1x20 Female Headers| Sockets for Raspberry Pi Pico 2 | 20-Pin 2.54mm Single-Row Socket Strip | Standard 2.54mm Female Header 20-pin | 2 |

---

### Component Notes:
* **Microcontroller:** Must be the **Raspberry Pi Pico 2 (RP2350)** to take advantage of the 5V-tolerant GPIO architecture.
* **Optional Row Resistors (R1-R8):** While RP2350 GPIOs can connect directly in open-drain mode, placing $100\Omega$ series resistors provides an extra layer of ESD protection and current limiting without affecting scan speeds.
* **Power Connection:** Pin 4 of J1 (+5V) connects directly to Pico 2 `VBUS` (Pin 40), simultaneously powering the Pico 2 regulator and providing 5V power to the USB-A keyboard / wireless dongle.
