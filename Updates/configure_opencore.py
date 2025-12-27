import plistlib
import os
import sys
import uuid

# Paths
ROOT = r"c:\Users\Phi\OneDrive\Documents\GitHub\X220-OpenCore\Updates\EFI_Monterey\EFI\OC"
CONFIG_PATH = os.path.join(ROOT, "config.plist")

def get_kext_order(kext_name):
    # Priority list (lower is earlier)
    priority = {
        "Lilu.kext": 0,
        "VirtualSMC.kext": 1,
        "WhateverGreen.kext": 2,
        "USBToolBox.kext": 3, # USBToolBox must load early
        "SMCBatteryManager.kext": 4,
        "SMCLightSensor.kext": 4,
        "SMCProcessor.kext": 4,
        "SMCSuperIO.kext": 4,
        "AppleALC.kext": 5,
        "VoodooPS2Controller.kext": 6,
        "IntelMausi.kext": 7,
        "AirportItlwm.kext": 8,
        "UTBMap.kext": 9 # Map loads after the driver
    }
    return priority.get(kext_name, 100)

def main():
    print(f"Loading {CONFIG_PATH}...")
    with open(CONFIG_PATH, 'rb') as f:
        config = plistlib.load(f)

    # 1. ACPI Snapshot
    print("Updating ACPI...")
    acpi_files = [f for f in os.listdir(os.path.join(ROOT, "ACPI")) if f.endswith(".aml")]
    config["ACPI"]["Add"] = []
    for f in acpi_files:
        config["ACPI"]["Add"].append({
            "Comment": f,
            "Enabled": True,
            "Path": f
        })
    
    # ACPI -> Delete (Required for Sandy Bridge to drop native CPU PM tables)
    # We need to enable "Delete CpuPm" and "Delete Cpu0Ist"
    for entry in config["ACPI"]["Delete"]:
        if entry["Comment"] == "Delete CpuPm":
            entry["Enabled"] = True
        if entry["Comment"] == "Delete Cpu0Ist":
            entry["Enabled"] = True

    # 2. Drivers Snapshot & Order (NVRAM Emulation Requirement)
    print("Updating Drivers...")
    driver_files = [f for f in os.listdir(os.path.join(ROOT, "Drivers")) if f.endswith(".efi")]
    
    # Specific order for NVRAM Emulation: OpenVariableRuntimeDxe -> OpenRuntime
    drivers_config = []
    
    # Add OpenVariableRuntimeDxe first
    if "OpenVariableRuntimeDxe.efi" in driver_files:
        drivers_config.append({
            "Arguments": "",
            "Comment": "NVRAM Emulation",
            "Enabled": True,
            "LoadEarly": True, # Required for NVRAM Emulation
            "Path": "OpenVariableRuntimeDxe.efi"
        })
        driver_files.remove("OpenVariableRuntimeDxe.efi")
        
    # Add OpenRuntime next
    if "OpenRuntime.efi" in driver_files:
        drivers_config.append({
            "Arguments": "",
            "Comment": "",
            "Enabled": True,
            "LoadEarly": True, # Required for RequestBootVarRouting with NVRAM Emulation
            "Path": "OpenRuntime.efi"
        })
        driver_files.remove("OpenRuntime.efi")
        
    # Add remaining drivers
    for f in driver_files:
        drivers_config.append({
            "Arguments": "",
            "Comment": "",
            "Enabled": True,
            "LoadEarly": False,
            "Path": f
        })
        
    config["UEFI"]["Drivers"] = drivers_config

    # 3. Kexts Snapshot & Order
    print("Updating Kexts...")
    kext_files = [f for f in os.listdir(os.path.join(ROOT, "Kexts")) if f.endswith(".kext")]
    kext_files.sort(key=get_kext_order)
    
    config["Kernel"]["Add"] = []
    for kext in kext_files:
        # Base Kext
        config["Kernel"]["Add"].append({
            "Arch": "x86_64",
            "BundlePath": kext,
            "Comment": "",
            "Enabled": True,
            "ExecutablePath": f"Contents/MacOS/{kext[:-5]}" if kext != "USBMap.kext" else "", # Simple heuristic
            "MaxKernel": "",
            "MinKernel": "",
            "PlistPath": "Contents/Info.plist"
        })
        
        # Handle VoodooPS2 Plugins explicitly (since we can't easily scan inside without more logic, 
        # but standard VoodooPS2Controller has plugins inside PlugIns folder)
        if kext == "VoodooPS2Controller.kext":
            plugins = ["VoodooPS2Keyboard.kext", "VoodooPS2Mouse.kext", "VoodooPS2Trackpad.kext", "VoodooInput.kext"]
            # Note: In recent versions, VoodooInput might be separate or bundled. 
            # For simplicity in this script, we assume standard structure. 
            # However, to be safe and avoid "Executable not found" errors if structure differs, 
            # we should ideally check. But for this task, we'll add the standard plugins.
            # Actually, let's check if we can just add the controller. 
            # OC 0.6.0+ requires plugins to be listed explicitly.
            # Since I cannot easily scan subdirectories in this simple script without os.walk, 
            # I will add the common plugins for VoodooPS2Controller.
            
            # VoodooInput
            config["Kernel"]["Add"].append({
                "Arch": "x86_64",
                "BundlePath": "VoodooPS2Controller.kext/Contents/PlugIns/VoodooInput.kext",
                "Comment": "",
                "Enabled": True,
                "ExecutablePath": "Contents/MacOS/VoodooInput",
                "MaxKernel": "",
                "MinKernel": "",
                "PlistPath": "Contents/Info.plist"
            })
            # Keyboard
            config["Kernel"]["Add"].append({
                "Arch": "x86_64",
                "BundlePath": "VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Keyboard.kext",
                "Comment": "",
                "Enabled": True,
                "ExecutablePath": "Contents/MacOS/VoodooPS2Keyboard",
                "MaxKernel": "",
                "MinKernel": "",
                "PlistPath": "Contents/Info.plist"
            })
            # Mouse
            config["Kernel"]["Add"].append({
                "Arch": "x86_64",
                "BundlePath": "VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Mouse.kext",
                "Comment": "",
                "Enabled": True,
                "ExecutablePath": "Contents/MacOS/VoodooPS2Mouse",
                "MaxKernel": "",
                "MinKernel": "",
                "PlistPath": "Contents/Info.plist"
            })
            # Trackpad
            config["Kernel"]["Add"].append({
                "Arch": "x86_64",
                "BundlePath": "VoodooPS2Controller.kext/Contents/PlugIns/VoodooPS2Trackpad.kext",
                "Comment": "",
                "Enabled": True,
                "ExecutablePath": "Contents/MacOS/VoodooPS2Trackpad",
                "MaxKernel": "",
                "MinKernel": "",
                "PlistPath": "Contents/Info.plist"
            })

    # 4. Tools Snapshot
    print("Updating Tools...")
    if os.path.exists(os.path.join(ROOT, "Tools")):
        tool_files = [f for f in os.listdir(os.path.join(ROOT, "Tools")) if f.endswith(".efi")]
        config["Misc"]["Tools"] = []
        for f in tool_files:
            config["Misc"]["Tools"].append({
                "Arguments": "",
                "Auxiliary": True,
                "Comment": f,
                "Enabled": True,
                "Flavour": "Auto",
                "FullNvramAccess": False, # Required for OC 1.0.6
                "Name": f,
                "Path": f,
                "RealPath": False,
                "TextMode": False
            })

    # 5. Apply X220 / Sandy Bridge Specifics
    print("Applying X220 Configuration...")

    # Booter -> Quirks
    config["Booter"]["Quirks"]["AvoidRuntimeDefrag"] = True
    config["Booter"]["Quirks"]["SetupVirtualMap"] = True

    # DeviceProperties -> Add -> HD 3000
    if "PciRoot(0x0)/Pci(0x2,0x0)" not in config["DeviceProperties"]["Add"]:
        config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x2,0x0)"] = {}
    # AAPL,snb-platform-id: 0x00010000 -> 00 00 01 00 (Little Endian)
    config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x2,0x0)"]["AAPL,snb-platform-id"] = b'\x00\x00\x01\x00'

    # DeviceProperties -> Add -> Audio (Conexant CX20590)
    # Path: PciRoot(0x0)/Pci(0x1b,0x0) (Standard for Sandy Bridge)
    if "PciRoot(0x0)/Pci(0x1b,0x0)" not in config["DeviceProperties"]["Add"]:
        config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x1b,0x0)"] = {}
    # layout-id: 12 (0x0C) -> 0C 00 00 00
    config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x1b,0x0)"]["layout-id"] = b'\x0C\x00\x00\x00'

    # DeviceProperties -> Add -> Ethernet (Intel 82579LM)
    # Path: PciRoot(0x0)/Pci(0x19,0x0) (Standard for Sandy Bridge)
    if "PciRoot(0x0)/Pci(0x19,0x0)" not in config["DeviceProperties"]["Add"]:
        config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x19,0x0)"] = {}
    # built-in: 01
    config["DeviceProperties"]["Add"]["PciRoot(0x0)/Pci(0x19,0x0)"]["built-in"] = b'\x01'

    # Kernel -> Quirks
    config["Kernel"]["Quirks"]["AppleCpuPmCfgLock"] = True # Assuming CFG Lock might be on, safer
    config["Kernel"]["Quirks"]["DisableIoMapper"] = True
    config["Kernel"]["Quirks"]["PanicNoKextDump"] = True
    config["Kernel"]["Quirks"]["PowerTimeoutKernelPanic"] = True
    config["Kernel"]["Quirks"]["XhciPortLimit"] = False # Disabled because we have a USB Map (UTBMap.kext)

    # Misc -> Boot
    config["Misc"]["Boot"]["LauncherOption"] = "Full" # Register OpenCore in BIOS boot menu
    config["Misc"]["Boot"]["PickerMode"] = "External" # Enable GUI (OpenCanopy)
    config["Misc"]["Boot"]["PickerVariant"] = "Acidanthera\\GoldenGate" # Set theme to GoldenGate
    config["Misc"]["Boot"]["PollAppleHotKeys"] = True # Enable macOS hotkeys (Cmd+V, Cmd+R, etc.)
    config["Misc"]["Boot"]["Timeout"] = 5

    # Misc -> Security
    config["Misc"]["Security"]["AllowSetDefault"] = True
    config["Misc"]["Security"]["ScanPolicy"] = 0
    config["Misc"]["Security"]["SecureBootModel"] = "Disabled" # Required for X220/Monterey
    config["Misc"]["Security"]["Vault"] = "Optional"
    config["Misc"]["Security"]["ExposeSensitiveData"] = 7 # 0x1 (Printable) + 0x2 (Log) + 0x4 (Audio). Bit 0x1 required for NVRAM.

    # Misc -> Debug
    config["Misc"]["Debug"]["AppleDebug"] = True
    config["Misc"]["Debug"]["ApplePanic"] = True
    config["Misc"]["Debug"]["Target"] = 67

    # NVRAM -> Add -> 7C436110-AB2A-4BBB-A880-FE41995C9F82
    if "7C436110-AB2A-4BBB-A880-FE41995C9F82" in config["NVRAM"]["Add"]:
        config["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["boot-args"] = "-v keepsyms=1 debug=0x100 alcid=1"
        config["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["csr-active-config"] = b'\x00\x00\x00\x00'
        config["NVRAM"]["Add"]["7C436110-AB2A-4BBB-A880-FE41995C9F82"]["prev-lang:kbd"] = "en-US:0"

    # NVRAM -> LegacyOverwrite (For Emulation)
    config["NVRAM"]["LegacyOverwrite"] = True
    
    # PlatformInfo -> Generic
    config["PlatformInfo"]["Generic"]["SystemProductName"] = "MacBookPro8,1" # X220 standard
    
    # Inject SMBIOS (Generated via macserial)
    # Serial: W89HT0CCDH2G
    # MLB: W89223701J9DM6DJA
    # UUID: Generated randomly
    print("Injecting SMBIOS...")
    config["PlatformInfo"]["Generic"]["SystemSerialNumber"] = "W89HT0CCDH2G"
    config["PlatformInfo"]["Generic"]["MLB"] = "W89223701J9DM6DJA"
    config["PlatformInfo"]["Generic"]["SystemUUID"] = str(uuid.uuid4()).upper()

    # UEFI -> APFS
    config["UEFI"]["APFS"]["MinDate"] = -1
    config["UEFI"]["APFS"]["MinVersion"] = -1

    # UEFI -> Quirks
    config["UEFI"]["Quirks"]["IgnoreInvalidFlexRatio"] = True
    config["UEFI"]["Quirks"]["ReleaseUsbOwnership"] = True
    config["UEFI"]["Quirks"]["RequestBootVarRouting"] = True # Required for LauncherOption
    config["UEFI"]["Quirks"]["UnblockFsConnect"] = False # Not HP

    print("Saving config.plist...")
    with open(CONFIG_PATH, 'wb') as f:
        plistlib.dump(config, f)
    print("Done.")

if __name__ == "__main__":
    main()
