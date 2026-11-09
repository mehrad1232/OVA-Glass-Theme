# NOVA Glass — complete iPhone 5s / iOS 12 project

NOVA Glass is a unified rootful jailbreak customization project for **iPhone 5s / iOS 12.5.8**. It combines a SnowBoard theme, a Theos/Logos SpringBoard tweak, a PreferenceLoader settings pane and an original ringtone.

## Repository structure

- `NOVA Glass.theme/` — SnowBoard theme, generated app icons, Settings icons, wallpapers and editable artwork.
- `NOVAWeather/` — Objective-C/Logos tweak, Theos Makefile, Debian control metadata, PreferenceLoader bundle and install layout.
- `tools/build_theme.py` — base artwork and wallpaper generation.
- `tools/build_complete_artwork.py` — recognizable app pictograms and iOS 12 Settings icon variants.
- `tools/generate_ringtone.py` — original NOVA ringtone source generator.
- `.github/workflows/build-complete.yml` — one workflow that builds and packages all deliverables.
- `docs/RESEARCH-AND-ARCHITECTURE.md` — implementation research, compatibility notes, installation and recovery.

## Features implemented in source

- SnowBoard app icons matched by bundle ID, plus iOS 12 Settings icon assets.
- Six static iPhone 5s wallpapers.
- SpringBoard daylight glow from 07:00 to 13:59 and animated snow from 14:00 to 06:59.
- Subtle glass edge treatment for SpringBoard icon image views.
- Best-effort translucent glass overlays on the iOS cover sheet and Control Center when their private classes are present.
- Settings toggle for enabling/disabling the weather effects.
- Original 24-second ringtone generated from source and staged in `/Library/Ringtones`.
- One ZIP artifact containing the theme, installable Debian package and installation instructions.

## Build / download

Open **Actions → Build NOVA Glass Complete iOS 12 Package**. Download the artifact named `NOVA-Glass-Full-iOS12`. The ZIP contains:
- `NOVA Glass.theme/`
- `Packages/com.nova.glass.weather_*.deb`
- `NOVA-Glass-Ringtone.m4r`
- `INSTALL.txt`

The package targets rootful arm64. It is not a rootless package.

## Install

1. Back up the device.
2. Install the single included `.deb` with Sileo. It installs the SnowBoard theme, SpringBoard tweak, preference pane and ringtone into their rootful locations.
3. Open SnowBoard and enable NOVA Glass (enable the Settings Icons extension if available).
4. Respring if Sileo has not already restarted SpringBoard.
5. Choose NOVA Glass in Settings → Sounds if iOS has registered the tone.

## Compatibility and honest status

This repository contains actual source code and automated packaging, not only a mock-up. However, SpringBoard, Lock Screen and Control Center are private iOS internals. The tweak uses conditional hooks and must be verified on the exact Amethyst/Sileo/iOS 12.5.8 combination before it can be called runtime-certified. A green GitHub build proves compilation and packaging, not safe runtime behavior.

Some third-party icon filenames may need adjustment to match the installed app's exact bundle ID. The glass overlay is a restrained visual treatment; it does not replace every system UI screen, add new gestures, or redesign every notification/status-bar element. The HTML wallpaper preview is for desktop preview only; the actual clock-based weather effect comes from the tweak.

If SpringBoard becomes unstable, remove `com.nova.glass.weather` from Sileo or through SSH and respring. Do not manually overwrite system frameworks or SpringBoard.app assets.

## Research

See [docs/RESEARCH-AND-ARCHITECTURE.md](docs/RESEARCH-AND-ARCHITECTURE.md) for technical decisions and references to Theos, Logos, SnowBoard, PreferenceLoader and iOS ringtone format.
