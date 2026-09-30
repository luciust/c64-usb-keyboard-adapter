# Bill of Materials (BOM) — 100% DIP & THT

All components selected for this project use strictly **Through-Hole Technology (THT)** and **Dual In-line Packages (DIP)**. No surface mount devices (SMD) are required.

| RefDes | Component / Value | Description | Package | Generic Part Number / Example | Qty |
|:---:|:---|:---|:---:|:---|:---:|
| **U1** | Raspberry Pi Pico | RP2040 Dual ARM Cortex-M0+ MCU | 40-Pin DIP Module (2.54mm pitch) | SC0915 (Pico) or Pico H | 1 |
| **U2** | 74HCT245 | Octal 3-State Bus Transceiver | DIP-20 (0.3" / 7.62mm pitch) | 74HCT245N, SN74HCT245N | 1 |
| **D1-D8** | BAT42 / BAT43 / BAT85 | Low $V_F$ Schottky Barrier Diode | DO-35 (Axial leaded) | BAT42, BAT43, BAT85, 1N5819 | 8 |
| **Q1** | 2N7000 / BS170 | N-Channel Small-Signal MOSFET | TO-92 | 2N7000, BS170 (or 2N3904 BJT) | 1 |
| **R1-R8** | 1.8 kΩ 5% 1/4W | Upper Divider Resistor (PA0-PA7) | Axial Leaded 0207 / 1/4W | CFR-25JB-52-1K8 | 8 |
| **R9-R16** | 3.3 kΩ 5% 1/4W | Lower Divider Resistor (Pull-down to GND) | Axial Leaded 0207 / 1/4W | CFR-25JB-52-3K3 | 8 |
| **R17** | 100 kΩ 5% 1/4W | Gate pull-down resistor for Q1 | Axial Leaded 0207 / 1/4W | CFR-25JB-52-100K | 1 |
| **C1, C2** | 100 nF (0.1 µF) 50V | Decoupling Ceramic Capacitor | Radial Leaded (5.08mm / 2.54mm pitch) | K104K15X7RF53L2 | 2 |
| **C3** | 22 µF to 47 µF 16V | Bulk Power Filter Capacitor | Radial Electrolytic (2.54mm pitch) | UVZ1C470MDD | 1 |
| **J1** | 1x20 (or 2x10) Pin Header | C64 Keyboard Header (CN8) | 2.54mm pitch THT Male/Female Pin Header | Standard 2.54mm 1x20 header (Pin 2 cut) | 1 |
| **J2** | USB Type-A Female | USB Host Connector (Optional on PCB) | Right Angle THT USB Type-A Receptacle | USB-A1HSW6 | 1 |
| **J3** | 1x3 Pin Header | UART Debug Header (TX, RX, GND) | 2.54mm pitch THT Male Pin Header | Standard 1x3 Breakaway Header | 1 |
| **SOCKET1** | DIP-20 IC Socket | Socket for 74HCT245 | 20-Pin DIP (0.3" row spacing) | A 20-LC-TT | 1 |
| **SOCKET2** | 2x 1x20 Female Headers | Socket for Raspberry Pi Pico | 20-Pin 2.54mm Single-Row Socket Strip | Standard 2.54mm Female Header 20-pin | 2 |

---

### Component Substitution Notes
1. **Diodes D1 - D8:**
   * Preferred: `BAT42`, `BAT43`, `BAT85` (DO-35 glass package, forward voltage $V_F \approx 0.25\text{V}$ at 2mA).
   * Alternative: `1N5819` (DO-41 package, Schottky, slightly larger body).
   * Do NOT use standard silicon switching diodes (`1N4148`) if avoidable, as their $V_F$ is ~0.65V, which leaves less noise margin under the C64 $V_{IL\text{ max}} = 0.8\text{V}$ threshold.
2. **Resistor Packs:**
   * Instead of 16 individual axial resistors, you can substitute:
     * 1x 9-Pin SIP Resistor Network $1.8\text{ k}\Omega$ (Isolated, 8 independent elements, 16 pins or 2x 8-pin SIP)
     * 1x 9-Pin SIP Resistor Network $3.3\text{ k}\Omega$ (Bussed, 1 common GND pin + 8 resistors).
     * Both options use standard 2.54mm through-hole footprints.
3. **Pico Sockets:**
   * It is strongly recommended to install two 20-pin female header strips on the PCB rather than soldering the Pico directly. This allows the Pico to be easily unplugged for firmware updates or reuse.
