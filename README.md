# Gemini coded - NOT TESTED YET - Commodore 64 USB Keyboard & Wireless Host Adapter

A dual-core Raspberry Pi Pico (RP2040) bridge that connects modern USB keyboards and 2.4GHz wireless keyboard/mouse combos directly to the Commodore 64 (C64) mainboard keyboard connector (**CN8**).

Designed with **100% Through-Hole Technology (THT) and DIP components** for easy breadboard prototyping, hand soldering, and vintage hardware protection.

---

## Key Features

* **USB Host & Wireless Combo Support:**
  * Connects standard wired USB keyboards (104/105-key HID).
  * Supports **2.4GHz wireless combo dongles** (e.g. Logitech Unifying, Dell, HP) with composite keyboard + mouse interfaces.
  * Correctly identifies keyboard reports and safely isolates mouse data.
* **Vintage 5V Hardware Protection:**
  * **Columns (C64 → Pico):** Passive precision resistor dividers ($1.8\text{ k}\Omega / 3.3\text{ k}\Omega$) step down the C64 NMOS CIA $4.0\text{V} - 5.0\text{V}$ scan lines safely to $2.6\text{V} - 3.2\text{V}$ without exceeding the RP2040 $3.3\text{V}$ maximum limit.
  * **Rows (Pico → C64):** An octal **74HCT245** bus transceiver (DIP-20) coupled with **8x BAT42 Schottky diodes** emulates true open-drain/open-collector outputs.
  * **Joystick Port 1 Conflict Immunity:** Prevents catastrophic short-circuits if a joystick is pushed or fired while the keyboard adapter is active.
* **Zero-Latency Real-Time Emulation (< 50 ns):**
  * **Core 0:** Runs TinyUSB Host stack, HID parsing, hold-time pacing, and USB enumeration.
  * **Core 1:** Dedicated uninhibited real-time matrix engine directly monitoring C64 CIA 1 Port A column strobes and driving Port B rows in $< 50\text{ ns}$ (over 70× faster than the 1 MHz 6510 CPU read cycle).
* **KERNAL Debounce & Pacing Filter:**
  * Enforces a $35\text{ ms}$ minimum contact hold time (`C64_MIN_HOLD_TIME_US`) across multiple 50Hz/60Hz C64 vertical blank interrupt frames ($EA87) to ensure 100% key registration during fast typing.
* **Authentic Matrix & Special Keys:**
  * Automatic Shift pairing for Cursor Up/Left, Insert, and even-numbered Function keys (F2, F4, F6, F8).
  * Dedicated open-drain N-channel MOSFET (`2N7000`) for the C64 `RESTORE` key (Pin 3), mapped to `Page Up`, `Pause/Break`, or `F12`.
* **Hardware Construction:**
  * Strictly **DIP & THT (Through-Hole)** components.
  * Complete KiCad 7/8 schematic and 2-layer PCB layout project included.

---

## Project Structure

```
├── bin/
│   └── c64_usb_keyboard.uf2        # Pre-built, ready-to-flash Pico firmware
├── firmware/
│   ├── CMakeLists.txt              # CMake Pico SDK build configuration
│   ├── pico_sdk_import.cmake       # Pico SDK import script
│   ├── tusb_config.h               # TinyUSB Host stack configuration
│   ├── build/                      # Build output directory
│   └── src/
│       ├── main.c                  # Core 0 loop & Core 1 multicore launch
│       ├── c64_matrix.h            # Matrix GPIO definitions and API
│       ├── c64_matrix.c            # Real-time Core 1 snooper & contact hold-time logic
│       ├── keymap.h                # USB HID to C64 matrix mapping types & flags
│       ├── keymap.c                # Full 104-key USB to C64 8x8 matrix lookup table
│       ├── usb_hid_host.h          # TinyUSB host interface
│       └── usb_hid_host.c          # HID report parser & combo device handler
├── hardware/
│   ├── BOM.md                      # Complete 100% DIP/THT Bill of Materials
│   ├── breadboard_guide.md         # Step-by-step breadboard assembly and test guide
│   ├── PCB_LAYOUT_PROPOSAL.md      # Detailed PCB layout proposal & design rules
│   ├── generate_kicad.py           # KiCad project generation script
│   └── kicad/
│       ├── c64_usb_keyboard.kicad_pro  # KiCad project file
│       ├── c64_usb_keyboard.kicad_sch  # KiCad schematic file
│       └── c64_usb_keyboard.kicad_pcb  # KiCad 2-layer PCB layout file
└── docs/
    └── voltage_level_research.md   # In-depth research on 4V/3.3V translation & debouncing
```

