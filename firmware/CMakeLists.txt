cmake_minimum_required(VERSION 3.13)

# Initialize pico-sdk from GIT or environment
include(pico_sdk_import.cmake)

project(c64_usb_keyboard C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize Raspberry Pi Pico SDK
pico_sdk_init()

add_executable(c64_usb_keyboard
    src/main.c
    src/c64_matrix.c
    src/keymap.c
    src/usb_hid_host.c
)

# TinyUSB and Pico libraries
target_link_libraries(c64_usb_keyboard
    pico_stdlib
    pico_multicore
    tinyusb_host
    tinyusb_board
    hardware_gpio
    hardware_sync
    hardware_uart
)

# Enable UART stdio for debugging, disable USB CDC stdio (since native USB is HOST)
pico_enable_stdio_usb(c64_usb_keyboard 0)
pico_enable_stdio_uart(c64_usb_keyboard 1)

target_include_directories(c64_usb_keyboard PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/src
)

# Generate UF2, HEX, and BIN
pico_add_extra_outputs(c64_usb_keyboard)
