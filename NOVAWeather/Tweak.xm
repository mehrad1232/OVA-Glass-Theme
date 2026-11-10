#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>
#import <objc/message.h>

static NSString * const kSuite = @"com.nova.glass.messages";
static char kEffectKey, kTintKey, kHighlightKey, kSnowKey;

static BOOL NOVASetting(NSString *key, BOOL fallback) {
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id value = [p objectForKey:key];
    return value ? [value boolValue] : fallback;
}
static BOOL NOVAMessages(void) {
    return [NSBundle.mainBundle.bundleIdentifier isEqualToString:@"com.apple.MobileSMS"];
}
static BOOL NOVAHas(NSString *name, NSArray<NSString *> *tokens) {
    for (NSString *token in tokens)
        if ([name rangeOfString:token options:NSCaseInsensitiveSearch].location != NSNotFound) return YES;
    return NO;
}
static BOOL NOVAOutgoing(UIView *view) {
    for (UIView *v = view; v && view != nil; v = v.superview) {
        for (NSString *key in @[@"isFromMe", @"isOutgoing", @"isFromCurrentUser"]) {
            SEL s = NSSelectorFromString(key);
            if ([v respondsToSelector:s]) {
                @try { return ((BOOL (*)(id, SEL))objc_msgSend)(v, s); }
                @catch (__unused NSException *e) {}
            }
        }
        if (NOVAHas(NSStringFromClass(v.class), @[@"Outgoing", @"FromMe", @"FromSelf"])) return YES;
        if (v == view.superview && !v.superview) break;
    }
    return NO;
}
static UIImage *NOVASnowImage(void) {
    static UIImage *img; static dispatch_once_t once;
    dispatch_once(&once, ^{
        UIGraphicsBeginImageContextWithOptions(CGSizeMake(10,10), NO, 0);
        [[UIColor colorWithWhite:1 alpha:.95] setFill];
        [[UIBezierPath bezierPathWithOvalInRect:CGRectMake(1,1,8,8)] fill];
        img = UIGraphicsGetImageFromCurrentImageContext();
        UIGraphicsEndImageContext();
    });
    return img;
}
static void NOVAGlass(UIView *view, UIBlurEffectStyle style, CGFloat radius, UIColor *tint, CGFloat border) {
    if (!view || CGRectIsEmpty(view.bounds)) return;
    UIVisualEffectView *blur = objc_getAssociatedObject(view, &kEffectKey);
    UIView *wash = objc_getAssociatedObject(view, &kTintKey);
    UIView *shine = objc_getAssociatedObject(view, &kHighlightKey);
    if (!blur) {
        blur = [[UIVisualEffectView alloc] initWithEffect:[UIBlurEffect effectWithStyle:style]];
        blur.userInteractionEnabled = NO;
        blur.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        blur.clipsToBounds = YES;
        [view insertSubview:blur atIndex:0];
        objc_setAssociatedObject(view, &kEffectKey, blur, OBJC_ASSOCIATION_RETAIN_NONATOMIC);

        wash = [[UIView alloc] initWithFrame:view.bounds];
        wash.userInteractionEnabled = NO;
        wash.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        wash.clipsToBounds = YES;
        CAGradientLayer *g = [CAGradientLayer layer];
        g.name = @"nova-glass-gradient";
        g.colors = @[(id)[UIColor colorWithWhite:1 alpha:.34].CGColor,
                     (id)[UIColor colorWithRed:.67 green:.84 blue:1 alpha:.10].CGColor];
        g.startPoint = CGPointMake(.1,0); g.endPoint = CGPointMake(.9,1);
        [wash.layer addSublayer:g];
        [view insertSubview:wash atIndex:1];
        objc_setAssociatedObject(view, &kTintKey, wash, OBJC_ASSOCIATION_RETAIN_NONATOMIC);

        shine = [[UIView alloc] initWithFrame:CGRectMake(10,1,MAX(0,view.bounds.size.width-20),1)];
        shine.backgroundColor = [UIColor colorWithWhite:1 alpha:.78];
        shine.userInteractionEnabled = NO;
        shine.autoresizingMask = UIViewAutoresizingFlexibleWidth;
        [wash addSubview:shine];
        objc_setAssociatedObject(view, &kHighlightKey, shine, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    }
    blur.frame = view.bounds; wash.frame = view.bounds;
    blur.layer.cornerRadius = radius; wash.layer.cornerRadius = radius;
    for (CALayer *layer in wash.layer.sublayers)
        if ([layer.name isEqualToString:@"nova-glass-gradient"]) layer.frame = wash.bounds;
    shine.frame = CGRectMake(10,1,MAX(0,view.bounds.size.width-20),1);
    wash.backgroundColor = tint;
    view.backgroundColor = UIColor.clearColor;
    view.layer.cornerRadius = radius;
    view.layer.borderWidth = 0;
    view.layer.borderColor = nil;
    view.layer.shadowColor = [UIColor colorWithRed:.20 green:.48 blue:.78 alpha:.18].CGColor;
    view.layer.shadowOpacity = .22;
    view.layer.shadowRadius = 12;
    view.layer.shadowOffset = CGSizeMake(0, 5);
}
static void NOVASnow(UIView *host) {
    if (!host || objc_getAssociatedObject(host, &kSnowKey) || CGRectIsEmpty(host.bounds)) return;
    UIView *overlay = [[UIView alloc] initWithFrame:host.bounds];
    overlay.userInteractionEnabled = NO;
    overlay.backgroundColor = UIColor.clearColor;
    overlay.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    overlay.clipsToBounds = YES;
    CAEmitterLayer *emitter = [CAEmitterLayer layer];
    emitter.frame = overlay.bounds;
    emitter.emitterShape = kCAEmitterLayerLine;
    emitter.emitterMode = kCAEmitterLayerSurface;
    emitter.emitterPosition = CGPointMake(CGRectGetMidX(overlay.bounds), -2);
    emitter.emitterSize = CGSizeMake(CGRectGetWidth(overlay.bounds), 1);
    CAEmitterCell *flake = [CAEmitterCell emitterCell];
    flake.contents = (__bridge id)NOVASnowImage().CGImage;
    flake.birthRate = .18; flake.lifetime = 10;
    flake.velocity = 15; flake.velocityRange = 8; flake.yAcceleration = 5;
    flake.scale = .12; flake.scaleRange = .08; flake.alphaSpeed = -.055;
    emitter.emitterCells = @[flake];
    [overlay.layer addSublayer:emitter];
    [host insertSubview:overlay atIndex:0];
    objc_setAssociatedObject(host, &kSnowKey, overlay, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
}
static void NOVAStyle(UIView *view) {
    if (!view || !NOVAMessages()) return;
    NSString *name = NSStringFromClass(view.class);
    if (!NOVAHas(name, @[@"BalloonView", @"CKMessageEntryView", @"CKContentEntryView",
                        @"CKConversationListCell", @"CKConversationListStandardCell",
                        @"CKConversationListLargeTextCell", @"CKStarkConversationListCell",
                        @"CKTranscriptBalloonCell", @"CKConversationListTableView",
                        @"CKTranscriptCollectionView", @"UINavigationBar", @"UIToolbar"])) return;
    if (!NOVASetting(@"messages.enabled", NO)) return;
    BOOL ice = NOVASetting(@"messages.iceBlue", YES);
    if (NOVASetting(@"messages.bubbles", YES) && NOVAHas(name, @[@"BalloonView"])) {
        BOOL out = NOVAOutgoing(view);
        UIColor *tint = out
            ? [UIColor colorWithRed:.25 green:.59 blue:1 alpha:.25]
            : [UIColor colorWithRed:.91 green:.97 blue:1 alpha:.35];
        if (!ice) tint = out ? [UIColor colorWithRed:.18 green:.48 blue:.96 alpha:.20]
                             : [UIColor colorWithWhite:1 alpha:.28];
        NOVAGlass(view, UIBlurEffectStyleLight, 19, tint, out ? .58 : .9);
        return;
    }
    if (NOVASetting(@"messages.composer", YES) &&
        NOVAHas(name, @[@"CKMessageEntryView", @"CKContentEntryView"])) {
        NOVAGlass(view, UIBlurEffectStyleExtraLight, 21,
                  [UIColor colorWithRed:.92 green:.97 blue:1 alpha:.40], .92);
        return;
    }
    if (NOVASetting(@"messages.list", YES) &&
        NOVAHas(name, @[@"CKConversationListCell", @"CKConversationListStandardCell",
                        @"CKConversationListLargeTextCell", @"CKStarkConversationListCell",
                        @"CKTranscriptBalloonCell"])) {
        view.backgroundColor = UIColor.clearColor;
        UIView *content = view;
        if ([view isKindOfClass:UITableViewCell.class])
            content = ((UITableViewCell *)view).contentView;
        else if ([view isKindOfClass:UICollectionViewCell.class])
            content = ((UICollectionViewCell *)view).contentView;
        NOVAGlass(content, UIBlurEffectStyleLight, 14,
                  [UIColor colorWithRed:.94 green:.98 blue:1 alpha:.22], .56);
        return;
    }
    if (NOVASetting(@"messages.list", YES) && NOVAHas(name, @[@"CKConversationListTableView"])) {
        view.backgroundColor = [UIColor colorWithRed:.92 green:.96 blue:1 alpha:1];
        if (NOVASetting(@"messages.snow", YES)) NOVASnow(view);
        return;
    }
    if (NOVAHas(name, @[@"CKTranscriptCollectionView"])) {
        view.backgroundColor = [UIColor colorWithRed:.94 green:.97 blue:1 alpha:1];
        if (NOVASetting(@"messages.snow", YES)) NOVASnow(view);
        return;
    }
    if ([view isKindOfClass:UINavigationBar.class]) {
        UINavigationBar *bar = (UINavigationBar *)view;
        bar.translucent = YES;
        bar.barTintColor = [UIColor colorWithWhite:1 alpha:.52];
        bar.tintColor = [UIColor colorWithRed:.12 green:.48 blue:.96 alpha:1];
        bar.shadowImage = [UIImage new];
        return;
    }
    if ([view isKindOfClass:UIToolbar.class]) {
        UIToolbar *bar = (UIToolbar *)view;
        bar.translucent = YES;
        bar.barTintColor = [UIColor colorWithWhite:1 alpha:.48];
    }
}
%group NOVAMessagesOnly
%hook UIView
- (void)layoutSubviews {
    %orig;
    NOVAStyle(self);
}
%end
%end
%ctor {
    @autoreleasepool {
        if (NOVAMessages()) {
            dispatch_async(dispatch_get_main_queue(), ^{
                %init(NOVAMessagesOnly);
            });
        }
    }
}
