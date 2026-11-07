# NOVA Glass Theme v2.0

A SnowBoard icon theme and native-resolution wallpaper asset pack for jailbroken iOS 12 devices, including iPhone 5s (640x1136).

## Included
- 30 native PNG app icons in IconBundles, named by iOS bundle identifier
- 640x1136 iPhone 5s wallpaper in Wallpapers
- Wallpaper-Preview.html with a glass clock preview and day/night snow toggle
- Existing frosted-glass HTML concept and theme metadata
- Build-time checks for plist validity, icon count, PNG dimensions, and package size

## Build
GitHub Actions runs tools/build_theme.py, validates every generated PNG and creates NOVA-Glass-Theme-iOS12-v2.0.zip. The package is required to be at least 1.8 MB; this is real image content, not a padded placeholder.

## Install
1. Download the NOVA-Glass-Theme-iOS12-v2.0 artifact from the successful GitHub Actions run.
2. Extract NOVA Glass.theme.
3. Copy the folder to /Library/Themes/ on the jailbroken device.
4. Open SnowBoard, enable NOVA Glass, and respring if needed.

## Compatibility notes
- The icon files use common iOS stock bundle identifiers and standard PNG assets. SnowBoard's exact icon lookup can vary by iOS build and installed app bundle IDs; verify icons on-device.
- The wallpaper PNG is a normal image asset. SnowBoard does not automatically turn an HTML file into a live wallpaper. Set the PNG as wallpaper using iOS Photos/Settings.
- This package does not install Control Center, lock-screen, gesture, or ringtone tweaks. Those require separate iOS 12-compatible tweaks and are intentionally not misrepresented as included.

## Source
The icon and wallpaper assets are generated locally by tools/build_theme.py with Pillow. No external copyrighted icon pack is bundled.
