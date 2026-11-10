# NOVA Glass Messages 3.0 — research and architecture

## Research basis
- Theos Logos documentation: https://theos.dev/docs/logos
- Theos package documentation, including the MobileSubstrate bundle filter plist: https://theos.dev/docs/packaging
- Apple UIKit documentation for UIVisualEffectView and UIBlurEffect. Blur views must be composed correctly; fading the effect view or its superview can prevent correct rendering: https://developer.apple.com/documentation/uikit/uivisualeffectview and https://developer.apple.com/documentation/uikit/uiblureffect
- ChatKit is Apple's private SMS/iMessage UI framework. iOS 11 runtime-header indexes list CKBalloonView, CKMessageEntryView, CKConversationListCell and CKConversationListTableView. These are research references, not a guarantee that every class is identical on iOS 12.5.8: https://developer.limneos.net/?framework=ChatKit.framework&ios=11.1.2 and https://theapplewiki.com/wiki/Dev%3AChatKit.framework/Inheritance_hierarchy

## Runtime architecture
- Substrate injection is restricted to com.apple.MobileSMS.
- Logos hooks UIView layout as a compatibility fallback, then styles only runtime class names matching known ChatKit balloon, composer, conversation-list or transcript families.
- Glass uses a full-opacity UIVisualEffectView, a separate translucent tint/gradient layer and a fine border.
- Snow is a low-birth-rate CAEmitterLayer behind transcript/list content, touch-through and clipped to its host view.
- Preferences use the com.nova.glass.messages defaults suite and independent feature keys.

## Compatibility and validation
Target: arm64 rootful iOS 12.0+, with iPhone 5s / iOS 12.5.8 as the target device.
ChatKit is private and its view tree can vary. Runtime verification on the target iPhone remains necessary; CI verifies compilation, package metadata and injection scope, but cannot prove visual output on the phone.
