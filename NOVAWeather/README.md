# NOVA Glass for Messages

A Messages-only visual tweak for Apple Messages (com.apple.MobileSMS) on rootful arm64 iOS 12.

## What it styles
- Frosted, translucent navigation and toolbar appearance.
- Incoming and outgoing conversation balloon surfaces with rounded glass edges.
- The message composer / input surface.
- Conversation list cells and background.
- Independent switches for the main effect, bubbles, composer and conversation list.

## Install
Build the Debian package with Theos or download the GitHub Actions artifact. Install the .deb using Sileo, force-close Messages, then reopen it. Settings are under **Settings > NOVA Messages**.

## Compatibility and limitations
Designed for iPhone 5s on iOS 12.5.8, arm64, rootful jailbreak. The visual treatment approximates Liquid Glass using UIKit blur and translucent layers; iOS 12 cannot run Apple's newer native Liquid Glass framework. Messages uses private view classes, so balloon and composer matching must be verified on the actual device. A successful compile is not proof of runtime compatibility.

This project intentionally does not inject into SpringBoard or change the Home Screen, Lock Screen, weather, icons, ringtone, or other applications.
