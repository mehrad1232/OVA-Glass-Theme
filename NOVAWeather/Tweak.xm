#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>

@interface SBIconController : UIViewController @end
@interface SBIconImageView : UIImageView @end
@interface CSCoverSheetViewController : UIViewController @end

static NSString * const kNOVAEnabledKey = @"com.nova.glass.enabled";
static NSString * const kNOVASunEnabledKey = @"com.nova.glass.sun.enabled";
static NSString * const kNOVASnowEnabledKey = @"com.nova.glass.snow.enabled";
static NSString * const kNOVAPrefsSuite = @"com.nova.glass.weather";
static CFStringRef const kNOVAPrefsChanged = CFSTR("com.nova.glass/preferences-changed");

static BOOL NOVASettingEnabled(NSString *key) {
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    id value = [prefs objectForKey:key];
    return value ? [value boolValue] : YES;
}
static BOOL NOVAEnabled(void) { return NOVASettingEnabled(kNOVAEnabledKey); }
static BOOL NOVASunEnabled(void) { return NOVASettingEnabled(kNOVASunEnabledKey); }
static BOOL NOVASnowEnabled(void) { return NOVASettingEnabled(kNOVASnowEnabledKey); }

@interface NOVAGlassOverlay : UIView
@property(nonatomic,strong) CAGradientLayer *sunLayer;
@property(nonatomic,strong) CAEmitterLayer *snowLayer;
@property(nonatomic,strong) NSTimer *clockTimer;
- (void)updateForClock;
@end

static void NOVAOverlayPreferencesChanged(CFNotificationCenterRef center, void *observer,
                                          CFStringRef name, const void *object,
                                          CFDictionaryRef userInfo) {
    NOVAGlassOverlay *overlay = (__bridge NOVAGlassOverlay *)observer;
    dispatch_async(dispatch_get_main_queue(), ^{ [overlay updateForClock]; });
}

@implementation NOVAGlassOverlay
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.backgroundColor = UIColor.clearColor;
        self.userInteractionEnabled = NO;
        self.clipsToBounds = YES;
        self.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;

        _sunLayer = [CAGradientLayer layer];
        _sunLayer.startPoint = CGPointMake(.15, .1);
        _sunLayer.endPoint = CGPointMake(.85, .9);
        _sunLayer.colors = @[(id)[UIColor colorWithRed:1 green:.91 blue:.60 alpha:.30].CGColor,
                             (id)[UIColor colorWithWhite:1 alpha:.08].CGColor,
                             (id)UIColor.clearColor.CGColor];
        _sunLayer.locations = @[@0,@.42,@1];
        [self.layer addSublayer:_sunLayer];

        _snowLayer = [CAEmitterLayer layer];
        _snowLayer.emitterShape = kCAEmitterLayerLine;
        _snowLayer.emitterMode = kCAEmitterLayerSurface;
        CAEmitterCell *flake = [CAEmitterCell emitterCell];
        flake.contents = (id)[self snowflakeImage].CGImage;
        flake.birthRate = 8;
        flake.lifetime = 13;
        flake.velocity = 38;
        flake.velocityRange = 24;
        flake.xAcceleration = 4;
        flake.yAcceleration = 7;
        flake.scale = .22;
        flake.scaleRange = .15;
        flake.alphaSpeed = -.022;
        flake.spinRange = 1.0;
        _snowLayer.emitterCells = @[flake];
        [self.layer addSublayer:_snowLayer];

        CFNotificationCenterAddObserver(CFNotificationCenterGetDarwinNotifyCenter(),
            (__bridge const void *)self, NOVAOverlayPreferencesChanged,
            kNOVAPrefsChanged, NULL, CFNotificationSuspensionBehaviorDeliverImmediately);

        [self updateForClock];
        _clockTimer = [NSTimer scheduledTimerWithTimeInterval:60
            target:self selector:@selector(updateForClock) userInfo:nil repeats:YES];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(updateForClock)
            name:NSSystemTimeZoneDidChangeNotification object:nil];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(updateForClock)
            name:NSSystemClockDidChangeNotification object:nil];
    }
    return self;
}
- (UIImage *)snowflakeImage {
    UIGraphicsBeginImageContextWithOptions(CGSizeMake(18,18), NO, 0);
    CGContextRef c = UIGraphicsGetCurrentContext();
    CGContextSetStrokeColorWithColor(c, [UIColor colorWithWhite:1 alpha:.92].CGColor);
    CGContextSetLineWidth(c, 1.6);
    CGContextMoveToPoint(c,9,1); CGContextAddLineToPoint(c,9,17);
    CGContextMoveToPoint(c,1,9); CGContextAddLineToPoint(c,17,9);
    CGContextMoveToPoint(c,3,3); CGContextAddLineToPoint(c,15,15);
    CGContextMoveToPoint(c,15,3); CGContextAddLineToPoint(c,3,15);
    CGContextStrokePath(c);
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}
- (void)updateForClock {
    BOOL enabled = NOVAEnabled();
    NSInteger hour = [[NSCalendar currentCalendar] component:NSCalendarUnitHour fromDate:[NSDate date]];
    BOOL daylight = (hour >= 7 && hour < 14);
    [CATransaction begin];
    [CATransaction setAnimationDuration:1.0];
    self.sunLayer.opacity = (enabled && daylight && NOVASunEnabled()) ? 1.0 : 0.0;
    self.snowLayer.birthRate = (enabled && !daylight && NOVASnowEnabled()) ? 1.0 : 0.0;
    [CATransaction commit];
}
- (void)layoutSubviews {
    [super layoutSubviews];
    self.sunLayer.frame = self.bounds;
    self.snowLayer.frame = self.bounds;
    self.snowLayer.emitterPosition = CGPointMake(CGRectGetMidX(self.bounds), -8);
    self.snowLayer.emitterSize = CGSizeMake(self.bounds.size.width * 1.2, 1);
}
- (void)dealloc {
    [self.clockTimer invalidate];
    CFNotificationCenterRemoveObserver(CFNotificationCenterGetDarwinNotifyCenter(),
        (__bridge const void *)self, kNOVAPrefsChanged, NULL);
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}
@end

