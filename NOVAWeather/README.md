# NOVA Glass for Messages 3.0

A Messages-only glass redesign for rootful arm64 iOS 12, targeting iPhone 5s / iOS 12.5.8.

## Visual treatment
- UIKit blur through UIVisualEffectView and UIBlurEffect, with a separate ice-blue tint, gradient sheen and fine glass border.
- ChatKit balloon styling for incoming and outgoing message surfaces.
- Frosted composer and translucent navigation / toolbar.
- Conversation-list glass cards and an icy background.
- Optional low-rate falling snow behind transcript and conversation-list content.
- Independent switches for bubbles, composer, conversation list, ice-blue tint and snowfall.

## Install
Build with Theos or download the GitHub Actions artifact. Install the .deb using Sileo, then force-close and reopen Messages. Settings are under Settings > NOVA Messages.

## Compatibility and limitations
- Target: iPhone 5s, arm64, iOS 12.0–12.5.8, rootful jailbreak.
- Injection filter is restricted to com.apple.MobileSMS; SpringBoard and other apps are not injected.
- ChatKit is a private framework. Class names and view composition can vary between iOS builds; this tweak matches known ChatKit view families at runtime.
- The effect approximates modern Liquid Glass with iOS 12 UIKit blur and translucent layers; it is not Apple's later native Liquid Glass system.
- A successful compile does not replace testing on the actual iPhone 5s. If a view is not matched by the installed iOS build, its appearance will remain native.

To disable: turn off Enable NOVA Glass or uninstall the package from Sileo.
