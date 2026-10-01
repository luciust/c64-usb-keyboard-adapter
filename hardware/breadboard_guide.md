# Breadboard Prototyping & Testing Guide (Pico 2 Edition)

This guide walks you through building and testing the ultra-simplified **C64 USB Keyboard & Wireless Host Adapter** using the **Raspberry Pi Pico 2 (RP2350)**.

Thanks to the RP2350's **5V-tolerant GPIOs** and native open-drain matrix emulation, breadboard assembly takes **under 10 minutes** with virtually no complex wiring.

---

## 1. Breadboard Bill of Materials

| Item | Component | Package | Quantity | Description / Value |
|:---:|:---|:---:|:---:|:---|
| 1 | Raspberry Pi Pico 2 | 40-pin DIP | 1 | RP2350 microcontroller board (with pin headers) |
| 2 | Jumper Wire Ribbon | 20-pin | 1 | 2.54mm pitch female header cable to C64 CN8 connector |
| 3 | USB OTG Cable | Cable | 1 | Micro-USB male to USB-A female adapter |
| 4 | Ceramic Capacitor | Radial THT | 1 | 100 nF (0.1 µF) decoupling across +5V and GND |
| 5 | Electrolytic Capacitor | Radial THT | 1 | 10 µF to 47 µF 16V bulk filter across +5V and GND |
| 6 | Resistors (Optional) | Axial 1/4W | 8 | 100 Ω safety series resistors for rows PB0-PB7 |
| 7 | Solderless Breadboard | Half/Full | 1 | Standard solderless breadboard |

---

## 2. Complete Pinout & Wiring Table

Connect your breadboard jumper wires directly between the **C64 Motherboard Keyboard Connector (CN8)** and the **Raspberry Pi Pico 2**:

| C64 CN8 Pin | Signal Name | C64 Function | Pico 2 Pin | Pico 2 GPIO | Electrical Mode |
|:---:|:---|:---|:---:|:---|:---|
| **1** | GND | System Ground | **Pin 3, 38** | GND | Common Ground Reference |
| **2** | KEY | Polarizing Pin | — | — | *Missing pin (polarization plug)* |
| **3** | /RESTORE | Active-Low NMI | **Pin 21** | GP16 | Native Open-Drain Output |
| **4** | +5V DC | Power Supply | **Pin 40** | VBUS | Powers Pico 2 & USB Keyboard |
| **5** | Row 3 | PB3 (CIA 1) | **Pin 15** | GP11 *(via 100Ω)* | Native Open-Drain Output |
| **6** | Row 6 | PB6 (CIA 1) | **Pin 19** | GP14 *(via 100Ω)* | Native Open-Drain Output |
| **7** | Row 5 | PB5 (CIA 1) | **Pin 17** | GP13 *(via 100Ω)* | Native Open-Drain Output |
| **8** | Row 4 | PB4 (CIA 1) | **Pin 16** | GP12 *(via 100Ω)* | Native Open-Drain Output |
| **9** | Row 7 | PB7 (CIA 1) | **Pin 20** | GP15 *(via 100Ω)* | Native Open-Drain Output |
| **10** | Row 2 | PB2 (CIA 1) | **Pin 14** | GP10 *(via 100Ω)* | Native Open-Drain Output |
| **11** | Row 1 | PB1 (CIA 1) | **Pin 12** | GP9 *(via 100Ω)* | Native Open-Drain Output |
| **12** | Row 0 | PB0 (CIA 1) | **Pin 11** | GP8 *(via 100Ω)* | Native Open-Drain Output |
| **13** | Col 7 | PA7 (CIA 1) | **Pin 10** | GP7 | 5V-Tolerant Direct Input |
| **14** | Col 6 | PA6 (CIA 1) | **Pin 9** | GP6 | 5V-Tolerant Direct Input |
| **15** | Col 5 | PA5 (CIA 1) | **Pin 7** | GP5 | 5V-Tolerant Direct Input |
| **16** | Col 4 | PA4 (CIA 1) | **Pin 6** | GP4 | 5V-Tolerant Direct Input |
| **17** | Col 3 | PA3 (CIA 1) | **Pin 5** | GP3 | 5V-Tolerant Direct Input |
| **18** | Col 2 | PA2 (CIA 1) | **Pin 4** | GP2 | 5V-Tolerant Direct Input |
| **19** | Col 1 | PA1 (CIA 1) | **Pin 2** | GP1 | 5V-Tolerant Direct Input |
| **20** | Col 0 | PA0 (CIA 1) | **Pin 1** | GP0 | 5V-Tolerant Direct Input |

