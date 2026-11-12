#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>
#import <objc/message.h>
#import <math.h>

static NSString * const kSuite = @"com.nova.glass.messages";
static char kEffectKey, kTintKey, kHighlightKey, kAtmosphereKey, kAtmosphereMaskKey;

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
    for (UIView *v = view; v; v = v.superview) {
        for (NSString *key in @[@"isFromMe", @"isOutgoing", @"isFromCurrentUser"]) {
            SEL selector = NSSelectorFromString(key);
            if ([v respondsToSelector:selector]) {
                @try { return ((BOOL (*)(id, SEL))objc_msgSend)(v, selector); }
                @catch (__unused NSException *exception) {}
            }
        }
        if (NOVAHas(NSStringFromClass(v.class), @[@"Outgoing", @"FromMe", @"FromSelf"])) return YES;
    }
    return NO;
}

static UIImage *NOVAImage(NSString *kind) {
    static UIImage *snowImage, *rainImage, *leafImage;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        UIGraphicsBeginImageContextWithOptions(CGSizeMake(24, 24), NO, 0);
        UIBezierPath *snow = [UIBezierPath bezierPath];
        snow.lineWidth = 1.35; snow.lineCapStyle = kCGLineCapRound;
        [[UIColor colorWithWhite:1 alpha:.96] setStroke];
        CGPoint c = CGPointMake(12, 12);
        for (NSInteger i = 0; i < 6; i++) {
            CGFloat a = (CGFloat)i * (CGFloat)M_PI / 3.0;
            CGPoint p = CGPointMake(c.x + cos(a) * 9.5, c.y + sin(a) * 9.5);
            [snow moveToPoint:c]; [snow addLineToPoint:p];
            CGFloat a1 = a + (CGFloat)M_PI * .78, a2 = a - (CGFloat)M_PI * .78;
            [snow moveToPoint:p];
            [snow addLineToPoint:CGPointMake(p.x - cos(a1)*3.2, p.y - sin(a1)*3.2)];
            [snow moveToPoint:p];
            [snow addLineToPoint:CGPointMake(p.x - cos(a2)*3.2, p.y - sin(a2)*3.2)];
        }
        [snow stroke];
        snowImage = UIGraphicsGetImageFromCurrentImageContext();
        UIGraphicsEndImageContext();

        UIGraphicsBeginImageContextWithOptions(CGSizeMake(5, 22), NO, 0);
        [[UIColor colorWithRed:.72 green:.88 blue:1 alpha:.86] setFill];
        [[UIBezierPath bezierPathWithRoundedRect:CGRectMake(1.7, 1, 1.5, 19) cornerRadius:.75] fill];
        rainImage = UIGraphicsGetImageFromCurrentImageContext();
        UIGraphicsEndImageContext();

        UIGraphicsBeginImageContextWithOptions(CGSizeMake(28, 20), NO, 0);
        UIBezierPath *leaf = [UIBezierPath bezierPath];
        [leaf moveToPoint:CGPointMake(2,10)];
        [leaf addCurveToPoint:CGPointMake(25,3) controlPoint1:CGPointMake(8,-1) controlPoint2:CGPointMake(22,-1)];
        [leaf addCurveToPoint:CGPointMake(7,18) controlPoint1:CGPointMake(27,15) controlPoint2:CGPointMake(14,22)];
        [leaf closePath];
        [[UIColor colorWithRed:1 green:.55 blue:.19 alpha:.95] setFill]; [leaf fill];
        UIBezierPath *vein = [UIBezierPath bezierPath]; vein.lineWidth = .8;
        [[UIColor colorWithRed:.56 green:.25 blue:.10 alpha:.8] setStroke];
        [vein moveToPoint:CGPointMake(4,11)]; [vein addLineToPoint:CGPointMake(23,5)]; [vein stroke];
        leafImage = UIGraphicsGetImageFromCurrentImageContext();
        UIGraphicsEndImageContext();
    });
    if ([kind isEqualToString:@"snow"]) return snowImage;
    if ([kind isEqualToString:@"rain"]) return rainImage;
    if ([kind isEqualToString:@"leaves"]) return leafImage;
    return nil;
}

