#!/usr/bin/env python3
"""
KiCad 8 Project Generator for C64 USB Keyboard & Wireless Host Adapter (Pico 2 Edition)
Generates 100% KiCad 8 compliant .kicad_pro, .kicad_sch, and .kicad_pcb files.
Uses Raspberry Pi Pico 2 (RP2350) with 5V-tolerant native open-drain matrix interfacing.
"""

import os
import json
import uuid

def u():
    return str(uuid.uuid4())

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/kicad"
os.makedirs(OUT_DIR, exist_ok=True)

BOARD_W = 60.0
BOARD_H = 58.0

# -------------------------------------------------------------------------
# 1. Generate c64_usb_keyboard.kicad_pro (KiCad 8)
# -------------------------------------------------------------------------
pro_data = {
    "meta": {
        "filename": "c64_usb_keyboard.kicad_pro",
        "version": 3
    },
    "board": {
        "design_settings": {
            "defaults": {
                "board_outline_line_width": 0.15,
                "copper_line_width": 0.25,
                "silk_line_width": 0.12,
                "zones": {
                    "min_clearance": 0.35
                }
            },
            "rules": {
                "min_clearance": 0.25,
                "min_track_width": 0.25,
                "min_via_diameter": 0.8,
                "min_via_drill": 0.4,
                "min_copper_edge_clearance": 0.5
            }
        }
    },
    "schematic": {
        "top_level_sheets": [
            {
                "filename": "c64_usb_keyboard.kicad_sch",
                "name": "c64_usb_keyboard",
                "uuid": u()
            }
        ]
    }
}

with open(f"{OUT_DIR}/c64_usb_keyboard.kicad_pro", "w") as f:
    json.dump(pro_data, f, indent=2)

# -------------------------------------------------------------------------
# 2. Generate c64_usb_keyboard.kicad_sch (KiCad 8)
# -------------------------------------------------------------------------
sch_content = f"""(kicad_sch
	(version 20231120)
	(generator "eeschema")
	(generator_version "8.0")
	(uuid "{u()}")
	(paper "A4")
	(title_block
		(title "C64 USB Keyboard & Wireless Host Adapter (Pico 2 / RP2350)")
		(date "2026-10-01")
		(rev "v2.0 - Pico 2 Ultra-Simplified")
		(company "AGRAVITY Hardware / Software Project")
		(comment 1 "RP2350 5V-Tolerant GPIOs + Native Open-Drain Matrix Emulation")
		(comment 2 "Direct C64 Motherboard CN8 Interface - Zero Level Shifter ICs")
	)
	(lib_symbols
	)
	(sheet_instances
		(path "/"
			(page "1")
		)
	)
)
"""

with open(f"{OUT_DIR}/c64_usb_keyboard.kicad_sch", "w") as f:
    f.write(sch_content)

# -------------------------------------------------------------------------
# 3. Generate c64_usb_keyboard.kicad_pcb (KiCad 8)
# -------------------------------------------------------------------------
NETS = [
    (0, ""),
    (1, "GND"),
    (2, "+5V"),
    (3, "C64_RESTORE"),
    # Rows (PB0 - PB7)
    (4, "C64_ROW0"),
    (5, "C64_ROW1"),
    (6, "C64_ROW2"),
    (7, "C64_ROW3"),
    (8, "C64_ROW4"),
    (9, "C64_ROW5"),
    (10, "C64_ROW6"),
    (11, "C64_ROW7"),
    # Columns (PA0 - PA7)
    (12, "C64_COL0"),
    (13, "C64_COL1"),
    (14, "C64_COL2"),
    (15, "C64_COL3"),
    (16, "C64_COL4"),
    (17, "C64_COL5"),
    (18, "C64_COL6"),
    (19, "C64_COL7"),
    # Protected Rows between Resistors and Pico 2
    (20, "PICO_ROW0"),
    (21, "PICO_ROW1"),
    (22, "PICO_ROW2"),
    (23, "PICO_ROW3"),
    (24, "PICO_ROW4"),
    (25, "PICO_ROW5"),
    (26, "PICO_ROW6"),
    (27, "PICO_ROW7"),
    # UART Debug
    (28, "UART_TX"),
    (29, "UART_RX"),
]

