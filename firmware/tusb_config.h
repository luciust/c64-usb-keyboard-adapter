#ifndef _TUSB_CONFIG_H_
#define _TUSB_CONFIG_H_

#ifdef __cplusplus
extern "C" {
#endif

//--------------------------------------------------------------------
// COMMON CONFIGURATION
//--------------------------------------------------------------------

#ifndef CFG_TUSB_MCU
#define CFG_TUSB_MCU                OPT_MCU_RP2040
#endif

#ifndef CFG_TUSB_OS
#define CFG_TUSB_OS                 OPT_OS_NONE
#endif

#ifndef CFG_TUSB_DEBUG
#define CFG_TUSB_DEBUG              0
#endif

// Root hub port 0 configured as USB Host
#ifndef CFG_TUSB_RHPORT0_MODE
#define CFG_TUSB_RHPORT0_MODE       OPT_MODE_HOST
#endif

// Memory alignment and sizing
#ifndef CFG_TUH_MEM_SECTION
#define CFG_TUH_MEM_SECTION
#endif

#ifndef CFG_TUH_MEM_ALIGN
#define CFG_TUH_MEM_ALIGN           __attribute__((aligned(4)))
#endif

//--------------------------------------------------------------------
// HOST CONFIGURATION
//--------------------------------------------------------------------

#define CFG_TUH_ENABLED             1

#ifndef BOARD_TUH_RHPORT
#define BOARD_TUH_RHPORT            0
#endif

#define CFG_TUH_ENUMERATION_BUFSIZE 256

// Max devices supported (handles hubs and combo dongles)
#define CFG_TUH_DEVICE_MAX          4

// Support USB Hubs (vital for external hubs or combo devices)
#define CFG_TUH_HUB                 1

// Support HID Class (up to 4 interfaces: keyboard, mouse, consumer, etc.)
#define CFG_TUH_HID                 4

// Buffer size for HID Endpoints
#define CFG_TUH_HID_EPIN_BUFSIZE    64
#define CFG_TUH_HID_EPOUT_BUFSIZE   64

#ifdef __cplusplus
}
#endif

#endif /* _TUSB_CONFIG_H_ */
