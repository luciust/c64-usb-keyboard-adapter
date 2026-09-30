#include "keymap.h"

// Lookup table for USB HID keycodes (0x00 to 0x7F)
static const c64_key_mapping_t hid_to_c64_table[128] = {
    // 0x00 - 0x03: Reserved
    [0x00] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_NONE },
    [0x01] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_NONE },
    [0x02] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_NONE },
    [0x03] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_NONE },

    // Letters (A-Z)
    [0x04] = { 1, 2, KEYMAP_FLAG_NONE }, // A
    [0x05] = { 3, 4, KEYMAP_FLAG_NONE }, // B
    [0x06] = { 2, 4, KEYMAP_FLAG_NONE }, // C
    [0x07] = { 2, 2, KEYMAP_FLAG_NONE }, // D
    [0x08] = { 1, 6, KEYMAP_FLAG_NONE }, // E
    [0x09] = { 2, 5, KEYMAP_FLAG_NONE }, // F
    [0x0A] = { 3, 2, KEYMAP_FLAG_NONE }, // G
    [0x0B] = { 3, 5, KEYMAP_FLAG_NONE }, // H
    [0x0C] = { 4, 1, KEYMAP_FLAG_NONE }, // I
    [0x0D] = { 4, 2, KEYMAP_FLAG_NONE }, // J
    [0x0E] = { 4, 5, KEYMAP_FLAG_NONE }, // K
    [0x0F] = { 5, 2, KEYMAP_FLAG_NONE }, // L
    [0x10] = { 4, 4, KEYMAP_FLAG_NONE }, // M
    [0x11] = { 4, 7, KEYMAP_FLAG_NONE }, // N
    [0x12] = { 4, 6, KEYMAP_FLAG_NONE }, // O
    [0x13] = { 5, 1, KEYMAP_FLAG_NONE }, // P
    [0x14] = { 7, 6, KEYMAP_FLAG_NONE }, // Q
    [0x15] = { 2, 1, KEYMAP_FLAG_NONE }, // R
    [0x16] = { 1, 5, KEYMAP_FLAG_NONE }, // S
    [0x17] = { 2, 6, KEYMAP_FLAG_NONE }, // T
    [0x18] = { 3, 6, KEYMAP_FLAG_NONE }, // U
    [0x19] = { 3, 7, KEYMAP_FLAG_NONE }, // V
    [0x1A] = { 1, 1, KEYMAP_FLAG_NONE }, // W
    [0x1B] = { 2, 7, KEYMAP_FLAG_NONE }, // X
    [0x1C] = { 3, 1, KEYMAP_FLAG_NONE }, // Y
    [0x1D] = { 1, 4, KEYMAP_FLAG_NONE }, // Z

    // Numbers (1-0)
    [0x1E] = { 7, 0, KEYMAP_FLAG_NONE }, // 1
    [0x1F] = { 7, 3, KEYMAP_FLAG_NONE }, // 2
    [0x20] = { 1, 0, KEYMAP_FLAG_NONE }, // 3
    [0x21] = { 1, 3, KEYMAP_FLAG_NONE }, // 4
    [0x22] = { 2, 0, KEYMAP_FLAG_NONE }, // 5
    [0x23] = { 2, 3, KEYMAP_FLAG_NONE }, // 6
    [0x24] = { 3, 0, KEYMAP_FLAG_NONE }, // 7
    [0x25] = { 3, 3, KEYMAP_FLAG_NONE }, // 8
    [0x26] = { 4, 0, KEYMAP_FLAG_NONE }, // 9
    [0x27] = { 4, 3, KEYMAP_FLAG_NONE }, // 0

    // Standard control / punctuation
    [0x28] = { 0, 1, KEYMAP_FLAG_NONE }, // Enter / RETURN
    [0x29] = { 7, 7, KEYMAP_FLAG_NONE }, // Escape -> RUN/STOP
    [0x2A] = { 0, 0, KEYMAP_FLAG_NONE }, // Backspace -> INST/DEL
    [0x2B] = { 7, 2, KEYMAP_FLAG_NONE }, // Tab -> CTRL
    [0x2C] = { 7, 4, KEYMAP_FLAG_NONE }, // Space
    [0x2D] = { 5, 3, KEYMAP_FLAG_NONE }, // Minus (-)
    [0x2E] = { 6, 5, KEYMAP_FLAG_NONE }, // Equals (=)
    [0x2F] = { 5, 6, KEYMAP_FLAG_NONE }, // Left Bracket ([) -> C64 @
    [0x30] = { 6, 1, KEYMAP_FLAG_NONE }, // Right Bracket (]) -> C64 *
    [0x31] = { 6, 0, KEYMAP_FLAG_NONE }, // Backslash (\) -> C64 Pound (£)
    [0x33] = { 6, 2, KEYMAP_FLAG_NONE }, // Semicolon (;)
    [0x34] = { 5, 5, KEYMAP_FLAG_NONE }, // Apostrophe (') -> C64 Colon (:)
    [0x35] = { 7, 1, KEYMAP_FLAG_NONE }, // Grave (`) -> C64 Left Arrow (←)
    [0x36] = { 5, 7, KEYMAP_FLAG_NONE }, // Comma (,)
    [0x37] = { 5, 4, KEYMAP_FLAG_NONE }, // Period (.)
    [0x38] = { 6, 7, KEYMAP_FLAG_NONE }, // Slash (/)

    // Function keys
    [0x3A] = { 0, 4, KEYMAP_FLAG_NONE },       // F1
    [0x3B] = { 0, 4, KEYMAP_FLAG_AUTO_SHIFT },  // F2 (Shift + F1)
    [0x3C] = { 0, 5, KEYMAP_FLAG_NONE },       // F3
    [0x3D] = { 0, 5, KEYMAP_FLAG_AUTO_SHIFT },  // F4 (Shift + F3)
    [0x3E] = { 0, 6, KEYMAP_FLAG_NONE },       // F5
    [0x3F] = { 0, 6, KEYMAP_FLAG_AUTO_SHIFT },  // F6 (Shift + F5)
    [0x40] = { 0, 3, KEYMAP_FLAG_NONE },       // F7
    [0x41] = { 0, 3, KEYMAP_FLAG_AUTO_SHIFT },  // F8 (Shift + F7)
    [0x45] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_RESTORE }, // F12 -> RESTORE

    // Navigation & Editing
    [0x48] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_RESTORE }, // Pause/Break -> RESTORE
    [0x49] = { 0, 0, KEYMAP_FLAG_AUTO_SHIFT },  // Insert -> Shift + INST/DEL
    [0x4A] = { 6, 3, KEYMAP_FLAG_NONE },       // Home -> CLR/HOME
    [0x4B] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_RESTORE }, // Page Up -> RESTORE
    [0x4C] = { 0, 0, KEYMAP_FLAG_NONE },       // Delete -> INST/DEL
    [0x4D] = { 6, 3, KEYMAP_FLAG_AUTO_SHIFT },  // End -> Clear Screen (Shift + CLR/HOME)
    [0x4E] = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_RESTORE }, // Page Down -> RESTORE

    // Cursor keys
    [0x4F] = { 0, 2, KEYMAP_FLAG_NONE },       // Right Arrow -> CRSR RIGHT
    [0x50] = { 0, 2, KEYMAP_FLAG_AUTO_SHIFT },  // Left Arrow -> CRSR LEFT (Shift + CRSR RIGHT)
    [0x51] = { 0, 7, KEYMAP_FLAG_NONE },       // Down Arrow -> CRSR DOWN
    [0x52] = { 0, 7, KEYMAP_FLAG_AUTO_SHIFT },  // Up Arrow -> CRSR UP (Shift + CRSR DOWN)

    // Keypad keys
    [0x54] = { 6, 7, KEYMAP_FLAG_NONE }, // KP / -> Slash
    [0x55] = { 6, 1, KEYMAP_FLAG_NONE }, // KP * -> Asterisk
    [0x56] = { 5, 3, KEYMAP_FLAG_NONE }, // KP - -> Minus
    [0x57] = { 5, 0, KEYMAP_FLAG_NONE }, // KP + -> Plus (+)
    [0x58] = { 0, 1, KEYMAP_FLAG_NONE }, // KP Enter -> RETURN
    [0x59] = { 7, 0, KEYMAP_FLAG_NONE }, // KP 1
    [0x5A] = { 7, 3, KEYMAP_FLAG_NONE }, // KP 2
    [0x5B] = { 1, 0, KEYMAP_FLAG_NONE }, // KP 3
    [0x5C] = { 1, 3, KEYMAP_FLAG_NONE }, // KP 4
    [0x5D] = { 2, 0, KEYMAP_FLAG_NONE }, // KP 5
    [0x5E] = { 2, 3, KEYMAP_FLAG_NONE }, // KP 6
    [0x5F] = { 3, 0, KEYMAP_FLAG_NONE }, // KP 7
    [0x60] = { 3, 3, KEYMAP_FLAG_NONE }, // KP 8
    [0x61] = { 4, 0, KEYMAP_FLAG_NONE }, // KP 9
    [0x62] = { 4, 3, KEYMAP_FLAG_NONE }, // KP 0
    [0x63] = { 5, 4, KEYMAP_FLAG_NONE }, // KP . -> Period
};

c64_key_mapping_t keymap_get_c64_key(uint8_t hid_code) {
    if (hid_code < 128) {
        return hid_to_c64_table[hid_code];
    }
    c64_key_mapping_t none = { C64_KEY_NONE, C64_KEY_NONE, KEYMAP_FLAG_NONE };
    return none;
}
