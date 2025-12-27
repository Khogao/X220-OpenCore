# OpenCore 1.0.6 EFI for ThinkPad X220 (macOS Monterey)

This EFI folder has been built from scratch using OpenCore 1.0.6 and the latest Kexts.

## Specifications
- **Model**: Lenovo ThinkPad X220
- **CPU**: Intel Core i5-2520M (Sandy Bridge)
- **GPU**: Intel HD Graphics 3000
- **Wi-Fi**: Intel Centrino Advanced-N 6300 (Supported via `AirportItlwm.kext`)
- **Ethernet**: Intel 82579LM (Supported via `IntelMausi.kext`)
- **Audio**: Conexant CX20590 (Supported via `AppleALC.kext` layout-id 12 or similar - currently set to `alcid=1` in boot-args, change if needed)

## Contents
- **OpenCore**: v1.0.6 (Release)
- **Kexts**:
  - Lilu, WhateverGreen, AppleALC, VirtualSMC (plus plugins)
  - VoodooPS2Controller (Keyboard/Trackpad)
  - IntelMausi (Ethernet)
  - AirportItlwm (Wi-Fi for Monterey)
- **Drivers**: OpenRuntime, HfsPlusLegacy, OpenVariableRuntimeDxe (for NVRAM emulation)
- **ACPI**: DSDT.aml, SSDT-PM.aml

## Installation Instructions

1.  **Generate SMBIOS**:
    - The `config.plist` has `SystemProductName` set to `MacBookPro8,1`.
    - **Crucial**: You must generate a valid Serial Number, MLB, and UUID.
    - Use [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) to generate these values for `MacBookPro8,1`.
    - Update `PlatformInfo -> Generic` in `EFI/OC/config.plist` with your new values.

2.  **Copy to USB**:
    - Format a USB drive as FAT32 (Scheme: MBR or GPT).
    - Copy the `EFI` folder from `Updates/EFI_Monterey/` to the root of the USB drive.

3.  **BIOS Settings**:
    - Ensure BIOS is set to UEFI (or Both/Legacy First if needed, but UEFI preferred for OC).
    - Disable Secure Boot.
    - SATA Mode: AHCI.

4.  **Post-Install (Graphics)**:
    - Intel HD 3000 requires **OpenCore Legacy Patcher (OCLP)** to work fully in macOS Monterey.
    - After installing macOS, download and run OCLP to patch the graphics drivers.

## Notes
- **Wi-Fi**: `AirportItlwm.kext` is included. It works like a native card but requires you to join networks via the menu bar (or it might need manual setup if using the hidden network). It does *not* support AirDrop/Handoff.
- **Bluetooth**: If you have the original Bluetooth 3.0 module, it might work or require `IntelBluetoothFirmware`. This EFI does not currently include Bluetooth kexts. If you need them, download `IntelBluetoothFirmware` and add it.
