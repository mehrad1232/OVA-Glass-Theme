# NOVA Glass Weather & UI Tweak

Rootful iOS 12 / arm64 Theos tweak source. The tweak adds a time-aware overlay:
- 07:00–13:59: soft daylight glow.
- 14:00–06:59: animated snow emitter.
- A subtle glass surface on Lock Screen and Control Center when the relevant iOS 12 classes exist.

## Build
Run `make package` with Theos installed and an iOS SDK/toolchain available. GitHub Actions builds the .deb on macOS and uploads it as an artifact.

## Important limitations
This is a best-effort private-API tweak. SpringBoard, lock-screen and Control Center class names and view lifecycles are private implementation details and can vary across iOS point releases and jailbreak substrate versions. The overlay is non-interactive; it does not replace system controls. A successful compile is not proof of runtime stability. Keep a way to disable/remove the package through Sileo or SSH.

Preference key: `com.nova.glass.enabled` (NSUserDefaults, default YES).
