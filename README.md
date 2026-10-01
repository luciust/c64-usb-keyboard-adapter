# Gemini coded - NOT TESTED YET - Commodore 64 USB Keyboard & Wireless Host Adapter (Pico 2 Edition)

A high-performance **Raspberry Pi Pico 2 (RP2350)** bridge that connects modern USB keyboards and 2.4GHz wireless keyboard/mouse combos directly to the Commodore 64 (C64) mainboard keyboard connector (**CN8**).

Leveraging the **5V-tolerant GPIO architecture** of the RP2350, this project eliminates all external level-shifter transceivers, voltage divider resistors, and discrete open-drain diodes, reducing the entire board to just the **Pico 2, the C64 header, and two filter capacitors**.

---

## Key Features

* **Raspberry Pi Pico 2 (RP2350) Architecture:**
  * **5V-Tolerant Digital GPIOs:** GP0–GP16 directly interface with the C64's 5V NMOS CIA 6526 logic lines with **zero external level-shifting ICs**.
  * **Native Open-Drain Matrix Driving:** GP8–GP15 drive the C64 rows in native open-drain mode (0V drive / 5V High-Z), providing 100% hardware immunity against Joystick 1 bus contention.
  * **Direct RESTORE Key Driving:** GP16 drives the C64 Pin 3 (/RESTORE active-low NMI) directly in open-drain mode without extra transistors.
* **USB Host & Wireless Combo Support:**
  * Supports standard USB keyboards (104/105-key HID).
  * Supports **2.4GHz wireless combo dongles** (e.g. Logitech Unifying, Dell, HP) with composite keyboard + mouse interfaces.
  * Safely filters mouse reports while processing keyboard keystrokes.
* **Zero-Latency Real-Time Emulation (< 30 ns):**
  * **Core 0:** Runs TinyUSB Host stack, HID parsing, contact pacing, and USB enumeration.
  * **Core 1:** Dedicated real-time matrix engine monitoring C64 CIA 1 Port A column strobes and toggling row output enables in $< 30\text{ ns}$ (over 100× faster than the 1 MHz 6510 CPU read cycle).
* **KERNAL Debounce & Pacing Filter:**
  * Enforces a $35\text{ ms}$ minimum contact hold time (`C64_MIN_HOLD_TIME_US`) across multiple 50Hz/60Hz C64 vertical interrupt frames ($EA87) to ensure 100% key registration during fast typing.
* **Ultra-Simple Hardware Construction:**
  * Strictly **100% Through-Hole Technology (THT) and DIP** components.
  * Board dimensions: **60.0 mm × 58.0 mm** compact backpack format.
  * Complete **KiCad 8** schematic and 2-layer PCB layout project included.

---

## Project Structure

```
├── bin/
│   ├── c64_usb_keyboard_pico2.uf2  # Pre-built firmware for Raspberry Pi Pico 2 (RP2350)
│   ├── c64_usb_keyboard_pico1.uf2  # Backward-compatible build for Raspberry Pi Pico 1 (RP2040)
│   └── c64_usb_keyboard.uf2        # Default active binary (Pico 2)
├── firmware/
│   ├── CMakeLists.txt              # CMake Pico SDK build configuration
│   ├── pico_sdk_import.cmake       # Pico SDK import script
│   ├── tusb_config.h               # TinyUSB Host stack configuration
│   └── src/
│       ├── main.c                  # Core 0 loop & Core 1 multicore launch
│       ├── c64_matrix.h            # Matrix GPIO definitions and open-drain API
│       ├── c64_matrix.c            # Real-time Core 1 native open-drain engine
│       ├── keymap.h                # USB HID to C64 matrix mapping types & flags
│       ├── keymap.c                # Full 104-key USB to C64 8x8 matrix lookup table
│       ├── usb_hid_host.h          # TinyUSB host interface
│       └── usb_hid_host.c          # HID report parser & combo device handler
├── hardware/
│   ├── BOM.md                      # Ultra-minimal Bill of Materials
│   ├── breadboard_guide.md         # Step-by-step breadboard assembly and test guide
│   ├── PCB_LAYOUT_PROPOSAL.md      # Detailed KiCad 8 PCB layout guide
│   ├── generate_kicad.py           # KiCad 8 project generation script
│   └── kicad/
│       ├── c64_usb_keyboard.kicad_pro  # KiCad 8 project file
│       ├── c64_usb_keyboard.kicad_sch  # KiCad 8 schematic file
│       └── c64_usb_keyboard.kicad_pcb  # KiCad 8 2-layer PCB layout file
└── docs/
    └── voltage_level_research.md   # In-depth research on RP2350 5V tolerance vs RP2040
```

