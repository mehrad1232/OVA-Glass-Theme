# NOVA Glass Theme — iOS 12 / iPhone 5s

NOVA Glass is a SnowBoard icon theme with a separate SpringBoard weather-effects tweak.

## v4.0
- Redesigned glossy glass-style icon art and transparent rounded edges.
- Six static iPhone 5s wallpapers plus full-size source masters.
- NOVAWeather tweak: sunlight 07:00–14:00, snow 19:00–07:00, device-local time.
- The HTML file is only a browser preview; the live effect comes from the tweak.

## Build
GitHub Actions generates the icon/wallpaper artwork, validates dimensions and plist metadata, builds the rootful iOS 12 arm64 tweak with Theos, packages both into an artifact, and computes SHA-256 checksums.

## Device validation
CI can verify asset structure and compile/package the tweak. It cannot prove the tweak runs correctly on a physical iPhone 5s / iOS 12.5.8 / Amethyst. The first install must be tested on that device. The tweak is designed for rootful jailbreaks with MobileSubstrate-compatible injection and hooks SpringBoard's SBFStaticWallpaperView.

See NOVA Glass.theme/README.md and NOVAWeather/README.md for install instructions and limitations.
