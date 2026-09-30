#ifndef KEYMAP_H
#define KEYMAP_H

#include <stdint.h>
#include <stdbool.h>
#include "c64_matrix.h"

#ifdef __cplusplus
extern "C" {
#endif

// Keymap flags
#define KEYMAP_FLAG_NONE        0x00
#define KEYMAP_FLAG_RESTORE     0x01   // Triggers RESTORE line (NMI)
#define KEYMAP_FLAG_AUTO_SHIFT  0x02   // Automatically asserts C64 Left Shift (e.g. CRSR UP, CRSR LEFT, F2, F4, F6, F8)

typedef struct {
    uint8_t row;
    uint8_t col;
    uint8_t flags;
} c64_key_mapping_t;

// C64 Standard Modifier matrix coordinates
// Left Shift: Row 1, Col 7
#define C64_ROW_LSHIFT          1
#define C64_COL_LSHIFT          7

// Right Shift: Row 6, Col 4
#define C64_ROW_RSHIFT          6
#define C64_COL_RSHIFT          4

// Commodore Key (C=): Row 7, Col 5
#define C64_ROW_COMMODORE       7
#define C64_COL_COMMODORE       5

// CTRL Key: Row 7, Col 2
#define C64_ROW_CTRL            7
#define C64_COL_CTRL            2

// RUN/STOP Key: Row 7, Col 7
#define C64_ROW_RUNSTOP         7
#define C64_COL_RUNSTOP         7

// Lookup function for USB HID keycode (Usage Page 0x07)
c64_key_mapping_t keymap_get_c64_key(uint8_t hid_code);

#ifdef __cplusplus
}
#endif

#endif // KEYMAP_H
