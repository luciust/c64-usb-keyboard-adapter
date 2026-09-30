#!/usr/bin/env python3
"""
KiCad Project Generator for C64 USB Keyboard & Wireless Host Adapter
Generates .kicad_pro, .kicad_sch, and .kicad_pcb using 100% DIP and THT components.
"""

import os
import json
import uuid

def gen_uuid():
    return str(uuid.uuid4())

OUT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/kicad"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. Generate c64_usb_keyboard.kicad_pro
# -------------------------------------------------------------------------
pro_data = {
    "meta": {
        "filename": "c64_usb_keyboard.kicad_pro",
        "version": 3
    },
    "board": {
        "design_settings": {
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
                "uuid": gen_uuid()
            }
        ]
    }
}

with open(f"{OUT_DIR}/c64_usb_keyboard.kicad_pro", "w") as f:
    json.dump(pro_data, f, indent=2)

# -------------------------------------------------------------------------
# 2. Generate c64_usb_keyboard.kicad_sch
# -------------------------------------------------------------------------
sch_content = f"""(kicad_sch
  (version 20230121)
  (generator "eeschema")
  (generator_version "7.0")
  (uuid "{gen_uuid()}")
  (paper "A4")
  (title_block
    (title "C64 USB Keyboard & Wireless Host Adapter (DIP/THT)")
    (date "2026-09-30")
    (rev "v1.0")
    (company "AGRAVITY Hardware / Software Project")
    (comment 1 "Raspberry Pi Pico + 74HCT245 + BAT42 Schottky + Voltage Dividers")
    (comment 2 "100% DIP and THT Construction - C64 CN8 Connector")
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
# 3. Generate c64_usb_keyboard.kicad_pcb
# -------------------------------------------------------------------------
BOARD_W = 85.0
BOARD_H = 55.0

# Net definitions
NETS = [
    (0, ""),
    (1, "GND"),
    (2, "+5V"),
    (3, "+3V3"),
    (4, "C64_RESTORE"),
    # Rows
    (5, "C64_ROW0"),
    (6, "C64_ROW1"),
    (7, "C64_ROW2"),
    (8, "C64_ROW3"),
    (9, "C64_ROW4"),
    (10, "C64_ROW5"),
    (11, "C64_ROW6"),
    (12, "C64_ROW7"),
    # Cols (5V/4V from C64)
    (13, "C64_COL0"),
    (14, "C64_COL1"),
    (15, "C64_COL2"),
    (16, "C64_COL3"),
    (17, "C64_COL4"),
    (18, "C64_COL5"),
    (19, "C64_COL6"),
    (20, "C64_COL7"),
    # Cols (3.3V to Pico)
    (21, "PICO_COL0"),
    (22, "PICO_COL1"),
    (23, "PICO_COL2"),
    (24, "PICO_COL3"),
    (25, "PICO_COL4"),
    (26, "PICO_COL5"),
    (27, "PICO_COL6"),
    (28, "PICO_COL7"),
    # Rows (from Pico to 74HCT245)
    (29, "PICO_ROW0"),
    (30, "PICO_ROW1"),
    (31, "PICO_ROW2"),
    (32, "PICO_ROW3"),
    (33, "PICO_ROW4"),
    (34, "PICO_ROW5"),
    (35, "PICO_ROW6"),
    (36, "PICO_ROW7"),
    # 74HCT245 outputs to Diode cathodes
    (37, "DRV_ROW0"),
    (38, "DRV_ROW1"),
    (39, "DRV_ROW2"),
    (40, "DRV_ROW3"),
    (41, "DRV_ROW4"),
    (42, "DRV_ROW5"),
    (43, "DRV_ROW6"),
    (44, "DRV_ROW7"),
    # USB D+/D-
    (45, "USB_DP"),
    (46, "USB_DM"),
    (47, "UART_TX"),
    (48, "UART_RX"),
]

pcb_header = f"""(kicad_pcb
  (version 20221018)
  (generator "pcbnew")
  (generator_version "7.0")
  (general
    (thickness 1.6)
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
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (plot_on_all_layers_selection 0x0000000_00000000)
      (disableapertmacros false)
      (usegerberextensions false)
      (usegerberattributes true)
      (usegerberadvancedattributes true)
      (creategerberjobfile true)
      (dashed_line_dash_ratio 12.000000)
      (dashed_line_gap_ratio 3.000000)
      (svgprecision 4)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (dxfpolygonmode true)
      (dxfimperialunits true)
      (dxfcontourstoturnpoints true)
      (outputformat 1)
      (mirror false)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory "")
    )
  )
