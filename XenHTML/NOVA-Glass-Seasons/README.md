# NOVA Glass Seasons — Xen HTML add-on

Optional animated four-season overlay for iOS 9–12 devices running Xen HTML.

## Features
- Automatic season based on the device's local month (March–May spring, June–August summer, September–November autumn, December–February winter).
- Manual Spring / Summer / Autumn / Winter override.
- One-tap return to automatic mode.
- Seasonal CSS particles: petals, summer light motes, falling leaves, and snow.
- Lightweight CSS animation; respects prefers-reduced-motion.

## Install
1. Install a compatible Xen HTML release for iOS 12 from a trusted repository. This add-on does not install or modify Xen HTML.
2. Copy the folder `NOVA-Glass-Seasons` into `/var/mobile/Library/SBHTML/`.
3. In Xen HTML, enable this widget as a Home Screen background widget. Test it on the Lock Screen separately if desired.
4. Tap the small ✧ control at the lower right to choose a season. Choose “Use automatic season” to return to date-based mode.

## Safety and compatibility
- This is a separate Xen HTML widget. SnowBoard alone does not execute this HTML.
- It does not inject a tweak, modify SpringBoard binaries, change Settings layout, or install a preference bundle.
- Local season choice is stored in WebKit localStorage. If Xen HTML's WebView data is cleared, the choice resets to automatic.
- Performance and touch interaction must be verified on the target iPhone 5s / iOS 12.5.8.
