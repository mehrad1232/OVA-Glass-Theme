# NOVA Glass for Messages 3.2.2.2

Weather and glass effects for Apple Messages on rootful arm64 iOS 12, targeting iPhone 5s / iOS 12.5.8.

## Atmosphere effects
- **Snow:** fine six-arm flakes with slow drift and fade.
- **Rain:** angled blue-white drops with varied speed and falloff.
- **Sunlight:** warm radial glow and gently animated light beams.
- **Autumn leaves:** orange leaves with wind drift and natural spin.
- Each effect has its own switch in Settings > NOVA Messages. Effects may be combined.

## Glass treatment
- UIKit blur through UIVisualEffectView and UIBlurEffect.
- Ice-blue translucent tint, gradient sheen and subtle border.
- ChatKit balloon styling for incoming and outgoing message surfaces.
- Frosted composer and translucent navigation / toolbar.
- Conversation-list glass cards and an icy background.

## Technical approach
- Core Animation CAEmitterLayer / CAEmitterCell drives snow, rain and leaf particles.
- CAGradientLayer and CABasicAnimation create the sunlight glow and moving rays.
- The atmosphere overlay is non-interactive and inserted behind scroll content to keep text and buttons readable.
- The tweak is filtered to com.apple.MobileSMS; it does not inject into SpringBoard or other apps.
- Runtime class enumeration hooks concrete ChatKit layoutSubviews overrides as well as UIView's base layout method.

## Install
Build with Theos or download the GitHub Actions artifact. Install the .deb with Sileo, then force-close and reopen Messages. Settings are under Settings > NOVA Messages.

## Compatibility and limitations
- Target: iPhone 5s, arm64, iOS 12.0–12.5.8, rootful jailbreak.
- iOS 12 does not contain Apple's later native Liquid Glass framework; glass is recreated with iOS 12 UIKit blur and translucent layers.
- ChatKit is private. Class names and view composition can vary by iOS build; runtime matching is best-effort and must be validated on the actual iPhone.
- Particle rates are kept modest for older hardware. Turning off an effect removes its animation layer.
- A successful compile and package validation do not prove that every private ChatKit surface matches on the physical device.

To disable: turn off Enable NOVA Glass or uninstall the package from Sileo.