static CAEmitterCell *NOVAEmitterCell(NSString *kind) {
    CAEmitterCell *cell = [CAEmitterCell emitterCell];
    UIImage *image = NOVAImage(kind);
    cell.contents = (__bridge id)image.CGImage;
    cell.contentsScale = UIScreen.mainScreen.scale;
    cell.birthRate = 1.0f; cell.lifetime = 8.0f;
    cell.velocity = 18.0f; cell.velocityRange = 8.0f;
    cell.emissionLongitude = (CGFloat)M_PI_2; cell.emissionRange = .25f;
    cell.scale = .45f; cell.scaleRange = .2f; cell.alphaSpeed = -.025f;
    return cell;
}
static CAEmitterLayer *NOVAEmitter(NSString *kind, CGRect bounds) {
    CAEmitterLayer *emitter = [CAEmitterLayer layer];
    emitter.name = [@"nova-emitter-" stringByAppendingString:kind];
    emitter.frame = bounds;
    emitter.emitterShape = kCAEmitterLayerLine;
    emitter.emitterMode = kCAEmitterLayerSurface;
    emitter.emitterPosition = CGPointMake(CGRectGetMidX(bounds), -8);
    emitter.emitterSize = CGSizeMake(CGRectGetWidth(bounds), 1);
    emitter.renderMode = kCAEmitterLayerOldestFirst;
    CAEmitterCell *cell = NOVAEmitterCell(kind);

    if ([kind isEqualToString:@"snow"]) {
        cell.birthRate = 1.15f; cell.lifetime = 9.0f;
        cell.velocity = 17.0f; cell.velocityRange = 11.0f;
        cell.yAcceleration = 7.0f; cell.xAcceleration = 1.5f;
        cell.scale = .42f; cell.scaleRange = .25f;
        cell.alphaSpeed = -.035f; cell.emissionRange = .40f;
    } else if ([kind isEqualToString:@"rain"]) {
        cell.birthRate = 8.0f; cell.lifetime = 2.8f;
        cell.velocity = 215.0f; cell.velocityRange = 55.0f;
        cell.yAcceleration = 35.0f; cell.xAcceleration = 18.0f;
        cell.emissionLongitude = (CGFloat)M_PI_2 - .13f; cell.emissionRange = .10f;
        cell.scale = .78f; cell.scaleRange = .20f; cell.alphaSpeed = -.11f;
    } else if ([kind isEqualToString:@"leaves"]) {
        cell.birthRate = .42f; cell.lifetime = 10.0f;
        cell.velocity = 22.0f; cell.velocityRange = 18.0f;
        cell.yAcceleration = 10.0f; cell.xAcceleration = 5.0f;
        cell.emissionRange = .46f; cell.scale = .62f; cell.scaleRange = .32f;
        cell.spin = 1.15f; cell.spinRange = 2.8f; cell.alphaSpeed = -.025f;
    }
    emitter.emitterCells = @[cell];
    return emitter;
}

