#include "usb_hid_host.h"
#include "c64_matrix.h"
#include "keymap.h"
#include "tusb.h"
#include <stdio.h>
#include <string.h>

// Track active HID instances to support wireless combo sets (keyboard + mouse)
#define MAX_HID_INSTANCES   CFG_TUH_HID

typedef enum {
    DEV_TYPE_UNKNOWN = 0,
    DEV_TYPE_KEYBOARD,
    DEV_TYPE_MOUSE
} hid_dev_type_t;

typedef struct {
    uint8_t dev_addr;
    uint8_t instance;
    hid_dev_type_t dev_type;
    uint8_t prev_modifier;
    uint8_t prev_keys[6];
} hid_instance_state_t;

static hid_instance_state_t hid_states[MAX_HID_INSTANCES];

void usb_hid_host_init(void) {
    memset(hid_states, 0, sizeof(hid_states));
}

// Find state slot by address and instance
static hid_instance_state_t* get_instance_state(uint8_t dev_addr, uint8_t instance) {
    for (int i = 0; i < MAX_HID_INSTANCES; i++) {
        if (hid_states[i].dev_addr == dev_addr && hid_states[i].instance == instance) {
            return &hid_states[i];
        }
    }
    // Allocate empty slot
    for (int i = 0; i < MAX_HID_INSTANCES; i++) {
        if (hid_states[i].dev_addr == 0) {
            hid_states[i].dev_addr = dev_addr;
            hid_states[i].instance = instance;
            hid_states[i].dev_type = DEV_TYPE_UNKNOWN;
            hid_states[i].prev_modifier = 0;
            memset(hid_states[i].prev_keys, 0, sizeof(hid_states[i].prev_keys));
            return &hid_states[i];
        }
    }
    return NULL;
}

static void release_instance_state(uint8_t dev_addr, uint8_t instance) {
    for (int i = 0; i < MAX_HID_INSTANCES; i++) {
        if (hid_states[i].dev_addr == dev_addr && hid_states[i].instance == instance) {
            memset(&hid_states[i], 0, sizeof(hid_instance_state_t));
            break;
        }
    }
}

// Check if a keycode exists in a 6-byte key array
static bool key_in_array(uint8_t code, const uint8_t array[6]) {
    if (code == 0) return false;
    for (int i = 0; i < 6; i++) {
        if (array[i] == code) return true;
    }
    return false;
}

// Process single key press
static void handle_key_press(uint8_t keycode) {
    c64_key_mapping_t map = keymap_get_c64_key(keycode);

    if (map.flags & KEYMAP_FLAG_RESTORE) {
        c64_matrix_set_restore(true);
        printf("[USB] RESTORE Pressed\r\n");
    }

    if (map.flags & KEYMAP_FLAG_AUTO_SHIFT) {
        // Assert C64 Left Shift along with the primary key
        c64_matrix_press(C64_ROW_LSHIFT, C64_COL_LSHIFT);
    }

    if (map.row != C64_KEY_NONE && map.col != C64_KEY_NONE) {
        c64_matrix_press(map.row, map.col);
        printf("[USB] Key 0x%02X -> C64 Row %d, Col %d\r\n", keycode, map.row, map.col);
    }
}

// Process single key release
static void handle_key_release(uint8_t keycode) {
    c64_key_mapping_t map = keymap_get_c64_key(keycode);

    if (map.flags & KEYMAP_FLAG_RESTORE) {
        c64_matrix_set_restore(false);
        printf("[USB] RESTORE Released\r\n");
    }

    if (map.row != C64_KEY_NONE && map.col != C64_KEY_NONE) {
        c64_matrix_release(map.row, map.col);
    }

    if (map.flags & KEYMAP_FLAG_AUTO_SHIFT) {
        // Release C64 Left Shift
        c64_matrix_release(C64_ROW_LSHIFT, C64_COL_LSHIFT);
    }
}

// Process modifier byte bit changes
static void handle_modifiers(uint8_t prev, uint8_t curr) {
    uint8_t changed = prev ^ curr;
    if (!changed) return;

    // Bit 0: Left Ctrl -> C64 CTRL (Row 7, Col 2)
    if (changed & 0x01) {
        if (curr & 0x01) c64_matrix_press(C64_ROW_CTRL, C64_COL_CTRL);
        else             c64_matrix_release(C64_ROW_CTRL, C64_COL_CTRL);
    }
    // Bit 1: Left Shift -> C64 Left Shift (Row 1, Col 7)
    if (changed & 0x02) {
        if (curr & 0x02) c64_matrix_press(C64_ROW_LSHIFT, C64_COL_LSHIFT);
        else             c64_matrix_release(C64_ROW_LSHIFT, C64_COL_LSHIFT);
    }
    // Bit 2: Left Alt -> C64 Commodore C= (Row 7, Col 5)
    if (changed & 0x04) {
        if (curr & 0x04) c64_matrix_press(C64_ROW_COMMODORE, C64_COL_COMMODORE);
        else             c64_matrix_release(C64_ROW_COMMODORE, C64_COL_COMMODORE);
    }
    // Bit 3: Left GUI (Win/Cmd) -> C64 Commodore C= (Row 7, Col 5)
    if (changed & 0x08) {
        if (curr & 0x08) c64_matrix_press(C64_ROW_COMMODORE, C64_COL_COMMODORE);
        else             c64_matrix_release(C64_ROW_COMMODORE, C64_COL_COMMODORE);
    }
    // Bit 4: Right Ctrl -> C64 CTRL (Row 7, Col 2)
    if (changed & 0x10) {
        if (curr & 0x10) c64_matrix_press(C64_ROW_CTRL, C64_COL_CTRL);
        else             c64_matrix_release(C64_ROW_CTRL, C64_COL_CTRL);
    }
    // Bit 5: Right Shift -> C64 Right Shift (Row 6, Col 4)
    if (changed & 0x20) {
        if (curr & 0x20) c64_matrix_press(C64_ROW_RSHIFT, C64_COL_RSHIFT);
        else             c64_matrix_release(C64_ROW_RSHIFT, C64_COL_RSHIFT);
    }
    // Bit 6: Right Alt -> C64 Commodore C= (Row 7, Col 5)
    if (changed & 0x40) {
        if (curr & 0x40) c64_matrix_press(C64_ROW_COMMODORE, C64_COL_COMMODORE);
        else             c64_matrix_release(C64_ROW_COMMODORE, C64_COL_COMMODORE);
    }
    // Bit 7: Right GUI -> C64 Commodore C= (Row 7, Col 5)
    if (changed & 0x80) {
        if (curr & 0x80) c64_matrix_press(C64_ROW_COMMODORE, C64_COL_COMMODORE);
        else             c64_matrix_release(C64_ROW_COMMODORE, C64_COL_COMMODORE);
    }
}