"""

# Append nets
nets_str = ""
for n_id, n_name in NETS:
    nets_str += f'  (net {n_id} "{n_name}")\n'

# Board Outline (Edge.Cuts) with rounded corners
corners = [
    (2.0, 0.0), (BOARD_W - 2.0, 0.0),
    (BOARD_W, 2.0), (BOARD_W, BOARD_H - 2.0),
    (BOARD_W - 2.0, BOARD_H), (2.0, BOARD_H),
    (0.0, BOARD_H - 2.0), (0.0, 2.0)
]
outline_str = f"""
  (gr_line (start 2.0 0.0) (end {BOARD_W-2.0} 0.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_line (start {BOARD_W} 2.0) (end {BOARD_W} {BOARD_H-2.0}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_line (start {BOARD_W-2.0} {BOARD_H}) (end 2.0 {BOARD_H}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_line (start 0.0 {BOARD_H-2.0}) (end 0.0 2.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_arc (start 2.0 0.0) (mid 0.58 0.58) (end 0.0 2.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_arc (start {BOARD_W} 2.0) (mid {BOARD_W-0.58} 0.58) (end {BOARD_W-2.0} 0.0) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_arc (start {BOARD_W-2.0} {BOARD_H}) (mid {BOARD_W-0.58} {BOARD_H-0.58}) (end {BOARD_W} {BOARD_H-2.0}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
  (gr_arc (start 0.0 {BOARD_H-2.0}) (mid 0.58 {BOARD_H-0.58}) (end 2.0 {BOARD_H}) (stroke (width 0.15) (type solid)) (layer "Edge.Cuts"))
"""

# Silkscreen text
silkscreen_str = f"""
  (gr_text "C64 USB KEYBOARD & WIRELESS HOST" (at 42.5 2.5) (layer "F.SilkS")
    (effects (font (size 1.2 1.2) (thickness 0.2) (bold true)))
  )
  (gr_text "100% DIP & THT ADAPTER - PICO RP2040" (at 42.5 52.5) (layer "F.SilkS")
    (effects (font (size 1.0 1.0) (thickness 0.18)))
  )
  (gr_text "C64 CN8" (at 7.0 4.0) (layer "F.SilkS")
    (effects (font (size 1.0 1.0) (thickness 0.15)))
  )
  (gr_text "PIN 1 (GND)" (at 12.0 6.5) (layer "F.SilkS")
    (effects (font (size 0.8 0.8) (thickness 0.12)))
  )
"""

# Footprints helper
footprints_str = ""

def make_pad(p_num, net_id, net_name, x, y, drill=1.0, size=1.8, shape="rect"):
    return f'    (pad "{p_num}" thru_hole {shape} (at {x:.3f} {y:.3f}) (size {size} {size}) (drill {drill}) (layers "*.Cu" "*.Mask") (net {net_id} "{net_name}"))\n'

# 1. Mounting Holes (4x M3)
mholes = [(4.0, 4.0), (BOARD_W - 4.0, 4.0), (4.0, BOARD_H - 4.0), (BOARD_W - 4.0, BOARD_H - 4.0)]
for i, (hx, hy) in enumerate(mholes, 1):
    footprints_str += f"""  (footprint "MountingHole:MountingHole_3.2mm_M3" (layer "F.Cu")
    (at {hx} {hy})
    (pad "1" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask"))
    (fp_circle (center 0 0) (end 3.0 0) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
  )\n"""

# 2. J1: C64 CN8 Connector (1x20 THT Pin Header, 2.54mm pitch)
j1_y_start = 6.5
j1_nets = [
    (1, "GND"),         # Pin 1: GND
    (0, "KEY"),         # Pin 2: Key (cut)
    (4, "C64_RESTORE"), # Pin 3: /RESTORE
    (2, "+5V"),         # Pin 4: +5V
    (8, "C64_ROW3"),    # Pin 5: PB3
    (11, "C64_ROW6"),   # Pin 6: PB6
    (10, "C64_ROW5"),   # Pin 7: PB5
    (9, "C64_ROW4"),    # Pin 8: PB4
    (12, "C64_ROW7"),   # Pin 9: PB7
    (7, "C64_ROW2"),    # Pin 10: PB2
    (6, "C64_ROW1"),    # Pin 11: PB1
    (5, "C64_ROW0"),    # Pin 12: PB0
    (20, "C64_COL7"),   # Pin 13: PA7
    (19, "C64_COL6"),   # Pin 14: PA6
    (18, "C64_COL5"),   # Pin 15: PA5
    (17, "C64_COL4"),   # Pin 16: PA4
    (16, "C64_COL3"),   # Pin 17: PA3
    (15, "C64_COL2"),   # Pin 18: PA2
    (14, "C64_COL1"),   # Pin 19: PA1
    (13, "C64_COL0"),   # Pin 20: PA0
]

footprints_str += f"""  (footprint "Connector_PinHeader_2.54mm:PinHeader_1x20_P2.54mm_Vertical" (layer "F.Cu")
    (at 7.0 0.0)
    (fp_text reference "J1" (at 0 4.0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_line (start -1.27 {j1_y_start-1.27:.3f}) (end 1.27 {j1_y_start-1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start 1.27 {j1_y_start-1.27:.3f}) (end 1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start 1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (end -1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start -1.27 {j1_y_start + 19*2.54 + 1.27:.3f}) (end -1.27 {j1_y_start-1.27:.3f}) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
"""
for idx, (net_id, net_name) in enumerate(j1_nets):
    p_num = idx + 1
    py = j1_y_start + idx * 2.54
    shape = "rect" if p_num == 1 else "circle"
    footprints_str += make_pad(p_num, net_id, net_name, 0.0, py, drill=1.0, size=1.8, shape=shape)
footprints_str += "  )\n"

# 3. U2: 74HCT245 (DIP-20 Socket, 0.3" pitch)
u2_cx = 28.0
u2_cy = 28.0
footprints_str += f"""  (footprint "Package_DIP:DIP-20_W7.62mm_Socket" (layer "F.Cu")
    (at {u2_cx} {u2_cy})
    (fp_text reference "U2" (at 0 -13.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text value "74HCT245" (at 0 13.5) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -4.5 -12.5) (end 4.5 -12.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start 4.5 -12.5) (end 4.5 12.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start 4.5 12.5) (end -4.5 12.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start -4.5 12.5) (end -4.5 -12.5) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
"""
# Left pins 1-10 (x = -3.81), Right pins 20-11 (x = +3.81)
u2_pin_nets = {
    1: (2, "+5V"),          # DIR -> +5V
    2: (29, "PICO_ROW0"),   # A1
    3: (30, "PICO_ROW1"),   # A2
    4: (31, "PICO_ROW2"),   # A3
    5: (32, "PICO_ROW3"),   # A4
    6: (33, "PICO_ROW4"),   # A5
    7: (34, "PICO_ROW5"),   # A6
    8: (35, "PICO_ROW6"),   # A7
    9: (36, "PICO_ROW7"),   # A8
    10: (1, "GND"),         # GND
    11: (44, "DRV_ROW7"),   # B8
    12: (43, "DRV_ROW6"),   # B7
    13: (42, "DRV_ROW5"),   # B6
    14: (41, "DRV_ROW4"),   # B5
    15: (40, "DRV_ROW3"),   # B4
    16: (39, "DRV_ROW2"),   # B3
    17: (38, "DRV_ROW1"),   # B2
    18: (37, "DRV_ROW0"),   # B1
    19: (1, "GND"),         # /OE -> GND
    20: (2, "+5V"),         # VCC -> +5V
}
for p in range(1, 11):
    py = -11.43 + (p - 1) * 2.54
    net_id, net_name = u2_pin_nets[p]
    shape = "rect" if p == 1 else "circle"
    footprints_str += make_pad(p, net_id, net_name, -3.81, py, drill=0.8, size=1.6, shape=shape)

for p in range(11, 21):
    py = 11.43 - (p - 11) * 2.54
    net_id, net_name = u2_pin_nets[p]
    footprints_str += make_pad(p, net_id, net_name, 3.81, py, drill=0.8, size=1.6, shape="circle")

footprints_str += "  )\n"

# 4. D1 - D8: BAT42 Schottky Diodes (DO-35 Axial THT)
# Placed between U2 and J1 at X = 18.0
diode_nets = [
    (1, 5, "C64_ROW0", 37, "DRV_ROW0"),
    (2, 6, "C64_ROW1", 38, "DRV_ROW1"),
    (3, 7, "C64_ROW2", 39, "DRV_ROW2"),
    (4, 8, "C64_ROW3", 40, "DRV_ROW3"),
    (5, 9, "C64_ROW4", 41, "DRV_ROW4"),
    (6, 10, "C64_ROW5", 42, "DRV_ROW5"),
    (7, 11, "C64_ROW6", 43, "DRV_ROW6"),
    (8, 12, "C64_ROW7", 44, "DRV_ROW7"),
]
d_y_start = 18.0
for d_idx, a_net_id, a_net_name, k_net_id, k_net_name in diode_nets:
    dy = d_y_start + (d_idx - 1) * 3.2
    footprints_str += f"""  (footprint "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" (layer "F.Cu")
    (at 18.0 {dy:.2f})
    (fp_text reference "D{d_idx}" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12))))
    (fp_line (start -1.5 0) (end 1.5 0) (stroke (width 0.15) (type solid)) (layer "F.SilkS"))
    (fp_line (start 1.0 -0.8) (end 1.0 0.8) (stroke (width 0.2) (type solid)) (layer "F.SilkS"))
"""
    # Pad 1: Anode (x = -3.81), Pad 2: Cathode (x = +3.81)
    footprints_str += make_pad(1, a_net_id, a_net_name, -3.81, 0, drill=0.8, size=1.6, shape="circle")
    footprints_str += make_pad(2, k_net_id, k_net_name, 3.81, 0, drill=0.8, size=1.6, shape="rect")
    footprints_str += "  )\n"

# 5. R1 - R8 (1.8k upper) and R9 - R16 (3.3k lower) Resistor Dividers
# Upper resistors at X = 39.0, Lower at X = 49.0
r_y_start = 12.0
for i in range(8):
    ry = r_y_start + i * 3.5
    c64_col_net_id = 13 + i
    c64_col_net_name = f"C64_COL{i}"
    pico_col_net_id = 21 + i
    pico_col_net_name = f"PICO_COL{i}"

    # Upper Resistor R1-R8 (Series: C64_COL -> PICO_COL)
    r_up_num = i + 1
    footprints_str += f"""  (footprint "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" (layer "F.Cu")
    (at 39.0 {ry:.2f})
    (fp_text reference "R{r_up_num}" (at 0 -1.4) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))
"""
    footprints_str += make_pad(1, c64_col_net_id, c64_col_net_name, -3.81, 0, drill=0.8, size=1.5, shape="circle")
    footprints_str += make_pad(2, pico_col_net_id, pico_col_net_name, 3.81, 0, drill=0.8, size=1.5, shape="circle")
    footprints_str += "  )\n"

    # Lower Resistor R9-R16 (Pull-down: PICO_COL -> GND)
    r_dn_num = i + 9
    footprints_str += f"""  (footprint "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" (layer "F.Cu")
    (at 49.0 {ry:.2f})
    (fp_text reference "R{r_dn_num}" (at 0 -1.4) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))
"""
    footprints_str += make_pad(1, pico_col_net_id, pico_col_net_name, -3.81, 0, drill=0.8, size=1.5, shape="circle")
    footprints_str += make_pad(2, 1, "GND", 3.81, 0, drill=0.8, size=1.5, shape="circle")
    footprints_str += "  )\n"

# 6. U1: Raspberry Pi Pico (2x 1x20 Female Headers, Spacing 17.78mm / 0.7")
pico_x_left = 61.0
pico_x_right = 78.78
pico_y_start = 5.5

footprints_str += f"""  (footprint "Module:RaspberryPi_Pico_Socket" (layer "F.Cu")
    (at {pico_x_left} 0.0)
    (fp_text reference "U1" (at 8.89 2.5) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.2) (bold true))))
    (fp_text value "Raspberry Pi Pico" (at 8.89 53.0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_line (start -1.5 3.0) (end 19.28 3.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS"))
    (fp_line (start 19.28 3.0) (end 19.28 54.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS"))
    (fp_line (start 19.28 54.0) (end -1.5 54.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS"))
    (fp_line (start -1.5 54.0) (end -1.5 3.0) (stroke (width 0.2) (type solid)) (layer "F.SilkS"))
"""
# Pico Left Header (Pins 1-20)
pico_left_nets = [
    (21, "PICO_COL0"),  # Pin 1: GP0
    (22, "PICO_COL1"),  # Pin 2: GP1
    (1, "GND"),         # Pin 3: GND
    (23, "PICO_COL2"),  # Pin 4: GP2
    (24, "PICO_COL3"),  # Pin 5: GP3
    (25, "PICO_COL4"),  # Pin 6: GP4
    (26, "PICO_COL5"),  # Pin 7: GP5
    (1, "GND"),         # Pin 8: GND
    (27, "PICO_COL6"),  # Pin 9: GP6
    (28, "PICO_COL7"),  # Pin 10: GP7
    (29, "PICO_ROW0"),  # Pin 11: GP8
    (30, "PICO_ROW1"),  # Pin 12: GP9
    (1, "GND"),         # Pin 13: GND
    (31, "PICO_ROW2"),  # Pin 14: GP10
    (32, "PICO_ROW3"),  # Pin 15: GP11
    (33, "PICO_ROW4"),  # Pin 16: GP12
    (34, "PICO_ROW5"),  # Pin 17: GP13
    (1, "GND"),         # Pin 18: GND
    (35, "PICO_ROW6"),  # Pin 19: GP14
    (36, "PICO_ROW7"),  # Pin 20: GP15
]
for idx, (net_id, net_name) in enumerate(pico_left_nets):
    p_num = idx + 1
    py = pico_y_start + idx * 2.54
    shape = "rect" if p_num == 1 else "circle"
    footprints_str += make_pad(p_num, net_id, net_name, 0.0, py, drill=1.0, size=1.8, shape=shape)

# Pico Right Header (Pins 40 down to 21)
pico_right_nets = [
    (2, "+5V"),         # Pin 40: VBUS
    (2, "+5V"),         # Pin 39: VSYS
    (1, "GND"),         # Pin 38: GND
    (0, "3V3_EN"),      # Pin 37: 3V3_EN
    (3, "+3V3"),        # Pin 36: 3V3_OUT
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
    (4, "C64_RESTORE"), # Pin 21: GP16 (RESTORE)
]
for idx, (net_id, net_name) in enumerate(pico_right_nets):
    p_num = 40 - idx
    py = pico_y_start + idx * 2.54
    footprints_str += make_pad(p_num, net_id, net_name, 17.78, py, drill=1.0, size=1.8, shape="circle")

footprints_str += "  )\n"

# 7. Q1: 2N7000 (TO-92 THT) RESTORE transistor
footprints_str += f"""  (footprint "Package_TO_SOT_THT:TO-92_Inline" (layer "F.Cu")
    (at 15.0 12.0)
    (fp_text reference "Q1" (at 0 -2.0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12))))
    (pad "1" thru_hole circle (at -1.27 0) (size 1.4 1.4) (drill 0.8) (layers "*.Cu" "*.Mask") (net 1 "GND"))
    (pad "2" thru_hole circle (at 0 0) (size 1.4 1.4) (drill 0.8) (layers "*.Cu" "*.Mask") (net 4 "C64_RESTORE"))
    (pad "3" thru_hole circle (at 1.27 0) (size 1.4 1.4) (drill 0.8) (layers "*.Cu" "*.Mask") (net 4 "C64_RESTORE"))
  )\n"""

# 8. Decoupling Caps (C1, C2, C3)
footprints_str += f"""  (footprint "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.54mm" (layer "F.Cu")
    (at 28.0 13.5)
    (fp_text reference "C1" (at 0 -2.0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12))))
    (pad "1" thru_hole circle (at -1.27 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 2 "+5V"))
    (pad "2" thru_hole circle (at 1.27 0) (size 1.6 1.6) (drill 0.8) (layers "*.Cu" "*.Mask") (net 1 "GND"))
  )\n"""

footprints_str += f"""  (footprint "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" (layer "F.Cu")
    (at 14.0 46.0)
    (fp_text reference "C3" (at 0 -3.5) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))
    (pad "1" thru_hole rect (at -1.27 0) (size 1.8 1.8) (drill 0.8) (layers "*.Cu" "*.Mask") (net 2 "+5V"))
    (pad "2" thru_hole circle (at 1.27 0) (size 1.8 1.8) (drill 0.8) (layers "*.Cu" "*.Mask") (net 1 "GND"))
  )\n"""

# 9. J3: UART Debug Header (1x3 2.54mm THT)
footprints_str += f"""  (footprint "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" (layer "F.Cu")
    (at 49.0 47.0)
    (fp_text reference "J3" (at 0 -2.0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))
    (fp_text value "UART DEBUG" (at 0 8.0) (layer "F.SilkS") (effects (font (size 0.7 0.7) (thickness 0.12))))
    (pad "1" thru_hole rect (at 0 0) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 47 "UART_TX"))
    (pad "2" thru_hole circle (at 0 2.54) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 48 "UART_RX"))
    (pad "3" thru_hole circle (at 0 5.08) (size 1.6 1.6) (drill 1.0) (layers "*.Cu" "*.Mask") (net 1 "GND"))
  )\n"""

# Traces / Segments (Key power and signal routes)
segments_str = f"""
  (segment (start 7.0 14.12) (end 12.73 14.12) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 12.73 14.12) (end 12.73 46.0) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 12.73 46.0) (end 18.0 46.0) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 18.0 46.0) (end 24.19 28.0) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 24.19 28.0) (end 31.81 16.57) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 31.81 16.57) (end 31.81 13.5) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 31.81 13.5) (end 26.73 13.5) (width 0.6) (layer "F.Cu") (net 2))
  (segment (start 31.81 13.5) (end 78.78 5.5) (width 0.6) (layer "F.Cu") (net 2))
"""

# Ground plane zone on B.Cu
zone_str = f"""  (zone (net 1) (net_name "GND") (layer "B.Cu") (tstamp "{gen_uuid()}") (hatch edge 0.5)
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

print("[SUCCESS] KiCad project generated:")
print(f"  - {OUT_DIR}/c64_usb_keyboard.kicad_pro")
print(f"  - {OUT_DIR}/c64_usb_keyboard.kicad_sch")
print(f"  - {OUT_DIR}/c64_usb_keyboard.kicad_pcb")
