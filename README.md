# NOVA Glass — iPhone 5s / iOS 12.5.8

NOVA Glass is a glass-style customization project for rootful arm64 iOS 12.5.8 and Amethyst.

## Home Screen + Lock Screen atmosphere
The NOVA Glass Atmosphere add-on places transparent animation over the wallpaper on both SpringBoard Home Screen and Lock Screen:
- Falling snow
- Fine rain
- Warm sunlight and moving light rays
- Falling autumn leaves

All four effects run together by default. They are drawn on a transparent Xen HTML layer, behind Home Screen icons and above the Lock Screen wallpaper. This add-on does not target Apple Messages.

## Install the atmosphere add-on
1. Install an iOS 12-compatible Xen HTML release from a trusted repository.
2. Install the com.nova.glass.atmosphere_2.0.0_iphoneos-arm.deb package with Sileo.
3. In Settings > Xen HTML, enable NOVA Glass Atmosphere for both Home Screen wallpaper and Lock Screen wallpaper.

The package includes legacy Xen HTML 1.x files and the Xen HTML 2 Universal index.html location. SnowBoard alone cannot render HTML widgets.

## Theme components
- NOVA Glass.theme/ — SnowBoard icons, Settings glyphs and wallpapers.
- XenHTML/NOVA-Atmosphere/ — transparent Home Screen / Lock Screen animated atmosphere.
- XenHTML/NOVA-Glass-Seasons/ — optional seasonal widget.
- XenHTML/NOVA-LockScreen/ — optional clock/date widget.

## Compatibility
- Target: iPhone 5s (arm64), iOS 12.5.8, rootful Amethyst.
- The atmosphere add-on is a Xen HTML widget, not a native tweak. It requires Xen HTML to be installed and enabled at both wallpaper locations.
- It does not inject into Messages or modify private ChatKit classes.
- On the Lock Screen, Xen HTML wallpaper widgets are non-touch layers by design; the visual effects remain animated without taking over lock-screen controls.
