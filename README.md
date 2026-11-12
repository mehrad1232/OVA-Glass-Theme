# NOVA Glass Complete Edition — iPhone 5s / iOS 12.5.8

A rootful arm64 glass-style customization project for iOS 12.5.8 and Amethyst.

## Components
- **SnowBoard theme:** glass-style app icons, iOS 12 Settings glyphs and iPhone 5s wallpapers.
- **Messages tweak:** NOVA Messages 3.2.2 hooks ChatKit layout overrides and provides selectable snow, rain, animated sunlight and falling autumn leaves; injection is restricted to com.apple.MobileSMS.
- **System Experience tweak:** optional best-effort glass styling for selected Lock Screen, Control Center and Phone call UI surfaces.
- **Original ringtone:** generated NOVA Glass M4R, packaged into the System Experience DEB and also provided separately.
- **Lock Screen widget:** optional Xen HTML clock/date widget with subtle frost animation.
- **Seasonal widget:** optional Xen HTML four-season widget with automatic and manual season selection.

## Build
GitHub Actions builds the complete theme, Messages DEB, System Experience DEB, ringtone and ZIP artifacts. See the build-complete workflow in .github/workflows.

## Install
1. Extract the complete ZIP.
2. Copy NOVA Glass.theme to /Library/Themes/ and enable it in SnowBoard.
3. Install the Messages DEB from Sileo if you want the Messages glass and atmosphere effects.
4. Open Settings > NOVA Messages and enable the effects you want: snow, rain, sunlight or autumn leaves.
5. Install the System Experience DEB only after making a device backup; it touches selected SpringBoard/Control Center/Phone view classes.
6. Choose NOVA-Glass-Ringtone.m4r in Settings > Sounds.
7. Install an iOS 12-compatible Xen HTML release separately before enabling either optional widget.

## Compatibility and limitations
- Target: iPhone 5s (arm64), iOS 12.5.8, rootful Amethyst.
- iOS 12 does not contain Apple's later native Liquid Glass framework; effects are recreated with UIKit blur, translucent layers and highlights.
- Snow, rain and leaves use Core Animation particle emitters; sunlight uses animated gradient layers.
- ChatKit, Lock Screen, Control Center and Phone UI contain private classes whose names can vary by iOS build. The Messages tweak uses runtime class-family matching; unsupported surfaces stay native.
- Xen HTML is optional and is not included as a dependency.
- A successful GitHub Actions build proves compilation and packaging only. It does not prove that every private UI class matches on the physical iPhone. Test on the target device and keep Sileo available for removal.

## Project layout
- NOVA Glass.theme/ — SnowBoard assets.
- NOVAWeather/ — Messages tweak.
- NOVAExperience/ — Lock Screen / Control Center / Phone UI tweak and ringtone packaging.
- XenHTML/ — optional HTML widgets.
- tools/ — artwork and ringtone generators.