static void NOVASunshine(CALayer *container, CGRect bounds) {
    CAGradientLayer *glow = [CAGradientLayer layer];
    glow.name = @"nova-sun-glow"; glow.type = kCAGradientLayerRadial; glow.frame = bounds;
    glow.startPoint = CGPointMake(.08,.05); glow.endPoint = CGPointMake(.92,.90);
    glow.colors = @[
        (id)[UIColor colorWithRed:1 green:.97 blue:.79 alpha:.34].CGColor,
        (id)[UIColor colorWithRed:1 green:.84 blue:.53 alpha:.13].CGColor,
        (id)[UIColor colorWithWhite:1 alpha:0].CGColor
    ];
    glow.locations = @[@0.0,@.38,@1.0]; glow.opacity = .92f;
    [container addSublayer:glow];

    CAGradientLayer *beam = [CAGradientLayer layer];
    beam.name = @"nova-sun-beam"; beam.frame = bounds;
    beam.colors = @[
        (id)[UIColor colorWithWhite:1 alpha:0].CGColor,
        (id)[UIColor colorWithRed:1 green:.94 blue:.78 alpha:.16].CGColor,
        (id)[UIColor colorWithWhite:1 alpha:0].CGColor
    ];
    beam.locations = @[@0.0,@.5,@1.0];
    beam.startPoint = CGPointMake(.5,0); beam.endPoint = CGPointMake(.5,1); beam.opacity = .8f;
    [container addSublayer:beam];

    CABasicAnimation *sway = [CABasicAnimation animationWithKeyPath:@"transform.rotation.z"];
    sway.fromValue = @(-.16); sway.toValue = @(.16); sway.duration = 15.0;
    sway.autoreverses = YES; sway.repeatCount = HUGE_VALF;
    [beam addAnimation:sway forKey:@"nova-sunlight-sway"];

    CABasicAnimation *pulse = [CABasicAnimation animationWithKeyPath:@"opacity"];
    pulse.fromValue = @.62; pulse.toValue = @.98; pulse.duration = 6.5;
    pulse.autoreverses = YES; pulse.repeatCount = HUGE_VALF;
    [glow addAnimation:pulse forKey:@"nova-sunlight-pulse"];
}

