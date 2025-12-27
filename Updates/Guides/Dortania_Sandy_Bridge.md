# Dortania OpenCore Install Guide - Laptop Sandy Bridge

*Source: [https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/sandy-bridge.html](https://dortania.github.io/OpenCore-Install-Guide/config-laptop.plist/sandy-bridge.html)*

## Starting Point

Making a config.plist may seem hard, it's not. It just takes some time but this guide will tell you how to configure everything.

**Tools needed:**
*   [ProperTree](https://github.com/corpnewt/ProperTree) - Universal plist editor
*   [GenSMBIOS](https://github.com/corpnewt/GenSMBIOS) - For generating SMBIOS data
*   [Sample/config.plist](https://github.com/acidanthera/OpenCorePkg/releases)

## ACPI

### Add

You will need SSDTs to bring back functionality:

*   **SSDT-PM**: Needed for proper CPU power management. Run Pike's `ssdtPRGen.sh` script to generate this.
*   **SSDT-EC**: Fixes the embedded controller.
*   **SSDT-XOSI**: Makes all _OSI calls specific to Windows work for macOS.
*   **SSDT-PNLF**: Fixes brightness control.
*   **SSDT-IMEI**: Needed for Sandy Bridge CPU with 7 series motherboards (Not needed for 6-series).

**Note:** Do not add your generated `DSDT.aml` here.

### Delete

*   **CpuPm**: Drop table with Signature `53534454` and OemTableId `437075506d000000`.
*   **Cpu0Ist**: Drop table with Signature `53534454` and OemTableId `4370753049737400`.

### Patch

*   **OSI rename**: Find `5f4f5349`, Replace `584f5349` (Required for SSDT-XOSI).

## DeviceProperties

### Add

**PciRoot(0x0)/Pci(0x2,0x0)** (iGPU)

*   `AAPL,snb-platform-id`: `00000100` (Laptop)

**PciRoot(0x0)/Pci(0x16,0x0)** (IMEI - Mixed Chipset only)

*   `device-id`: `3A1C0000` (Only if you have 7-series chipset with Sandy Bridge CPU)

**PciRoot(0x0)/Pci(0x1b,0x0)** (Audio)

*   Use boot-arg `alcid=xxx` instead.

## Kernel

### Quirks

*   `AppleCpuPmCfgLock`: **YES** (If CFG-Lock enabled in BIOS)
*   `DisableIoMapper`: **YES** (If VT-d enabled in BIOS)
*   `PanicNoKextDump`: **YES**
*   `PowerTimeoutKernelPanic`: **YES**
*   `XhciPortLimit`: **YES** (If USB 3.0 issues on older macOS)

## Misc

### Boot

*   `HideAuxiliary`: **YES**

### Debug

*   `AppleDebug`: **YES**
*   `ApplePanic`: **YES**
*   `DisableWatchDog`: **YES**
*   `Target`: `67`

### Security

*   `AllowSetDefault`: **YES**
*   `ScanPolicy`: `0`
*   `SecureBootModel`: `Default` (or `Disabled` for older macOS/modifications)
*   `Vault`: `Optional`

## NVRAM

### Add

**7C436110-AB2A-4BBB-A880-FE41995C9F82**

*   `boot-args`: `-v debug=0x100 keepsyms=1 alcid=1` (Add `-wegnoegpu` if disabling dGPU)
*   `csr-active-config`: `00000000` (SIP Enabled)
*   `prev-lang:kbd`: `en-US:0` (String)

## PlatformInfo

### Generic

*   **SystemProductName**: `MacBookPro8,1` (13") or `MacBookPro8,2` (15")
*   Generate Serial, Board Serial, SmUUID using GenSMBIOS.

## UEFI

### APFS

*   `MinDate` / `MinVersion`: `-1` (For High Sierra and older, or if using older OpenCore versions)

### Quirks

*   `IgnoreInvalidFlexRatio`: **YES**
*   `ReleaseUsbOwnership`: **YES**
*   `UnblockFsConnect`: **NO** (HP only)

## Intel BIOS Settings

**Disable:**
*   Fast Boot
*   Secure Boot
*   VT-d (can be enabled if DisableIoMapper is YES)
*   CSM
*   CFG Lock

**Enable:**
*   VT-x
*   Above 4G Decoding
*   Hyper-Threading
*   Execute Disable Bit
*   EHCI/XHCI Hand-off
*   SATA Mode: AHCI
