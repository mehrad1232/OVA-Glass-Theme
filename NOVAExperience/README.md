# NOVA Glass System Experience 1.0.0

Optional rootful arm64 tweak for iOS 12.0–12.5.8. It adds restrained UIKit blur styling to known Lock Screen notification/action surfaces, Control Center modules and Phone incoming/active call surfaces. The same package installs the original NOVA Glass ringtone at `/Library/Ringtones/NOVA Glass.m4r`.

## Important compatibility notes
- iOS private class names vary between point releases and jailbreak environments. Unknown views are left untouched.
- The incoming-call styling is best-effort; it does not replace Apple's call controls or change call behavior.
- The lock-screen clock widget is a separate optional Xen HTML widget in `XenHTML/NOVA-LockScreen`.
- This package is optional and separate from NOVA Glass for Messages. Test on the target device before enabling both.
- Disable system styling by setting `enabled` to false in the `com.nova.glass.experience` preferences domain, or uninstall this package.