@interface NOVAGlassPanel : UIView
@end
@implementation NOVAGlassPanel
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.userInteractionEnabled = NO;
        self.backgroundColor = [UIColor colorWithWhite:1 alpha:.035];
        self.layer.borderColor = [UIColor colorWithWhite:1 alpha:.16].CGColor;
        self.layer.borderWidth = 1.0;
        self.layer.cornerRadius = 18;
        self.layer.masksToBounds = YES;
    }
    return self;
}
@end

static void NOVAInstallOverlayBehindContent(UIView *host, NSInteger tag, BOOL weather) {
    if (!host) return;
    UIView *existing = [host viewWithTag:tag];
    if (existing) {
        existing.frame = host.bounds;
        return;
    }
    UIView *overlay = weather ? (UIView *)[[NOVAGlassOverlay alloc] initWithFrame:host.bounds]
                              : (UIView *)[[NOVAGlassPanel alloc] initWithFrame:host.bounds];
    overlay.tag = tag;
    overlay.userInteractionEnabled = NO;
    overlay.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [host insertSubview:overlay atIndex:0];
}

%group NOVAIconGlass
%hook SBIconImageView
- (void)layoutSubviews {
    %orig;
    CALayer *glass = nil;
    for (CALayer *candidate in self.layer.sublayers) {
        if ([candidate.name isEqualToString:@"com.nova.glass.icon-sheen"]) { glass = candidate; break; }
    }
    if (!glass) {
        CAGradientLayer *sheen = [CAGradientLayer layer];
        sheen.name = @"com.nova.glass.icon-sheen";
        sheen.colors = @[(id)[UIColor colorWithWhite:1 alpha:.17].CGColor,
                         (id)[UIColor colorWithWhite:1 alpha:.015].CGColor,
                         (id)[UIColor colorWithWhite:1 alpha:.035].CGColor];
        sheen.locations = @[@0,@.42,@1];
        sheen.startPoint = CGPointMake(.1,0);
        sheen.endPoint = CGPointMake(.9,1);
        sheen.borderColor = [UIColor colorWithWhite:1 alpha:.30].CGColor;
        sheen.borderWidth = 1.0;
        [self.layer addSublayer:sheen];
        glass = sheen;
    }
    glass.frame = self.bounds;
    glass.cornerRadius = self.layer.cornerRadius > 0 ? self.layer.cornerRadius : 18;
    glass.masksToBounds = YES;
}
%end
%end

%group NOVAHome
%hook SBIconController
- (void)viewDidAppear:(BOOL)animated {
    %orig;
    dispatch_async(dispatch_get_main_queue(), ^{
        NOVAInstallOverlayBehindContent([(UIViewController *)self view], 0x4E4F5641, YES);
    });
}
- (void)viewDidLayoutSubviews {
    %orig;
    NOVAInstallOverlayBehindContent([(UIViewController *)self view], 0x4E4F5641, YES);
}
%end
%end

%group NOVALockScreen
%hook CSCoverSheetViewController
- (void)viewDidAppear:(BOOL)animated {
    %orig;
    dispatch_async(dispatch_get_main_queue(), ^{
        NOVAInstallOverlayBehindContent([(UIViewController *)self view], 0x4E4F5642, NO);
    });
}
%end
%end

%ctor {
    @autoreleasepool {
        if (objc_getClass("SBIconController")) %init(NOVAHome);
        if (objc_getClass("CSCoverSheetViewController")) %init(NOVALockScreen);
        if (objc_getClass("SBIconImageView")) %init(NOVAIconGlass);
    }
}
