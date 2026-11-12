# NOVA Glass Atmosphere Ultra 2.1.0

A refined transparent Liquid Glass overlay for iPhone 5s / iOS 12.5.8, designed for Xen HTML.

## Visual redesign
- Soft blue-white aurora ribbons and a moving prismatic glass orb.
- Fine edge reflections and low-opacity bottom haze; the wallpaper remains visible.
- Warm, restrained sunlight with slow moving rays.
- Fine snowfall, delicate rain streaks, subtle autumn leaves and tiny glass-like glints.
- No opaque wallpaper replacement, labels, panels or touch-blocking controls.

## Install
1. Install the iOS 12-compatible Xen HTML release from a trusted repository.
2. Install `com.nova.glass.atmosphere_2.1.0_iphoneos-arm.deb` with Sileo.
3. Open Settings > Xen HTML.
4. Enable NOVA Glass Atmosphere Ultra on the Home Screen and/or Lock Screen.
5. Keep the widget full-screen and in the wallpaper layer.

## Installed paths
- Home Screen: `/var/mobile/Library/SBHTML/NOVA-Glass-Atmosphere/Wallpaper.html`
- Lock Screen: `/var/mobile/Library/LockHTML/NOVA-Glass-Atmosphere/LockBackground.html`
- Xen HTML 2: `/var/mobile/Library/Widgets/Universal/NOVA-Glass-Atmosphere/index.html`

## Compatibility and performance
- Target: arm64, rootful jailbreak, iOS 12.0+.
- Canvas animation is throttled to about 30 FPS.
- Canvas pixel ratio is capped at 1.25 to limit memory use on iPhone 5s.
- All effects are pointer-events:none; Home Screen icons and Lock Screen controls remain usable.
- Transparent background preserves the user's wallpaper.