static void NOVARefreshAtmosphere(UIView *host) {
    if (!host || CGRectIsEmpty(host.bounds)) return;
    BOOL enabled = NOVASetting(@"messages.enabled", YES) && NOVASetting(@"messages.list", YES);
    BOOL snow = enabled && NOVASetting(@"messages.snow", YES);
    BOOL rain = enabled && NOVASetting(@"messages.rain", NO);
    BOOL sunshine = enabled && NOVASetting(@"messages.sunshine", NO);
    BOOL leaves = enabled && NOVASetting(@"messages.leaves", NO);
    NSInteger mask = (snow ? 1 : 0) | (rain ? 2 : 0) | (sunshine ? 4 : 0) | (leaves ? 8 : 0);

    UIView *overlay = objc_getAssociatedObject(host, &kAtmosphereKey);
    NSNumber *oldMask = objc_getAssociatedObject(host, &kAtmosphereMaskKey);
    if (mask == 0) {
        [overlay removeFromSuperview];
        objc_setAssociatedObject(host, &kAtmosphereKey, nil, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
        objc_setAssociatedObject(host, &kAtmosphereMaskKey, nil, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
        return;
    }

    if (!overlay || oldMask.integerValue != mask) {
        [overlay removeFromSuperview];
        overlay = [[UIView alloc] initWithFrame:host.bounds];
        overlay.backgroundColor = UIColor.clearColor;
        overlay.userInteractionEnabled = NO;
        overlay.accessibilityElementsHidden = YES;
        overlay.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        overlay.clipsToBounds = YES;
        if (sunshine) NOVASunshine(overlay.layer, overlay.bounds);
        if (snow) [overlay.layer addSublayer:NOVAEmitter(@"snow", overlay.bounds)];
        if (rain) [overlay.layer addSublayer:NOVAEmitter(@"rain", overlay.bounds)];
        if (leaves) [overlay.layer addSublayer:NOVAEmitter(@"leaves", overlay.bounds)];
        [host insertSubview:overlay atIndex:0];
        objc_setAssociatedObject(host, &kAtmosphereKey, overlay, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
        objc_setAssociatedObject(host, &kAtmosphereMaskKey, @(mask), OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    }

    overlay.frame = host.bounds;
    for (CALayer *layer in overlay.layer.sublayers) {
        layer.frame = overlay.bounds;
        if ([layer isKindOfClass:CAEmitterLayer.class]) {
            CAEmitterLayer *emitter = (CAEmitterLayer *)layer;
            emitter.emitterPosition = CGPointMake(CGRectGetMidX(overlay.bounds), -8);
            emitter.emitterSize = CGSizeMake(CGRectGetWidth(overlay.bounds), 1);
        }
    }
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
        CAGradientLayer *gradient = [CAGradientLayer layer];
        gradient.name = @"nova-glass-gradient";
        gradient.colors = @[
            (id)[UIColor colorWithWhite:1 alpha:.34].CGColor,
            (id)[UIColor colorWithRed:.67 green:.84 blue:1 alpha:.10].CGColor
        ];
        gradient.startPoint = CGPointMake(.1,0); gradient.endPoint = CGPointMake(.9,1);
        [wash.layer addSublayer:gradient];
        [view insertSubview:wash atIndex:1];
        objc_setAssociatedObject(view, &kTintKey, wash, OBJC_ASSOCIATION_RETAIN_NONATOMIC);

        shine = [[UIView alloc] initWithFrame:CGRectMake(10,1,MAX(0,view.bounds.size.width-20),1)];
        shine.backgroundColor = [UIColor colorWithWhite:1 alpha:.78];
        shine.userInteractionEnabled = NO; shine.autoresizingMask = UIViewAutoresizingFlexibleWidth;
        [wash addSubview:shine];
        objc_setAssociatedObject(view, &kHighlightKey, shine, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    }
    blur.frame = view.bounds; wash.frame = view.bounds;
    blur.layer.cornerRadius = radius; wash.layer.cornerRadius = radius;
    for (CALayer *layer in wash.layer.sublayers)
        if ([layer.name isEqualToString:@"nova-glass-gradient"]) layer.frame = wash.bounds;
    shine.frame = CGRectMake(10,1,MAX(0,view.bounds.size.width-20),1);
    wash.backgroundColor = tint; view.backgroundColor = UIColor.clearColor;
    view.layer.cornerRadius = radius; view.layer.borderWidth = border;
    view.layer.borderColor = [UIColor colorWithWhite:1 alpha:.60].CGColor;
    view.layer.shadowColor = [UIColor colorWithRed:.20 green:.48 blue:.78 alpha:.18].CGColor;
    view.layer.shadowOpacity = .22; view.layer.shadowRadius = 12;
    view.layer.shadowOffset = CGSizeMake(0,5);
}

static void NOVAStyle(UIView *view) {
    if (!view || !NOVAMessages()) return;
    NSString *name = NSStringFromClass(view.class);
    BOOL scrollHost = [view isKindOfClass:UIScrollView.class] &&
        NOVAHas(name, @[@"CKConversationList", @"CKTranscript", @"CKMessageTranscript"]);
    if (scrollHost) NOVARefreshAtmosphere(view);
    if (!NOVASetting(@"messages.enabled", YES)) return;

    if (NOVASetting(@"messages.bubbles", YES) &&
        NOVAHas(name, @[@"CKBalloonView", @"BalloonView", @"CKMessageBalloonView"])) {
        BOOL outgoing = NOVAOutgoing(view);
        UIColor *tint = outgoing
            ? [UIColor colorWithRed:.25 green:.59 blue:1 alpha:.25]
            : [UIColor colorWithRed:.91 green:.97 blue:1 alpha:.35];
        if (!NOVASetting(@"messages.iceBlue", YES))
            tint = outgoing ? [UIColor colorWithRed:.18 green:.48 blue:.96 alpha:.20]
                            : [UIColor colorWithWhite:1 alpha:.28];
        NOVAGlass(view, UIBlurEffectStyleLight, 19, tint, outgoing ? .58 : .9);
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
        if ([view isKindOfClass:UITableViewCell.class]) content = ((UITableViewCell *)view).contentView;
        else if ([view isKindOfClass:UICollectionViewCell.class]) content = ((UICollectionViewCell *)view).contentView;
        NOVAGlass(content, UIBlurEffectStyleLight, 14,
                  [UIColor colorWithRed:.94 green:.98 blue:1 alpha:.22], .56);
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
