# NOVA Glass Complete Edition — iPhone 5s / iOS 12.5.8

A rootful arm64 glass-style customization project for iOS 12.5.8 and Amethyst.

## Components
- **SnowBoard theme:** glass-style app icons, iOS 12 Settings glyphs and iPhone 5s wallpapers.
- **Messages tweak:** optional ChatKit bubble, composer and conversation-list styling; injection is restricted to `com.apple.MobileSMS`.
- **System Experience tweak:** optional best-effort glass styling for selected Lock Screen, Control Center and Phone call UI surfaces.
- **Original ringtone:** generated NOVA Glass M4R, packaged into the System Experience DEB and also provided separately.
- **Lock Screen widget:** optional Xen HTML clock/date widget with subtle frost animation.
- **Seasonal widget:** optional Xen HTML four-season widget with automatic and manual season selection.

## Build
GitHub Actions builds the complete theme, Messages DEB, System Experience DEB, ringtone and ZIP artifacts. See [Build NOVA Glass Complete Edition](.github/workflows/build-complete.yml).

## Install
1. Extract the complete ZIP.
2. Copy `NOVA Glass.theme` to `/Library/Themes/` and enable it in SnowBoard.
3. Install the Messages DEB from Sileo if you want the Messages effects.
4. Install the System Experience DEB only after making a device backup; it touches selected SpringBoard/Control Center/Phone view classes.
5. Choose `NOVA-Glass-Ringtone.m4r` in Settings > Sounds.
6. Install an iOS 12-compatible Xen HTML release separately before enabling either optional widget.

## Compatibility and limitations
- Target: iPhone 5s (arm64), iOS 12.5.8, rootful Amethyst.
- iOS 12 does not contain Apple's later native Liquid Glass framework; effects are recreated with UIKit blur, translucent layers and highlights.
- ChatKit, Lock Screen, Control Center and Phone UI contain private classes whose names can vary by iOS build. The optional system tweak uses conservative runtime matching; unsupported surfaces stay native.
- Xen HTML is optional and is not included as a dependency.
- A successful GitHub Actions build proves compilation and packaging only. It does not prove that every private UI class matches on the physical iPhone. Test optional system styling after a backup and keep Sileo available for removal.

## Project layout
- `NOVA Glass.theme/` — SnowBoard assets.
- `NOVAWeather/` — Messages tweak.
- `NOVAExperience/` — Lock Screen / Control Center / Phone UI tweak and ringtone packaging.
- `XenHTML/` — optional HTML widgets.
- `tools/` — artwork and ringtone generators.
