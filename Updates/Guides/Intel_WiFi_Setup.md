# Intel Wi-Fi Setup Guide (Intel Centrino Advanced-N 6300)

Your ThinkPad X220 is equipped with the **Intel Centrino Advanced-N 6300**. This card is supported in macOS Monterey using the **OpenIntelWireless** project.

## Required Kexts & Tools

I have downloaded the following for you in the `Updates` folder:

1.  **AirportItlwm.kext** (Monterey version): Located in `Updates/Kexts/AirportItlwm_Monterey.zip`.
    *   *Usage:* Enables native macOS Wi-Fi menu integration.
    *   *Installation:* Add to `EFI/OC/Kexts` and enable in `config.plist`.

2.  **HeliPort.dmg**: Located in `Updates/Tools/HeliPort.dmg`.
    *   *Usage:* A client app for `itlwm.kext`. Not strictly required if using `AirportItlwm`, but useful for diagnostics or if you switch to the standard `itlwm.kext` for stability.

## Installation Instructions

1.  **Extract Kext**: Unzip `Updates/Kexts/AirportItlwm_Monterey.zip`.
2.  **Copy to EFI**: Copy `AirportItlwm.kext` to your `EFI/OC/Kexts/` folder.
3.  **Update Config**:
    *   Open your `config.plist` with **ProperTree**.
    *   Perform a "Clean Snapshot" (Ctrl+Shift+R) to add the new kext.
    *   **Important:** Ensure `AirportItlwm.kext` is loaded *after* `IO80211Family.kext` (if present, though usually it's not explicitly listed in OC). Just make sure it's in the Kernel -> Add list.
4.  **Reboot**: Restart your computer.

## Troubleshooting

*   **Experimental Support**: The Centrino 6300 is an older card (Gen 1/2). Support is considered "Experimental". If you experience instability or kernel panics with `AirportItlwm`, try switching to the standard `itlwm.kext` (available on the [OpenIntelWireless GitHub](https://github.com/OpenIntelWireless/itlwm/releases)) and use the **HeliPort** app to connect to Wi-Fi.
*   **Performance**: Speeds might be lower than in Windows due to the nature of the driver emulation.

## Resources

*   **Official Guide**: [OpenIntelWireless Installation Guide](https://openintelwireless.github.io/itlwm/Installation.html)
*   **GitHub Repo**: [https://github.com/OpenIntelWireless/itlwm](https://github.com/OpenIntelWireless/itlwm)