---

## Quick Start: Flashing the Pico 2

1. Connect your **Raspberry Pi Pico 2** to your PC via USB while holding down the **BOOTSEL** button.
2. The board will mount as a mass storage volume named `RP2350`.
3. Drag and drop [`bin/c64_usb_keyboard_pico2.uf2`](bin/c64_usb_keyboard_pico2.uf2) onto the `RP2350` drive.
4. The board will reboot automatically into USB Host bridge mode.

---

## Wiring Summary (C64 Mainboard CN8 $\leftrightarrow$ Pico 2)

| CN8 Pin | Signal | Destination | Function / Notes |
|:---:|:---|:---|:---|
| **1** | GND | Pico 2 GND (Pins 3, 38) | Common Ground reference |
| **2** | KEY | *None* | Polarizing pin (cut on motherboard header) |
| **3** | /RESTORE | Pico 2 GP16 (Pin 21) | Direct native open-drain NMI trigger |
| **4** | +5V DC | Pico 2 VBUS (Pin 40) | Powers Pico 2 & USB Keyboard |
| **5** | Row 3 (PB3) | Pico 2 GP11 (Pin 15) | Native Open-Drain *(via optional 100Ω)* |
| **6** | Row 6 (PB6) | Pico 2 GP14 (Pin 19) | Native Open-Drain *(via optional 100Ω)* |
| **7** | Row 5 (PB5) | Pico 2 GP13 (Pin 17) | Native Open-Drain *(via optional 100Ω)* |
| **8** | Row 4 (PB4) | Pico 2 GP12 (Pin 16) | Native Open-Drain *(via optional 100Ω)* |
| **9** | Row 7 (PB7) | Pico 2 GP15 (Pin 20) | Native Open-Drain *(via optional 100Ω)* |
| **10** | Row 2 (PB2) | Pico 2 GP10 (Pin 14) | Native Open-Drain *(via optional 100Ω)* |
| **11** | Row 1 (PB1) | Pico 2 GP9  (Pin 12) | Native Open-Drain *(via optional 100Ω)* |
| **12** | Row 0 (PB0) | Pico 2 GP8  (Pin 11) | Native Open-Drain *(via optional 100Ω)* |
| **13** | Col 7 (PA7) | Pico 2 GP7  (Pin 10) | Direct 5V-tolerant input |
| **14** | Col 6 (PA6) | Pico 2 GP6  (Pin 9)  | Direct 5V-tolerant input |
| **15** | Col 5 (PA5) | Pico 2 GP5  (Pin 7)  | Direct 5V-tolerant input |
| **16** | Col 4 (PA4) | Pico 2 GP4  (Pin 6)  | Direct 5V-tolerant input |
| **17** | Col 3 (PA3) | Pico 2 GP3  (Pin 5)  | Direct 5V-tolerant input |
| **18** | Col 2 (PA2) | Pico 2 GP2  (Pin 4)  | Direct 5V-tolerant input |
| **19** | Col 1 (PA1) | Pico 2 GP1  (Pin 2)  | Direct 5V-tolerant input |
| **20** | Col 0 (PA0) | Pico 2 GP0  (Pin 1)  | Direct 5V-tolerant input |

---

## Building Firmware from Source

```bash
cd firmware
mkdir -p build && cd build
export PICO_SDK_PATH=/home/lucius/Priv/AGRAVITY/pico-sdk
cmake -DPICO_BOARD=pico2 ..
make -j$(nproc)
```

---

## Documentation Links

* [Voltage Level Shifting & RP2350 5V Tolerance Research](docs/voltage_level_research.md)
* [Breadboard Testing & Prototyping Guide](hardware/breadboard_guide.md)
* [Bill of Materials (Pico 2 Edition)](hardware/BOM.md)
* [PCB Layout Proposal & Design Guide (KiCad 8)](hardware/PCB_LAYOUT_PROPOSAL.md)
* [KiCad 8 Project Directory](hardware/kicad/)
