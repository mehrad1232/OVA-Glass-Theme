#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>

static NSString * const kSuite = @"com.nova.glass.experience";
static char kNOVAEffectKey;

static BOOL NOVAEnabled(void) {
    id value = [[[NSUserDefaults alloc] initWithSuiteName:kSuite] objectForKey:@"enabled"];
    return value ? [value boolValue] : YES;
}
static BOOL NOVAProcessAllowed(void) {
    NSString *bundle = NSBundle.mainBundle.bundleIdentifier ?: @"";
    return [bundle isEqualToString:@"com.apple.springboard"] ||
           [bundle isEqualToString:@"com.apple.mobilephone"] ||
           [bundle isEqualToString:@"com.apple.InCallService"];
}
static BOOL NOVANameHas(NSString *name, NSArray<NSString *> *parts) {
    for (NSString *part in parts)
        if ([name rangeOfString:part options:NSCaseInsensitiveSearch].location != NSNotFound) return YES;
    return NO;
}
static void NOVAApplyGlass(UIView *view, CGFloat radius, UIColor *washColor) {
    if (!view || CGRectIsEmpty(view.bounds) || objc_getAssociatedObject(view, &kNOVAEffectKey)) return;
    UIVisualEffectView *blur = [[UIVisualEffectView alloc] initWithEffect:
        [UIBlurEffect effectWithStyle:UIBlurEffectStyleLight]];
    blur.frame = view.bounds;
    blur.userInteractionEnabled = NO;
    blur.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    blur.clipsToBounds = YES;
    blur.layer.cornerRadius = radius;
    [view insertSubview:blur atIndex:0];

    UIView *wash = [[UIView alloc] initWithFrame:view.bounds];
    wash.backgroundColor = washColor;
    wash.userInteractionEnabled = NO;
    wash.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    wash.layer.cornerRadius = radius;
    wash.layer.borderWidth = 0.65;
    wash.layer.borderColor = [UIColor colorWithWhite:1 alpha:.48].CGColor;
    wash.layer.shadowColor = [UIColor colorWithRed:.20 green:.48 blue:.78 alpha:.25].CGColor;
    wash.layer.shadowOpacity = .18;
    wash.layer.shadowRadius = 10;
    wash.layer.shadowOffset = CGSizeMake(0,4);
    [view insertSubview:wash aboveSubview:blur];
    objc_setAssociatedObject(view, &kNOVAEffectKey, blur, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    view.backgroundColor = UIColor.clearColor;
    view.layer.cornerRadius = radius;
    view.clipsToBounds = YES;
}
static void NOVAStyleView(UIView *view) {
    if (!NOVAEnabled() || !NOVAProcessAllowed() || !view) return;
    NSString *name = NSStringFromClass(view.class);

    // iOS 12 Lock Screen / Today view surfaces. Match known container names only.
    if (NOVANameHas(name, @[@"SBLockScreenNotificationListView",
                            @"SBLockScreenActionButtonsView",
                            @"SBLockScreenDateView",
                            @"SBDashBoardNotificationListView",
                            @"SBDashBoardActionButton",
                            @"SBLockScreenSlideUpAppGrabberView"])) {
        NOVAApplyGlass(view, 18, [UIColor colorWithRed:.88 green:.95 blue:1 alpha:.24]);
        return;
    }

    // Control Center cards and controls.
    if (NOVANameHas(name, @[@"CCUIContentModuleContainerView",
                            @"CCUIControlCenterSectionView",
                            @"CCUIRoundButton",
                            @"CCUIControlCenterSlider"])) {
        NOVAApplyGlass(view, 17, [UIColor colorWithRed:.88 green:.96 blue:1 alpha:.26]);
        return;
    }

    // Incoming and active call UI. Class names differ across iOS 12 point releases;
    // this optional styling is intentionally limited to known Phone UI class families.
    if (NOVANameHas(name, @[@"PHIncomingCallView",
                            @"PHInCallRootView",
                            @"PHInCallBottomBar",
                            @"PHBottomBar",
                            @"PHCallParticipantsView",
                            @"PHHandsetDialerView"])) {
        NOVAApplyGlass(view, 22, [UIColor colorWithRed:.78 green:.90 blue:1 alpha:.30]);
        return;
    }
}
%group NOVASystemGlass
%hook UIView
- (void)layoutSubviews {
    %orig;
    NOVAStyleView(self);
}
%end
%end

%ctor {
    @autoreleasepool {
        if (NOVAProcessAllowed()) {
            dispatch_async(dispatch_get_main_queue(), ^{
                %init(NOVASystemGlass);
            });
        }
    }
}
