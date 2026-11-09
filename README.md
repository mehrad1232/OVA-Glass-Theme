# NOVA Glass — iPhone 5s / iOS 12

Unified rootful jailbreak customization for iPhone 5s / iOS 12.5.8: SnowBoard icons, SpringBoard weather effects, editable settings and an original ringtone.

## Features
- SnowBoard app and Settings icon theme.
- Home Screen sunlight glow from 07:00 to 13:59 and snowfall from 14:00 to 06:59.
- Independent Settings switches for master effects, sunlight and snowfall; changes apply immediately.
- Touch-through overlays placed behind Home Screen content. Control Center is deliberately left unobstructed so its controls remain usable.
- Original NOVA ringtone.

## Build
Open Actions → Build NOVA Glass Complete iOS 12 Package and download the `NOVA-Glass-Full-iOS12` artifact. The package targets rootful arm64 and iOS 12.

## Install
1. Back up the iPhone.
2. Install the new `com.nova.glass.weather` Debian package in Sileo as an upgrade.
3. Enable NOVA Glass in SnowBoard.
4. Open Settings → NOVA Glass and choose the three effect switches.

## Safety
This tweak uses private SpringBoard classes. A successful GitHub build proves compilation and packaging, not runtime certification. Test on iPhone 5s / iOS 12.5.8. If SpringBoard becomes unstable, remove `com.nova.glass.weather` in Sileo or over SSH and respring.