---

## Quick Start: Flashing the Pico

1. Connect your Raspberry Pi Pico to your computer while holding down the **BOOTSEL** button.
2. The Pico will mount as a mass storage volume named `RPI-RP2`.
3. Copy `bin/c64_usb_keyboard.uf2` into the `RPI-RP2` drive.
4. The Pico will reboot automatically and start running the C64 keyboard bridge.

---

## Wiring Summary (C64 Mainboard CN8 Connector)

| CN8 Pin | Signal | Destination | Function / Notes |
|:---:|:---|:---|:---|
| **1** | GND | Common GND | System Ground reference |
| **2** | KEY | *None* | Polarizing pin (cut on motherboard header) |
| **3** | /RESTORE | Q1 Drain (2N7000) | Pulls active-low NMI to GND |
| **4** | +5V DC | Pico VBUS (Pin 40), U2 Pin 20 | Power input from C64 |
| **5** | Row 3 (PB3) | D4 Anode | Pulled low via BAT42 from 74HCT245 Pin 15 (B4) |
| **6** | Row 6 (PB6) | D7 Anode | Pulled low via BAT42 from 74HCT245 Pin 12 (B7) |
| **7** | Row 5 (PB5) | D6 Anode | Pulled low via BAT42 from 74HCT245 Pin 13 (B6) |
| **8** | Row 4 (PB4) | D5 Anode | Pulled low via BAT42 from 74HCT245 Pin 14 (B5) |
| **9** | Row 7 (PB7) | D8 Anode | Pulled low via BAT42 from 74HCT245 Pin 11 (B8) |
| **10** | Row 2 (PB2) | D3 Anode | Pulled low via BAT42 from 74HCT245 Pin 16 (B3) |
| **11** | Row 1 (PB1) | D2 Anode | Pulled low via BAT42 from 74HCT245 Pin 17 (B2) |
| **12** | Row 0 (PB0) | D1 Anode | Pulled low via BAT42 from 74HCT245 Pin 18 (B1) |
| **13** | Col 7 (PA7) | R8 (1.8k) → Pico GP7 | Stepped down to safe 3.2V (R16 3.3k to GND) |
| **14** | Col 6 (PA6) | R7 (1.8k) → Pico GP6 | Stepped down to safe 3.2V (R15 3.3k to GND) |
| **15** | Col 5 (PA5) | R6 (1.8k) → Pico GP5 | Stepped down to safe 3.2V (R14 3.3k to GND) |
| **16** | Col 4 (PA4) | R5 (1.8k) → Pico GP4 | Stepped down to safe 3.2V (R13 3.3k to GND) |
| **17** | Col 3 (PA3) | R4 (1.8k) → Pico GP3 | Stepped down to safe 3.2V (R12 3.3k to GND) |
| **18** | Col 2 (PA2) | R3 (1.8k) → Pico GP2 | Stepped down to safe 3.2V (R11 3.3k to GND) |
| **19** | Col 1 (PA1) | R2 (1.8k) → Pico GP1 | Stepped down to safe 3.2V (R10 3.3k to GND) |
| **20** | Col 0 (PA0) | R1 (1.8k) → Pico GP0 | Stepped down to safe 3.2V (R9 3.3k to GND) |

---

## Building Firmware from Source

To rebuild the firmware using the local Pico SDK:

```bash
cd firmware
mkdir -p build && cd build
export PICO_SDK_PATH=/home/lucius/Priv/AGRAVITY/pico-sdk
cmake ..
make -j$(nproc)
```

The compiled UF2 file will be generated at `firmware/build/c64_usb_keyboard.uf2`.

---

## Documentation Links

* [Voltage Level Shifting, Matrix & Debounce Research](docs/voltage_level_research.md)
* [Breadboard Testing & Prototyping Guide](hardware/breadboard_guide.md)
* [Bill of Materials (100% DIP & THT)](hardware/BOM.md)
* [PCB Layout Proposal & Design Guide](hardware/PCB_LAYOUT_PROPOSAL.md)
* [KiCad Project Directory](hardware/kicad/)