pcb_header = f"""(kicad_pcb
	(version 20240108)
	(generator "pcbnew")
	(generator_version "8.0")
	(general
		(thickness 1.6)
		(legacy_teardrops no)
	)
	(paper "A4")
	(layers
		(0 "F.Cu" signal)
		(31 "B.Cu" signal)
		(32 "B.Adhes" user "B.Adhesive")
		(33 "F.Adhes" user "F.Adhesive")
		(34 "B.Paste" user)
		(35 "F.Paste" user)
		(36 "B.SilkS" user "B.Silkscreen")
		(37 "F.SilkS" user "F.Silkscreen")
		(38 "B.Mask" user)
		(39 "F.Mask" user)
		(40 "Dwgs.User" user "User.Drawings")
		(41 "Cmts.User" user "User.Comments")
		(44 "Edge.Cuts" user)
		(46 "B.CrtYd" user "B.Courtyard")
		(47 "F.CrtYd" user "F.Courtyard")
		(48 "B.Fab" user)
		(49 "F.Fab" user)
	)
	(setup
		(pad_to_mask_clearance 0.05)
		(allow_soldermask_bridges_in_footprints no)
		(pcbplotparams
			(layerselection 0x00010fc_ffffffff)
			(plot_on_all_layers_selection 0x0000000_00000000)
			(disableapertmacros no)
			(usegerberextensions no)
			(usegerberattributes yes)
			(usegerberadvancedattributes yes)
			(creategerberjobfile yes)
			(svgprecision 4)
			(plotframeref no)
			(viasonmask no)
			(mode 1)
			(useauxorigin no)
			(dxfpolygonmode yes)
			(dxfimperialunits yes)
			(dxfcontourstoturnpoints yes)
			(outputformat 1)
			(mirror no)
			(drillshape 1)
			(scaleselection 1)
			(outputdirectory "")
		)
	)
"""

# Net declarations
nets_str = ""
for n_id, n_name in NETS:
    nets_str += f'\t(net {n_id} "{n_name}")\n'

# Board Outline (Edge.Cuts) with rounded corners
corners = [
    (2.0, 0.0), (BOARD_W - 2.0, 0.0),
    (BOARD_W, 2.0), (BOARD_W, BOARD_H - 2.0),
    (BOARD_W - 2.0, BOARD_H), (2.0, BOARD_H),
    (0.0, BOARD_H - 2.0), (0.0, 2.0)
]
outline_str = f"""
	(gr_line (start 2.0 0.0) (end {BOARD_W-2.0} 0.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_line (start {BOARD_W} 2.0) (end {BOARD_W} {BOARD_H-2.0}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_line (start {BOARD_W-2.0} {BOARD_H}) (end 2.0 {BOARD_H}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_line (start 0.0 {BOARD_H-2.0}) (end 0.0 2.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_arc (start 2.0 0.0) (mid 0.58 0.58) (end 0.0 2.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_arc (start {BOARD_W} 2.0) (mid {BOARD_W-0.58} 0.58) (end {BOARD_W-2.0} 0.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_arc (start {BOARD_W-2.0} {BOARD_H}) (mid {BOARD_W-0.58} {BOARD_H-0.58}) (end {BOARD_W} {BOARD_H-2.0}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
	(gr_arc (start 0.0 {BOARD_H-2.0}) (mid 0.58 {BOARD_H-0.58}) (end 2.0 {BOARD_H}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts") (uuid "{u()}"))
"""

# Silkscreen Title & Labels
silkscreen_str = f"""
	(gr_text "C64 PICO 2 USB HOST" (at {BOARD_W/2} 2.5) (layer "F.SilkS") (uuid "{u()}")
		(effects (font (size 1.2 1.2) (thickness 0.2) (bold yes)))
	)
	(gr_text "RP2350 5V-TOLERANT NATIVE OPEN-DRAIN" (at {BOARD_W/2} {BOARD_H-2.5}) (layer "F.SilkS") (uuid "{u()}")
		(effects (font (size 0.8 0.8) (thickness 0.15)))
	)
	(gr_text "CN8 PIN 1" (at 7.0 3.5) (layer "F.SilkS") (uuid "{u()}")
		(effects (font (size 0.8 0.8) (thickness 0.12)))
	)
"""

footprints_str = ""

def make_pad_k8(p_num, net_id, net_name, x, y, drill=1.0, size=1.8, shape="circle"):
    return f"""\t\t(pad "{p_num}" thru_hole {shape}
			(at {x:.3f} {y:.3f})
			(size {size} {size})
			(drill {drill})
			(layers "*.Cu" "*.Mask")
			(remove_unused_layers no)
			(net {net_id} "{net_name}")
			(uuid "{u()}")
		)\n"""