//--------------------------------------------------------------------+
// TinyUSB Callbacks
//--------------------------------------------------------------------+

void tuh_hid_mount_cb(uint8_t dev_addr, uint8_t instance, uint8_t const* desc_report, uint16_t desc_len) {
    (void)desc_report;
    (void)desc_len;

    hid_instance_state_t* state = get_instance_state(dev_addr, instance);
    uint8_t const itf_protocol = tuh_hid_interface_protocol(dev_addr, instance);

    printf("[USB] HID Device mounted: Addr %d, Instance %d, Protocol %d\r\n", dev_addr, instance, itf_protocol);

    if (itf_protocol == HID_ITF_PROTOCOL_KEYBOARD) {
        if (state) state->dev_type = DEV_TYPE_KEYBOARD;
        printf("[USB] Interface identified as KEYBOARD\r\n");
    } else if (itf_protocol == HID_ITF_PROTOCOL_MOUSE) {
        if (state) state->dev_type = DEV_TYPE_MOUSE;
        printf("[USB] Interface identified as MOUSE\r\n");
    } else {
        // Combo dongles often report HID_ITF_PROTOCOL_NONE; classify dynamically on first report
        if (state) state->dev_type = DEV_TYPE_UNKNOWN;
        printf("[USB] Interface protocol 0 (will autodetect from reports)\r\n");
    }

    // Request the first report
    tuh_hid_receive_report(dev_addr, instance);
}

void tuh_hid_umount_cb(uint8_t dev_addr, uint8_t instance) {
    printf("[USB] HID Device unmounted: Addr %d, Instance %d\r\n", dev_addr, instance);
    release_instance_state(dev_addr, instance);

    // Release all keys to prevent stuck keys when unplugged
    c64_matrix_release_all();
}

void tuh_hid_report_received_cb(uint8_t dev_addr, uint8_t instance, uint8_t const* report, uint16_t len) {
    hid_instance_state_t* state = get_instance_state(dev_addr, instance);
    if (!state) {
        tuh_hid_receive_report(dev_addr, instance);
        return;
    }

    // Pointer to keyboard boot report data
    uint8_t const* kbd_report = NULL;

    // Detect keyboard report format
    if (len == 8) {
        // Standard Boot Protocol Keyboard Report:
        // Byte 0: Modifiers, Byte 1: Reserved, Bytes 2-7: 6 Keycodes
        kbd_report = report;
        state->dev_type = DEV_TYPE_KEYBOARD;
    } else if (len == 9 && (report[0] == 1 || report[0] == 2)) {
        // Report with Report ID (common on wireless combo dongles)
        // If Report ID is 1 (Keyboard), data follows at report + 1
        if (report[0] == 1) {
            kbd_report = report + 1;
            state->dev_type = DEV_TYPE_KEYBOARD;
        } else {
            state->dev_type = DEV_TYPE_MOUSE;
        }
    } else if (len >= 3 && len <= 5) {
        // Standard mouse report (Buttons, X, Y, Wheel)
        state->dev_type = DEV_TYPE_MOUSE;
        // Mouse movement safely acknowledged without triggering keys
    }

    // If this is a valid keyboard report, process it
    if (kbd_report != NULL) {
        uint8_t modifier = kbd_report[0];
        uint8_t const* keys = &kbd_report[2];

        // 1. Process Modifiers
        handle_modifiers(state->prev_modifier, modifier);
        state->prev_modifier = modifier;

        // 2. Process Key Releases (keys in prev_keys but not in new keys)
        for (int i = 0; i < 6; i++) {
            uint8_t prev_k = state->prev_keys[i];
            if (prev_k != 0 && !key_in_array(prev_k, keys)) {
                handle_key_release(prev_k);
            }
        }

        // 3. Process Key Presses (keys in new keys but not in prev_keys)
        for (int i = 0; i < 6; i++) {
            uint8_t curr_k = keys[i];
            if (curr_k != 0 && !key_in_array(curr_k, state->prev_keys)) {
                handle_key_press(curr_k);
            }
        }

        // Save current key report
        memcpy(state->prev_keys, keys, 6);
    }

    // Continue receiving next report
    tuh_hid_receive_report(dev_addr, instance);
}
