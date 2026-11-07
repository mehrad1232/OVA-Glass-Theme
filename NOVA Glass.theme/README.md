# NOVA Glass Theme v3.0 — iOS 12 / SnowBoard

A genuine glass-style icon theme for jailbroken iOS 12 devices, designed and tested as a build artifact for iPhone 5s (640×1136).

## What's actually included
- 70+ SnowBoard-ready PNG icons in `NOVA Glass.theme/IconBundles`, each 120×120 and named by app bundle identifier.
- 512×512 editable high-resolution icon masters in `NOVA Glass.theme/Artwork-Source/Icons`.
- Six iPhone 5s wallpapers (day, golden, dusk, night, aurora, snow) at 640×1136.
- Six 1170×2532 full-resolution wallpaper masters in `Artwork-Source/Wallpapers`.
- SnowBoard theme metadata and a separate HTML visual preview.

The high-resolution masters are real source artwork, not random padding. The SnowBoard-ready icon files are the 120×120 PNGs in IconBundles.

## Build and artifact
GitHub Actions runs `tools/build_theme.py`, validates the PNGs and plist, creates `NOVA-Glass-Theme-iOS12-v3.0.zip`, and checks that the ZIP is at least 50,000,000 bytes. The archive uses stored (uncompressed) PNG files, so its size is based on actual image assets.

## Install
1. Download the `NOVA-Glass-Theme-iOS12-v3.0` artifact from the successful Actions run.
2. Extract the `NOVA Glass.theme` folder.
3. Copy it to `/Library/Themes/` on the jailbroken iPhone.
4. Enable NOVA Glass in SnowBoard and respring.
5. Choose one of the six PNG wallpapers in Photos or Settings.

## Compatibility limits — read before expecting system-wide changes
- SnowBoard can apply icons when the installed app's bundle identifier matches a filename in IconBundles. Third-party bundle identifiers can differ by app version; unmatched apps keep their original icons.
- This is an icon-and-wallpaper SnowBoard theme. It does **not** independently replace the Settings app's internal screens, system font, Control Center, lock-screen layout, gestures, or ringtone. Those require separate iOS 12.5.8-compatible SnowBoard extensions or jailbreak tweaks. Do not install random iOS 17-only packages on iOS 12.
- The HTML preview is not an iOS live wallpaper. The included PNG wallpapers are normal static images.

## Build source
All art is generated locally by `tools/build_theme.py` with Pillow. No proprietary icon pack or copyrighted font is bundled.