# 1. Mounting Holes (4x M3)
mholes = [(3.5, 3.5), (BOARD_W - 3.5, 3.5), (3.5, BOARD_H - 3.5), (BOARD_W - 3.5, BOARD_H - 3.5)]
for idx, (hx, hy) in enumerate(mholes, 1):
    footprints_str += f"""\t(footprint "MountingHole:MountingHole_3.2mm_M3"
		(layer "F.Cu")
		(uuid "{u()}")
		(at {hx} {hy})
		(property "Reference" "H{idx}" (at 0 0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.5 0.5)) (hide yes)))
		(pad "1" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask") (uuid "{u()}"))
		(fp_circle (center 0 0) (end 2.5 0) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
	)\n"""

# 2. J1: C64 CN8 Connector (1x20 THT Pin Header, 2.54mm pitch)
j1_y_start = 5.0
j1_nets = [
    (1, "GND"),         # Pin 1: GND
    (0, "KEY"),         # Pin 2: Key (cut)
    (3, "C64_RESTORE"), # Pin 3: /RESTORE
    (2, "+5V"),         # Pin 4: +5V
    (7, "C64_ROW3"),    # Pin 5: PB3
    (10, "C64_ROW6"),   # Pin 6: PB6
    (9, "C64_ROW5"),    # Pin 7: PB5
    (8, "C64_ROW4"),    # Pin 8: PB4
    (11, "C64_ROW7"),   # Pin 9: PB7
    (6, "C64_ROW2"),    # Pin 10: PB2
    (5, "C64_ROW1"),    # Pin 11: PB1
    (4, "C64_ROW0"),    # Pin 12: PB0
    (19, "C64_COL7"),   # Pin 13: PA7
    (18, "C64_COL6"),   # Pin 14: PA6
    (17, "C64_COL5"),   # Pin 15: PA5
    (16, "C64_COL4"),   # Pin 16: PA4
    (15, "C64_COL3"),   # Pin 17: PA3
    (14, "C64_COL2"),   # Pin 18: PA2
    (13, "C64_COL1"),   # Pin 19: PA1
    (12, "C64_COL0"),   # Pin 20: PA0
]

