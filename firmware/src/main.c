#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "bsp/board.h"
#include "tusb.h"

#include "c64_matrix.h"
#include "usb_hid_host.h"

int main(void) {
    // 1. Initialize board and standard I/O (UART on GP0/GP1)
    board_init();
    stdio_init_all();

    printf("\r\n==============================================\r\n");
    printf("   Commodore 64 USB Keyboard & Wireless Host   \r\n");
    printf("   RP2040 Dual-Core Real-Time Matrix Emulator  \r\n");
    printf("   AGRAVITY Hardware / Software Project 2026   \r\n");
    printf("==============================================\r\n");

    // 2. Initialize C64 matrix GPIOs
    printf("[INIT] Initializing C64 Matrix GPIOs...\r\n");
    c64_matrix_init();

    // 3. Launch Core 1 dedicated matrix snooper/driver
    // Core 1 handles real-time response (< 50ns) to C64 CIA scan cycles
    printf("[INIT] Launching Real-Time Matrix Engine on Core 1...\r\n");
    multicore_launch_core1(c64_matrix_core1_run);

    // 4. Initialize USB HID host stack
    printf("[INIT] Initializing USB Host Stack (TinyUSB)...\r\n");
    tusb_init();
    usb_hid_host_init();

    printf("[READY] Waiting for USB Keyboard / Wireless Combo...\r\n\r\n");

    // 5. Core 0 Main Loop
    while (1) {
        // USB host controller event processing
        tuh_task();

        // Process debounce hold-time timers and LED state
        c64_matrix_task();
    }

    return 0;
}
