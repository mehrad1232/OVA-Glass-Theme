# NOVA Glass Weather Effects — iOS 12

This rootful Theos tweak is a separate companion to the SnowBoard icon theme.

## Behavior
- Sunlight: radial warm light from the top of the wallpaper view from 07:00 inclusive to 14:00 exclusive, using the device's local clock.
- Snow: animated Core Animation emitter from 19:00 inclusive through 06:59 local time.
- 14:00–18:59: neither sunlight nor snowfall.
- The overlay is attached to SpringBoard's SBFStaticWallpaperView; it does not alter app icons or app UI.

## Compatibility and limitations
- Build target: iOS 12.0+, rootful jailbreak, arm64; intended for iPhone 5s / iOS 12.5.8 and Amethyst with MobileSubstrate-compatible injection.
- SnowBoard is needed for the icon theme, not for this tweak.
- This is not a WinterBoard HTML wallpaper. The effect is implemented by a SpringBoard tweak.
- The source and package can be build-validated in CI, but runtime behavior must still be verified on the actual iPhone 5s. A successful .deb build alone is not proof of device compatibility.
- If SBFStaticWallpaperView changes in a jailbreak/SpringBoard build, the tweak will not attach. Disable or uninstall the package to recover; it has no preference pane or safe-mode dependency.

## Build
Run make clean package FINALPACKAGE=1 with Theos and an iOS SDK installed. CI uses the macOS Theos toolchain to produce a rootful package. Physical-device testing is still required. The package uses the rootful iphoneos-arm Debian architecture.

CI runs on the v4 build branch as well as main, using Ubuntu 22.04 for Theos.