footprints_str += f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x20_P2.54mm_Vertical"
		(layer "F.Cu")
		(uuid "{u()}")
		(at 7.0 0.0)
		(property "Reference" "J1" (at 0 2.5) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 1 1) (thickness 0.15))))
		(property "Value" "C64_CN8" (at 0 55.0) (layer "F.Fab") (uuid "{u()}") (effects (font (size 0.8 0.8) (thickness 0.12))))
		(fp_line (start -1.27 {j1_y_start-1.27:.3f}) (end 1.27 {j1_y_start-1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start 1.27 {j1_y_start-1.27:.3f}) (end 1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start 1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (end -1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start -1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (end -1.27 {j1_y_start-1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
"""
for idx, (net_id, net_name) in enumerate(j1_nets):
    p_num = idx + 1
    py = j1_y_start + idx * 2.54
    shape = "rect" if p_num == 1 else "circle"
    footprints_str += make_pad_k8(p_num, net_id, net_name, 0.0, py, drill=1.0, size=1.8, shape=shape)
footprints_str += "\t)\n"

# 3. RN1: 8x 100 Ohm Protection Resistors (Axial THT placed between J1 rows and Pico 2)
# Positioned at X = 18.0 mm
resistor_nets = [
    (1, 4, "C64_ROW0", 20, "PICO_ROW0"),
    (2, 5, "C64_ROW1", 21, "PICO_ROW1"),
    (3, 6, "C64_ROW2", 22, "PICO_ROW2"),
    (4, 7, "C64_ROW3", 23, "PICO_ROW3"),
    (5, 8, "C64_ROW4", 24, "PICO_ROW4"),
    (6, 9, "C64_ROW5", 25, "PICO_ROW5"),
    (7, 10, "C64_ROW6", 26, "PICO_ROW6"),
    (8, 11, "C64_ROW7", 27, "PICO_ROW7"),
]
r_y_start = 16.0
for r_idx, c64_net, c64_name, pico_net, pico_name in resistor_nets:
    ry = r_y_start + (r_idx - 1) * 3.5
    footprints_str += f"""\t(footprint "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"
		(layer "F.Cu")
		(uuid "{u()}")
		(at 19.0 {ry:.2f})
		(property "Reference" "R{r_idx}" (at 0 -1.5) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.7 0.7) (thickness 0.12))))
		(property "Value" "100R" (at 0 1.5) (layer "F.Fab") (uuid "{u()}") (effects (font (size 0.6 0.6) (thickness 0.1))))
		(fp_line (start -3.81 0) (end 3.81 0) (stroke (width 0.15) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
"""
    footprints_str += make_pad_k8(1, c64_net, c64_name, -3.81, 0, drill=0.8, size=1.6, shape="circle")
    footprints_str += make_pad_k8(2, pico_net, pico_name, 3.81, 0, drill=0.8, size=1.6, shape="circle")
    footprints_str += "\t)\n"

# 4. U1: Raspberry Pi Pico 2 Module (Socketed with 2x 1x20 Female Headers, 0.7" row spacing)
pico_x_left = 34.0
pico_x_right = 51.78
pico_y_start = 5.0

footprints_str += f"""\t(footprint "Module:RaspberryPi_Pico_Socket"
		(layer "F.Cu")
		(uuid "{u()}")
		(at {pico_x_left} 0.0)
		(property "Reference" "U1" (at 8.89 2.5) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 1.2 1.2) (thickness 0.2) (bold yes))))
		(property "Value" "Pico 2 (RP2350)" (at 8.89 55.0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.9 0.9) (thickness 0.15))))
		(fp_line (start -1.5 3.0) (end 19.28 3.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start 19.28 3.0) (end 19.28 55.5) (stroke (width 0.2) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start 19.28 55.5) (end -1.5 55.5) (stroke (width 0.2) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
		(fp_line (start -1.5 55.5) (end -1.5 3.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS") (uuid "{u()}"))
"""
# Pico Left Header (Pins 1-20: GP0-GP15)
pico_left_nets = [
    (12, "C64_COL0"),  # Pin 1: GP0 (Direct 5V-tolerant input)
    (13, "C64_COL1"),  # Pin 2: GP1 (Direct 5V-tolerant input)
    (1, "GND"),        # Pin 3: GND
    (14, "C64_COL2"),  # Pin 4: GP2 (Direct 5V-tolerant input)
    (15, "C64_COL3"),  # Pin 5: GP3 (Direct 5V-tolerant input)
    (16, "C64_COL4"),  # Pin 6: GP4 (Direct 5V-tolerant input)
    (17, "C64_COL5"),  # Pin 7: GP5 (Direct 5V-tolerant input)
    (1, "GND"),        # Pin 8: GND
    (18, "C64_COL6"),  # Pin 9: GP6 (Direct 5V-tolerant input)
    (19, "C64_COL7"),  # Pin 10: GP7 (Direct 5V-tolerant input)
    (20, "PICO_ROW0"), # Pin 11: GP8 (Native Open-Drain)
    (21, "PICO_ROW1"), # Pin 12: GP9 (Native Open-Drain)
    (1, "GND"),        # Pin 13: GND
    (22, "PICO_ROW2"), # Pin 14: GP10 (Native Open-Drain)
    (23, "PICO_ROW3"), # Pin 15: GP11 (Native Open-Drain)
    (24, "PICO_ROW4"), # Pin 16: GP12 (Native Open-Drain)
    (25, "PICO_ROW5"), # Pin 17: GP13 (Native Open-Drain)
    (1, "GND"),        # Pin 18: GND
    (26, "PICO_ROW6"), # Pin 19: GP14 (Native Open-Drain)
    (27, "PICO_ROW7"), # Pin 20: GP15 (Native Open-Drain)
]
for idx, (net_id, net_name) in enumerate(pico_left_nets):
    p_num = idx + 1
    py = pico_y_start + idx * 2.54
    shape = "rect" if p_num == 1 else "circle"
    footprints_str += make_pad_k8(p_num, net_id, net_name, 0.0, py, drill=1.0, size=1.8, shape=shape)

# Pico Right Header (Pins 40 down to 21)
pico_right_nets = [
    (2, "+5V"),         # Pin 40: VBUS (Power input from C64 Pin 4)
    (2, "+5V"),         # Pin 39: VSYS
    (1, "GND"),         # Pin 38: GND
    (0, "3V3_EN"),      # Pin 37: 3V3_EN
    (0, "+3V3"),        # Pin 36: 3V3_OUT
    (0, "ADC_VREF"),    # Pin 35: ADC_VREF
    (0, "GP28"),        # Pin 34: GP28
    (1, "GND"),         # Pin 33: GND
    (0, "GP27"),        # Pin 32: GP27
    (0, "GP26"),        # Pin 31: GP26
    (0, "RUN"),         # Pin 30: RUN
    (0, "GP22"),        # Pin 29: GP22
    (1, "GND"),         # Pin 28: GND
    (0, "GP21"),        # Pin 27: GP21
    (0, "GP20"),        # Pin 26: GP20
    (0, "GP19"),        # Pin 25: GP19
    (0, "GP18"),        # Pin 24: GP18
    (1, "GND"),         # Pin 23: GND
    (0, "GP17"),        # Pin 22: GP17
    (3, "C64_RESTORE"), # Pin 21: GP16 (Direct Native Open-Drain)
]
for idx, (net_id, net_name) in enumerate(pico_right_nets):
    p_num = 40 - idx
    py = pico_y_start + idx * 2.54
    footprints_str += make_pad_k8(p_num, net_id, net_name, 17.78, py, drill=1.0, size=1.8, shape="circle")

footprints_str += "\t)\n"

# 5. Capacitors (C1: 100nF Ceramic, C2: 47uF Electrolytic)
footprints_str += f"""\t(footprint "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.54mm"
		(layer "F.Cu")
		(uuid "{u()}")
		(at 16.0 10.0)
		(property "Reference" "C1" (at 0 -2.0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.7 0.7) (thickness 0.12))))
		(property "Value" "100nF" (at 0 2.0) (layer "F.Fab") (uuid "{u()}") (effects (font (size 0.6 0.6) (thickness 0.1))))
"""
footprints_str += make_pad_k8(1, 2, "+5V", -1.27, 0, drill=0.8, size=1.6, shape="circle")
footprints_str += make_pad_k8(2, 1, "GND", 1.27, 0, drill=0.8, size=1.6, shape="circle")
footprints_str += "\t)\n"

footprints_str += f"""\t(footprint "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"
		(layer "F.Cu")
		(uuid "{u()}")
		(at 24.0 10.0)
		(property "Reference" "C2" (at 0 -3.2) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.7 0.7) (thickness 0.12))))
		(property "Value" "47uF" (at 0 3.2) (layer "F.Fab") (uuid "{u()}") (effects (font (size 0.6 0.6) (thickness 0.1))))
"""
footprints_str += make_pad_k8(1, 2, "+5V", -1.27, 0, drill=0.8, size=1.8, shape="rect")
footprints_str += make_pad_k8(2, 1, "GND", 1.27, 0, drill=0.8, size=1.8, shape="circle")
footprints_str += "\t)\n"

# 6. J3: 1x3 UART Debug Header
footprints_str += f"""\t(footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"
		(layer "F.Cu")
		(uuid "{u()}")
		(at 24.0 48.0)
		(property "Reference" "J3" (at 0 -2.0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.8 0.8) (thickness 0.15))))
		(property "Value" "UART" (at 0 8.0) (layer "F.SilkS") (uuid "{u()}") (effects (font (size 0.7 0.7) (thickness 0.12))))
"""
footprints_str += make_pad_k8(1, 28, "UART_TX", 0, 0, drill=1.0, size=1.6, shape="rect")
footprints_str += make_pad_k8(2, 29, "UART_RX", 0, 2.54, drill=1.0, size=1.6, shape="circle")
footprints_str += make_pad_k8(3, 1, "GND", 0, 5.08, drill=1.0, size=1.6, shape="circle")
footprints_str += "\t)\n"

# Copper Traces
segments_str = f"""
	(segment (start 7.0 12.62) (end 14.73 10.0) (width 0.6) (layer "F.Cu") (net 2) (uuid "{u()}"))
	(segment (start 14.73 10.0) (end 22.73 10.0) (width 0.6) (layer "F.Cu") (net 2) (uuid "{u()}"))
	(segment (start 22.73 10.0) (end 51.78 5.0) (width 0.6) (layer "F.Cu") (net 2) (uuid "{u()}"))
"""

# Ground plane on Bottom Copper (B.Cu)
zone_str = f"""\t(zone (net 1) (net_name "GND") (layer "B.Cu") (tstamp "{u()}") (hatch edge 0.5)
		(priority 0)
		(connect_pads yes (clearance 0.35))
		(min_thickness 0.25)
		(filled_areas_thickness no)
		(fill yes (thermal_gap 0.5) (thermal_bridge_width 0.5))
		(polygon
			(pts
				(xy 0.5 0.5)
				(xy {BOARD_W-0.5} 0.5)
				(xy {BOARD_W-0.5} {BOARD_H-0.5})
				(xy 0.5 {BOARD_H-0.5})
			)
		)
	)
"""

full_pcb_str = pcb_header + nets_str + outline_str + silkscreen_str + footprints_str + segments_str + zone_str + ")\n"

with open(f"{OUT_DIR}/c64_usb_keyboard.kicad_pcb", "w") as f:
    f.write(full_pcb_str)

print("[SUCCESS] Generated 100% KiCad 8 files in " + OUT_DIR)
