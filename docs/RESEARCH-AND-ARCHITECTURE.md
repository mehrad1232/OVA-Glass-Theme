# NOVA Glass — technical research and implementation notes

Target: iPhone 5s, iOS 12.5.8, rootful Amethyst, Sileo and SnowBoard.

## Runtime behavior

- The weather overlay is attached to the SpringBoard icon controller's own view, inserted behind its content. This keeps the effect on the Home Screen rather than whichever window happens to be key while SpringBoard launches.
- The Lock Screen receives only a restrained, touch-through glass treatment.
- The full-screen Control Center overlay was removed so Control Center controls remain visible and usable.
- All overlays are non-interactive and inserted behind host content.
- Preferences are stored in the `com.nova.glass.weather` defaults suite and broadcast through a Darwin notification. Changes apply immediately without a respring.

## Settings

Settings → NOVA Glass exposes three switches:
- Enable NOVA effects
- Daylight glow (07:00–13:59)
- Night snowfall (14:00–06:59)

The schedule follows the device's local clock. Each weather switch can be controlled independently.

## Build and installation

The GitHub Actions workflow builds the rootful arm64 package for iOS 12 and packages the SnowBoard theme and ringtone with it. Install the newly generated `.deb` in Sileo as an upgrade. Back up the device first.

## Compatibility note

The tweak uses private SpringBoard classes. A successful compile is not a guarantee of runtime compatibility on every Amethyst/Sonar configuration. Test on the target iPhone 5s / iOS 12.5.8. If SpringBoard becomes unstable, remove `com.nova.glass.weather` from Sileo or SSH and respring.