---

## 3. Step-by-Step Breadboard Assembly

### Step 1: Place the Pico 2 & Power Rail
1. Insert the **Raspberry Pi Pico 2** across the center divider of your breadboard.
2. Connect C64 CN8 Pin 1 (GND) to the breadboard GND rail and Pico 2 Pin 38 (GND).
3. Connect C64 CN8 Pin 4 (+5V) to Pico 2 **Pin 40 (VBUS)**.
4. Place the **47 µF electrolytic capacitor** and **100 nF ceramic capacitor** across +5V and GND.

### Step 2: Wire Columns (PA0 - PA7)
Connect direct jumper wires from C64 CN8 column pins to Pico 2 GP0-GP7:
* CN8 Pin 20 $\rightarrow$ Pico 2 GP0 (Pin 1)
* CN8 Pin 19 $\rightarrow$ Pico 2 GP1 (Pin 2)
* CN8 Pin 18 $\rightarrow$ Pico 2 GP2 (Pin 4)
* CN8 Pin 17 $\rightarrow$ Pico 2 GP3 (Pin 5)
* CN8 Pin 16 $\rightarrow$ Pico 2 GP4 (Pin 6)
* CN8 Pin 15 $\rightarrow$ Pico 2 GP5 (Pin 7)
* CN8 Pin 14 $\rightarrow$ Pico 2 GP6 (Pin 9)
* CN8 Pin 13 $\rightarrow$ Pico 2 GP7 (Pin 10)

### Step 3: Wire Rows (PB0 - PB7) & RESTORE
Connect direct jumper wires (or insert $100\Omega$ resistors in series) from C64 CN8 row pins to Pico 2 GP8-GP15:
* CN8 Pin 12 (PB0) $\rightarrow$ Pico 2 GP8  (Pin 11)
* CN8 Pin 11 (PB1) $\rightarrow$ Pico 2 GP9  (Pin 12)
* CN8 Pin 10 (PB2) $\rightarrow$ Pico 2 GP10 (Pin 14)
* CN8 Pin 5  (PB3) $\rightarrow$ Pico 2 GP11 (Pin 15)
* CN8 Pin 8  (PB4) $\rightarrow$ Pico 2 GP12 (Pin 16)
* CN8 Pin 7  (PB5) $\rightarrow$ Pico 2 GP13 (Pin 17)
* CN8 Pin 6  (PB6) $\rightarrow$ Pico 2 GP14 (Pin 19)
* CN8 Pin 9  (PB7) $\rightarrow$ Pico 2 GP15 (Pin 20)
* CN8 Pin 3  (/RESTORE) $\rightarrow$ Pico 2 GP16 (Pin 21)

---

## 4. Flashing & Testing

1. Connect the Pico 2 to your PC via USB while holding the **BOOTSEL** button.
2. Drag and drop [`bin/c64_usb_keyboard_pico2.uf2`](file:///home/lucius/Priv/AGRAVITY/2026-10-c64-usb-keyboard/bin/c64_usb_keyboard_pico2.uf2) onto the `RP2350` drive.
3. Unplug from PC, plug the USB OTG cable into the Pico 2 micro-USB port, and connect your USB keyboard or wireless combo dongle.
4. Plug the ribbon cable into the C64 motherboard CN8 header.
5. Power on the Commodore 64: the adapter boots instantly and is ready for typing!
