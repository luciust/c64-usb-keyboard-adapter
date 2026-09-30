#ifndef C64_MATRIX_H
#define C64_MATRIX_H

#include <stdint.h>
#include <stdbool.h>
#include "pico/stdlib.h"

#ifdef __cplusplus
extern "C" {
#endif

//--------------------------------------------------------------------
// GPIO PIN DEFINITIONS
//--------------------------------------------------------------------

// C64 Columns (Inputs to Pico via 1.8k/3.3k resistor dividers)
// C64 CIA 1 Port A (PA0 - PA7)
#define C64_COL_BASE_PIN        0       // GP0 - GP7 (Cols 0-7)
#define C64_COL_MASK            0x000000FF

// C64 Rows (Outputs to 74HCT245 -> Schottky Diodes -> C64 PB0 - PB7)
// C64 CIA 1 Port B (PB0 - PB7)
#define C64_ROW_BASE_PIN        8       // GP8 - GP15 (Rows 0-7)
#define C64_ROW_MASK            0x0000FF00

// C64 RESTORE Key (Pin 3 of CN8, active low to NMI)
// Output to gate of 2N7000 / base of 2N3904 open-drain transistor
#define C64_RESTORE_PIN         16

// Status LED (Onboard Pico LED)
#define STATUS_LED_PIN          25

// Matrix dimensions
#define C64_MATRIX_ROWS         8
#define C64_MATRIX_COLS         8

// Special values
#define C64_KEY_NONE            0xFF

// Debounce / Minimum contact hold time in microseconds
// C64 KERNAL scans keyboard every 16.6ms (NTSC) or 20ms (PAL)
// A minimum hold time of 35ms ensures the KERNAL debounce logic registers every stroke
#define C64_MIN_HOLD_TIME_US    35000

//--------------------------------------------------------------------
// PUBLIC API
//--------------------------------------------------------------------

// Initialize GPIO pins, registers, and launch Core 1 matrix worker
void c64_matrix_init(void);

// Core 1 matrix real-time responder task (runs exclusively on Core 1)
void c64_matrix_core1_run(void);

// Press a key in the C64 matrix (Row 0-7, Col 0-7)
void c64_matrix_press(uint8_t row, uint8_t col);

// Release a key in the C64 matrix (with automatic hold-time pacing)
void c64_matrix_release(uint8_t row, uint8_t col);

// Release all keys immediately
void c64_matrix_release_all(void);

// Set RESTORE key state (true = pressed/pulled to GND)
void c64_matrix_set_restore(bool pressed);

// Periodic task to process delayed key releases (debounce / hold-time)
void c64_matrix_task(void);

#ifdef __cplusplus
}
#endif

#endif // C64_MATRIX_H
