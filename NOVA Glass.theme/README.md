# NOVA Glass Theme v4.0 — iOS 12 / SnowBoard

NOVA Glass v4.0 contains redesigned glossy glass-style icons and static wallpapers for the iPhone 5s. It is paired with the separate NOVAWeather rootful tweak for actual SpringBoard effects.

## Theme assets
- 70+ SnowBoard icon PNGs, 120×120, RGBA with transparent corners, named by app bundle identifier.
- 512×512 editable source masters for each generated icon.
- Six iPhone 5s wallpapers (day, golden, dusk, night, aurora, snow) at 640×1136.
- Six full-size 1170×2532 wallpaper masters.
- Wallpaper-Preview.html is only a browser preview. SnowBoard does not run it as a live wallpaper.

## Actual time-based effects
Install the separate NOVAWeather package from the combined v4 artifact:
- Sunlight from the top of the wallpaper: 07:00–13:59 local time.
- Animated snowfall: 19:00–06:59 local time.
- 14:00–18:59: no overlay.
This is implemented in a SpringBoard tweak, not the SnowBoard theme. It targets iOS 12 rootful arm64 and attaches to SBFStaticWallpaperView. Runtime must be tested on the actual iPhone 5s / Amethyst before calling it device-verified.

## Install
1. Extract the combined v4 ZIP on the PC.
2. Copy the NOVA Glass.theme folder to /Library/Themes/ on the jailbroken iPhone.
3. Install NOVAWeather.deb using Sileo or Zebra, then respring.
4. In SnowBoard, enable NOVA Glass and respring.
5. Set one of the included PNG wallpapers in Settings or Photos.

## Honest compatibility notes
- SnowBoard applies only icons whose bundle identifiers match. Third-party app IDs are best-effort and may vary by app version.
- The theme does not replace Settings internals, system fonts, Control Center, lock-screen layout, gestures, or ringtone.
- The tweak build is CI-validated, but no physical iPhone is attached to CI. If the effect does not appear or SpringBoard becomes unstable, uninstall NOVAWeather from Sileo/Zebra and respring.
