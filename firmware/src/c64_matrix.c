#include "c64_matrix.h"
#include "hardware/gpio.h"
#include "hardware/sync.h"
#include "pico/multicore.h"
#include <stdio.h>

// Array mapping each Column (0-7) to a bitmask of active Rows (bit 0-7)
// When Column C is pulled LOW by the C64 CIA, any bit R set in c64_col_to_rows[C]
// will cause Row R to be driven LOW (0V) via native open-drain (GPIO_OE = 1).
static volatile uint8_t c64_col_to_rows[C64_MATRIX_COLS];

// Debounce / Hold-time management
static absolute_time_t press_timestamp[C64_MATRIX_ROWS][C64_MATRIX_COLS];
static volatile bool pending_release[C64_MATRIX_ROWS][C64_MATRIX_COLS];
static volatile bool is_pressed[C64_MATRIX_ROWS][C64_MATRIX_COLS];

// RESTORE key state (Native Open-Drain on GP16)
static volatile bool restore_active = false;
static absolute_time_t restore_press_time;
static volatile bool restore_pending_release = false;

// LED activity toggle
static absolute_time_t last_led_blink;

void c64_matrix_init(void) {
    // 1. Initialize Column inputs (GP0 - GP7)
    // On Pico 2 (RP2350), GP0-GP7 are 5V-tolerant digital inputs.
    // They connect DIRECTLY to C64 CIA 1 Port A (PA0 - PA7) with zero level shifters!
    for (int col = 0; col < C64_MATRIX_COLS; col++) {
        uint pin = C64_COL_BASE_PIN + col;
        gpio_init(pin);
        gpio_set_dir(pin, GPIO_IN);
        gpio_disable_pulls(pin);
    }

    // 2. Initialize Row outputs (GP8 - GP15)
    // On Pico 2 (RP2350), we use Native Open-Drain:
    // Output latch is locked to 0 (GND).
    // To assert (pull LOW): Direction = GPIO_OUT (sinks current to GND).
    // To release (High-Z): Direction = GPIO_IN (5V-tolerant input, line pulled up to 5V by C64).
    for (int row = 0; row < C64_MATRIX_ROWS; row++) {
        uint pin = C64_ROW_BASE_PIN + row;
        gpio_init(pin);
        gpio_put(pin, 0);         // Latch locked to 0 (GND)
        gpio_set_dir(pin, GPIO_IN); // Start in High-Z (unpressed)
        gpio_disable_pulls(pin);
    }

    // 3. Initialize RESTORE pin (GP16)
    // Native Open-Drain directly connected to C64 CN8 Pin 3 (/RESTORE)
    gpio_init(C64_RESTORE_PIN);
    gpio_put(C64_RESTORE_PIN, 0);         // Latch locked to 0 (GND)
    gpio_set_dir(C64_RESTORE_PIN, GPIO_IN); // Start in High-Z
    gpio_disable_pulls(C64_RESTORE_PIN);

    // 4. Initialize Status LED (GP25)
    gpio_init(STATUS_LED_PIN);
    gpio_set_dir(STATUS_LED_PIN, GPIO_OUT);
    gpio_put(STATUS_LED_PIN, 0);

    // Clear matrix state
    for (int c = 0; c < C64_MATRIX_COLS; c++) {
        c64_col_to_rows[c] = 0;
        for (int r = 0; r < C64_MATRIX_ROWS; r++) {
            pending_release[r][c] = false;
            is_pressed[r][c] = false;
        }
    }
}

// Core 1 dedicated real-time matrix loop (Native Open-Drain Engine)
// Latency: < 30 nanoseconds from C64 column strobe to row response
void c64_matrix_core1_run(void) {
    while (1) {
        // Sample all 8 Column inputs (GP0 - GP7)
        // Active LOW from C64 CIA (0 = column selected, 1 = unselected)
        uint32_t gpio_in = sio_hw->gpio_in;
        uint8_t cols_raw = (uint8_t)(gpio_in & C64_COL_MASK);
        uint8_t active_cols = (uint8_t)(~cols_raw); // 1 = selected column

        uint8_t rows_active = 0;
        if (active_cols != 0) {
            // Unroll for maximum execution speed (< 12 CPU cycles on Cortex-M33)
            if (active_cols & 0x01) rows_active |= c64_col_to_rows[0];
            if (active_cols & 0x02) rows_active |= c64_col_to_rows[1];
            if (active_cols & 0x04) rows_active |= c64_col_to_rows[2];
            if (active_cols & 0x08) rows_active |= c64_col_to_rows[3];
            if (active_cols & 0x10) rows_active |= c64_col_to_rows[4];
            if (active_cols & 0x20) rows_active |= c64_col_to_rows[5];
            if (active_cols & 0x40) rows_active |= c64_col_to_rows[6];
            if (active_cols & 0x80) rows_active |= c64_col_to_rows[7];
        }

        // Native Open-Drain control via Output Enable (sio_hw->gpio_oe):
        // Bit = 1: Output enabled -> drives 0V (GND)
        // Bit = 0: Output disabled -> High-Z (floats to 5V via C64 motherboard pull-ups)
        uint32_t oe_bits = ((uint32_t)rows_active) << C64_ROW_BASE_PIN;
        sio_hw->gpio_oe = (sio_hw->gpio_oe & ~C64_ROW_MASK) | oe_bits;
    }
}

