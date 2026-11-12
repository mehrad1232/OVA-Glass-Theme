# NOVA Glass Atmosphere for Home Screen + Lock Screen

A transparent animated wallpaper overlay for iPhone 5s / iOS 12.5.8.

## Included live effects
- Snowfall: small drifting flakes with varied size, speed and opacity.
- Rain: fine diagonal blue-white rain streaks.
- Sunlight: warm radial glow and slow moving rays.
- Autumn leaves: orange/amber leaves that rotate and drift in a light wind.
- All four effects run together by default. There is no opaque wallpaper replacement and no touch-blocking overlay.

## Correct platform
This is a Xen HTML wallpaper widget, not a Messages tweak and not a SnowBoard theme.
Xen HTML is the component that places HTML between the wallpaper and SpringBoard icons or above the Lock Screen wallpaper. It supports iOS 9–12.

## Install
1. Install an iOS 12-compatible Xen HTML release from a trusted repository. SnowBoard alone cannot render HTML widgets.
2. Install com.nova.glass.atmosphere_2.0.0_iphoneos-arm.deb with Sileo.
3. Open Settings > Xen HTML.
4. Enable NOVA Glass Atmosphere for the Home Screen wallpaper location.
5. Enable NOVA Glass Atmosphere for the Lock Screen wallpaper location.
6. Keep the widget full-screen and behind icons/controls. The Lock Screen wallpaper location is a non-touch widget layer by Xen HTML design.

The DEB includes:
- Legacy Home Screen entry: /var/mobile/Library/SBHTML/NOVA-Glass-Atmosphere/Wallpaper.html
- Legacy Lock Screen entry: /var/mobile/Library/LockHTML/NOVA-Glass-Atmosphere/LockBackground.html
- Xen HTML 2 Universal entry: /var/mobile/Library/Widgets/Universal/NOVA-Glass-Atmosphere/index.html

The same transparent animation runs on both screens. You can enable either location or both.

## Technical details
- Canvas 2D animation, throttled to roughly 30 frames per second.
- Canvas pixel ratio is capped at 1.35 to reduce memory/bandwidth on older hardware.
- The WebView and canvas backgrounds are transparent; no opaque content hides the wallpaper.
- Pointer events are disabled for the overlay so home icons and lock-screen controls remain usable.
- Does not inject into Messages, modify ChatKit, or hook SpringBoard classes.
- The widget requires Xen HTML. Installing the DEB without Xen HTML will only place the files; nothing will render until the widget engine is installed and the two locations are enabled.
