# Lenovo Thinkpad X220 OpenCore Adoption Guide (Monterey Update)

![](./x220_High_Sierra.jpg)

## Overview

This repo provides an OpenCore configuration for the Lenovo ThinkPad X220. It has been updated to support **macOS Monterey** using **OpenCore 1.0.6**.

**Important for Monterey:**
The X220 uses Intel HD 3000 graphics, which are **not natively supported** in macOS Monterey. You **MUST** use [OpenCore Legacy Patcher (OCLP)](https://dortania.github.io/OpenCore-Legacy-Patcher/) after installation to enable graphics acceleration. Without it, the system will be extremely slow.

## Updates (December 2025)

*   **OpenCore**: Updated to **1.0.6**
*   **Kexts**: Updated to latest versions (Lilu 1.7.1, WEG 1.7.0, AppleALC 1.9.6, etc.)
*   **Target OS**: macOS Monterey (requires OCLP)

## Installation Steps

1.  **Flash BIOS**: Ensure you are running the modified BIOS (included in `X220_v1.46_Modified_BIOS.zip`) to remove the whitelist.
2.  **Create Installer**: Follow [Dortania's Guide](https://dortania.github.io/OpenCore-Install-Guide/) to create a macOS Monterey USB installer.
3.  **Prepare EFI**:
    *   Use the files in `Updates/OpenCore` as a base.
    *   Add the Kexts from `Updates/Kexts`.
    *   Add your `DSDT.aml` and `SSDT-PM.aml` to `ACPI`.
    *   Configure `config.plist` using **ProperTree** (found in `Updates/Tools`).
4.  **Install macOS**: Boot from USB and install Monterey.
5.  **Post-Install**:
    *   **Graphics**: Download and run **OpenCore Legacy Patcher**. Select "Post-Install Root Patch" to fix Intel HD 3000 graphics.
    *   **Power Management**: Generate a new `SSDT-PM.aml` for your specific CPU using `ssdtPRGen.sh` if needed.

## Additional Information

#### Why can't one simply follow Dortania's Guide?

Well, I actually followed [Dortania's guide](https://dortania.github.io/OpenCore-Install-Guide/) to make this repo, but some modifications had to be made to make audio and battery readouts work.

1. `Misc -> Security -> SecureBootModel` is set to `Disabled`.

2. `UEFI -> APFS -> MinDate & MinVersion` are set to `-1` to allow `High Sierra` installation with `APFS`.

2. NVRAM emulation is `Enabled` by adjusting `config.plist` according to the following steps ([source](https://www.reddit.com/r/hackintosh/comments/wdugxf/how_to_opencore_082_083_differences/)):
```
* OpenRuntime.efi specified after OpenVariableRuntimeDxe.efi in the Drivers list
* OpenVariableRuntimeDxe.efi loaded using LoadEarly=true
* OpenRuntime.efi also loaded using LoadEarly=true for correct operation of * RequestBootVarRouting
* LegacySchema populated
* LegacyOverwrite enabled to be able to overwrite any existing variable
* ExposeSensitiveData with at least bit 0x1 set
* This driver requires working FAT write support in firmware, and sufficient free space on the OpenCore EFI partition for up to three saved NVRAM files
* NVRAM values are loaded from NVRAM/nvram.plist
* Reset NVRAM option installed by the ResetNvramEntry driver removes NVRAM/nvram.plist instead of affecting underlying NVRAM
* CTRL+Enter in the OpenCore bootpicker updates or creates NVRAM/nvram.plist.
```

4. Using `DSDT.aml` from [mcdonnelltech](httpshttps://x220.mcdonnelltech.com//) to fix audio and battery readouts, instead of custom `SSDT`s.
I know this is not a good practice, but currently I can't spare the time and energy to reverse engineer every patch done to the `DSDT` and make seperate `SSDT` patches.
If the custom `SSDT`s are made, we can ditch `rEFInd` and use `OpenCore` to boot all OSes, which is a lot cleaner.
If anyone is interested in doing this, you're welcomed to fork this repo or create PRs.

5. **Intel Wi-Fi**: This guide now supports the Intel Centrino Advanced-N 6300 via `AirportItlwm`. See `Updates/Guides/Intel_WiFi_Setup.md` for details.

#### Binary Versions (Updated)

| Binary               | Version |
| -------------------- | ---------------- |
| OpenCore             | 1.0.6            |
| Lilu                 | 1.7.1            |
| AppleALC             | 1.9.6            |
| WhateverGreen        | 1.7.0            |
| VirtualSMC           | 1.3.7            |
| VoodooPS2Controller  | 2.3.7            |
| IntelMausi           | 1.0.8            |
| AirportItlwm         | 2.3.0 (Monterey) |
