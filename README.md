# NOVA Glass — iOS 12 / iPhone 5s

NOVA Glass is a rootful SnowBoard icon theme for legacy iOS, with six static wallpapers and a separate experimental SpringBoard weather-effects companion.

## What is included
- `NOVA Glass.theme/`: theme package. `tools/build_theme.py` generates icon PNGs, wallpapers, artwork masters, and preview.
- `NOVAWeather/`: companion tweak documentation. This folder currently contains documentation only; it is **not** a built or installable tweak package.
- `.github/workflows/main.yml`: GitHub Actions packaging workflow.

## Build the theme
The workflow installs Pillow, runs `python3 tools/build_theme.py`, validates file counts and image dimensions, and creates a ZIP artifact. This validation is a packaging check; it does not prove that every icon matches an installed app's bundle identifier or that the artwork has been visually reviewed on an iPhone.

1. Open the repository's **Actions** tab.
2. Select the latest successful **Build NOVA Glass Theme** run.
3. Download the `NOVA-Glass-Theme-iOS12-v3.0` artifact and extract it.
4. Copy `NOVA Glass.theme` to `/Library/Themes/` on the jailbroken device.
5. Enable it in SnowBoard, then respring.
6. Set one of the included PNG wallpapers manually in Settings or Photos.

## iOS 12 / SnowBoard install
Use a rootful jailbreak and SnowBoard compatible with iOS 12.5.8. Transfer the extracted folder using trusted SSH/SFTP or Filza. Back up the original theme before replacing anything. If icons don't change, check the app's actual bundle identifier and confirm SnowBoard icon theming is enabled.

## Scope and limitations
- This is an icon-and-wallpaper theme. It does not independently theme Control Center, lock-screen layout, system UI, gestures, fonts, or ringtones.
- Third-party icons are best-effort: SnowBoard only matches an icon if its filename corresponds to the installed app's bundle identifier. App updates can change identifiers.
- Wallpapers are ordinary static PNGs. The HTML preview is a browser preview, not an iOS live wallpaper.
- The current generator draws stylized glass/gradient monogram icons. They are generated placeholders, not individually hand-designed app glyphs; the repository does not include a vetted icon source pack.
- `NOVAWeather` is documentation-only. No tweak source, Theos Makefile, control file, or .deb is included. Do not install it expecting sunlight/snow overlays to run.
- No runtime device test has been performed as part of this update.

## Custom ringtone (iOS 12)
The theme does not install ringtones. Safest workflow:
1. On Windows, prepare a short audio file (AAC/M4A, preferably <=30 seconds).
2. Convert it to ringtone format `.m4r` (AAC audio with the .m4r extension).
3. Transfer it to iPhone using a trusted ringtone manager / supported iTunes workflow, or a compatible jailbreak ringtone tool.
4. Back up existing ringtone files before any manual filesystem replacement. Avoid overwriting system sounds blindly.
5. Select the installed tone in Settings > Sounds.

Ringtone tools and iOS 12 compatibility vary. Confirm compatibility before installing packages; don't assume a tweak built for modern iOS works on 12.5.8.

## Contributions
Include source artwork, app bundle identifier, license/attribution, and device/OS compatibility notes for new icons. For code changes, build the artifact and inspect it before claiming device compatibility.