void c64_matrix_press(uint8_t row, uint8_t col) {
    if (row >= C64_MATRIX_ROWS || col >= C64_MATRIX_COLS) return;

    press_timestamp[row][col] = get_absolute_time();
    pending_release[row][col] = false;
    is_pressed[row][col] = true;

    c64_col_to_rows[col] |= (uint8_t)(1 << row);

    // Activity LED pulse
    gpio_put(STATUS_LED_PIN, 1);
    last_led_blink = get_absolute_time();
}

void c64_matrix_release(uint8_t row, uint8_t col) {
    if (row >= C64_MATRIX_ROWS || col >= C64_MATRIX_COLS) return;

    if (!is_pressed[row][col]) return;

    int64_t held_us = absolute_time_diff_us(press_timestamp[row][col], get_absolute_time());
    if (held_us >= C64_MIN_HOLD_TIME_US) {
        c64_col_to_rows[col] &= (uint8_t)~(1 << row);
        is_pressed[row][col] = false;
        pending_release[row][col] = false;
    } else {
        pending_release[row][col] = true;
    }
}

void c64_matrix_release_all(void) {
    for (int c = 0; c < C64_MATRIX_COLS; c++) {
        c64_col_to_rows[c] = 0;
        for (int r = 0; r < C64_MATRIX_ROWS; r++) {
            pending_release[r][c] = false;
            is_pressed[r][c] = false;
        }
    }
    // High-Z on all rows immediately
    sio_hw->gpio_oe &= ~C64_ROW_MASK;
    c64_matrix_set_restore(false);
}

void c64_matrix_set_restore(bool pressed) {
    if (pressed) {
        restore_active = true;
        restore_pending_release = false;
        restore_press_time = get_absolute_time();
        // Drive GP16 LOW (OUTPUT mode) -> pulls /RESTORE to GND
        gpio_set_dir(C64_RESTORE_PIN, GPIO_OUT);
        gpio_put(STATUS_LED_PIN, 1);
    } else {
        if (!restore_active) return;
        int64_t held_us = absolute_time_diff_us(restore_press_time, get_absolute_time());
        if (held_us >= C64_MIN_HOLD_TIME_US) {
            restore_active = false;
            restore_pending_release = false;
            // High-Z (INPUT mode) -> line floats back to 5V
            gpio_set_dir(C64_RESTORE_PIN, GPIO_IN);
        } else {
            restore_pending_release = true;
        }
    }
}

void c64_matrix_task(void) {
    absolute_time_t now = get_absolute_time();

    // Process pending matrix key releases
    for (int col = 0; col < C64_MATRIX_COLS; col++) {
        for (int row = 0; row < C64_MATRIX_ROWS; row++) {
            if (pending_release[row][col]) {
                int64_t held_us = absolute_time_diff_us(press_timestamp[row][col], now);
                if (held_us >= C64_MIN_HOLD_TIME_US) {
                    c64_col_to_rows[col] &= (uint8_t)~(1 << row);
                    is_pressed[row][col] = false;
                    pending_release[row][col] = false;
                }
            }
        }
    }

    // Process pending RESTORE key release
    if (restore_pending_release) {
        int64_t held_us = absolute_time_diff_us(restore_press_time, now);
        if (held_us >= C64_MIN_HOLD_TIME_US) {
            restore_active = false;
            restore_pending_release = false;
            gpio_set_dir(C64_RESTORE_PIN, GPIO_IN);
        }
    }

    // Turn off activity LED after 50ms
    if (absolute_time_diff_us(last_led_blink, now) > 50000) {
        gpio_put(STATUS_LED_PIN, 0);
    }
}
