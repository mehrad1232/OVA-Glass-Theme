# NOVA Glass — technical research and implementation notes

Target hardware/software: iPhone 5s (arm64), iOS 12.5.8, rootful Amethyst jailbreak, Sileo, SnowBoard.

## 1. Architecture

NOVA Glass is split into three installable parts, assembled into one ZIP by GitHub Actions:

1. **SnowBoard theme** — app icons, Settings icons and static wallpapers.
2. **NOVAWeather Debian tweak** — a Theos/Logos Objective-C tweak injected into SpringBoard. It draws a time-aware overlay and subtle glass treatment on supported SpringBoard surfaces.
3. **NOVA ringtone** — an original short audio composition generated from source code and converted to AAC/M4R. The unified build stages it in `/Library/Ringtones` inside the Debian package.

The complete workflow packages the theme, tweak and ringtone together. The source project remains editable.

## 2. Why rootful arm64

The iPhone 5s uses 64-bit ARM (arm64) and iOS 12.5.8. This project targets the classic rootful jailbreak filesystem. It does not use the modern rootless `/var/jb` layout: Theos documents rootless as a newer scheme that targets iOS 15+ devices. The Makefile therefore sets `ARCHS = arm64`, an iOS 12 deployment target and ordinary rootful install paths.

## 3. SnowBoard theme format

SnowBoard themes use a folder ending in `.theme`, with an `IconBundles` directory and an `Info.plist`. The plist declares `PackageName` and `ThemeType = Icons`. Icon image names are bundle identifiers, so an icon only applies when the installed app's identifier matches.

iOS 12 Settings icons are placed under `Bundles/com.apple.preferences-framework`; regular iPhone models such as iPhone 5s use 58x58 @2x and 87x87 @3x assets. SnowBoard's Settings Icons extension is needed to apply those assets.

The artwork generator draws app-specific pictograms (phone, messages, camera, mail, maps, music, etc.) on a shared glass visual system. It does not use a font letter/monogram as the icon artwork. Third-party app identifiers are best-effort and can vary by app release.

## 4. Theos and Logos

Theos is the build system. Logos is the hook preprocessor used to replace/extend Objective-C methods through MobileSubstrate. The tweak is filtered to `com.apple.springboard`, so it is loaded into SpringBoard rather than every application.

The tweak currently:
- Adds a soft daylight glow between 07:00 and 13:59 local device time.
- Emits animated snow particles between 14:00 and 06:59.
- Adds a subtle glass edge/sheen to SpringBoard icon image views.
- Adds a low-opacity glass panel to the lock-screen cover sheet and Control Center when their expected iOS classes are present.
- Exposes an enable/disable switch in Settings through a PreferenceLoader bundle. The tweak and settings pane share the `com.nova.glass.weather` defaults suite.

Private SpringBoard class names and view lifecycles are not public APIs. The hooks are conditional where possible, but runtime behavior must be verified on the exact jailbreak and iOS build before treating the package as safe. A compile success is not a device test.

## 5. Live effects versus wallpaper

The six PNG wallpapers are static, correctly sized artwork for the iPhone 5s display. `Wallpaper-Preview.html` is a browser preview only. The actual time-dependent sunlight/snow effect is drawn by the SpringBoard tweak; it is not an HTML wallpaper and does not depend on the browser staying open.

## 6. Ringtone

The ringtone source is `tools/generate_ringtone.py`. It synthesizes an original melody as PCM WAV. CI converts it to AAC in an M4R container and places it at `/Library/Ringtones/NOVA Glass.m4r` in the Debian package. iOS ringtone handling has historical/private registration details, so availability in Settings must still be confirmed on-device after installation. Keep the original tone file and back up existing system sounds.

## 7. Build

GitHub Actions on macOS:
1. Installs Pillow, FFmpeg, ldid and dpkg.
2. Generates the SnowBoard icon/wallpaper artwork.
3. Generates and converts the original ringtone.
4. Installs Theos.
5. Compiles the rootful iOS 12 tweak and preference bundle.
6. Packages the ringtone into the Debian package.
7. Creates one ZIP containing the theme folder, .deb, ringtone and installation notes.

The artifact's successful creation confirms the automated build/package steps only. It does not prove visual quality, bundle-ID matching for every third-party app, or runtime stability on a physical iPhone.

## 8. Safe installation / recovery

- Make an iTunes/iMazing backup first.
- Install the .deb using Sileo.
- Copy `NOVA Glass.theme` into `/Library/Themes/` and enable it in SnowBoard.
- Respring once.
- If SpringBoard becomes unstable, enter safe mode or use SSH/NewTerm to remove package `com.nova.glass.weather`, then respring.
- Do not replace SpringBoard.app assets or system frameworks manually.

## 9. Known boundaries

- This is not a full system-wide replacement of every UIKit surface. The Control Center and lock-screen treatment is a restrained overlay; it does not redesign their controls.
- Gestures, fonts, notification banners, status bar and every Settings subpage are not all independently themed by this initial implementation.
- App icon coverage depends on actual installed bundle IDs.
- The time schedule uses the device's local clock.
- iOS 12.5.8 + Amethyst runtime compatibility has not been certified by a physical-device test.
