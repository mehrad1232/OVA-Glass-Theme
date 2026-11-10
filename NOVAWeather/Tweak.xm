#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <CoreMotion/CoreMotion.h>
#import <objc/runtime.h>

@interface SBIconController : UIViewController @end
@interface SBIconImageView : UIImageView @end
@interface CSCoverSheetViewController : UIViewController @end

static NSString * const kSuite = @"com.nova.glass.weather";
static NSString * const kEnabled = @"com.nova.glass.enabled";
static NSString * const kSun = @"com.nova.glass.sun.enabled";
static NSString * const kSnow = @"com.nova.glass.snow.enabled";
static NSString * const kRain = @"com.nova.glass.rain.enabled";
static NSString * const kLeaves = @"com.nova.glass.leaves.enabled";
static CFStringRef const kChanged = CFSTR("com.nova.glass/preferences-changed");
static BOOL NOVAGet(NSString *key) {
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id v = [p objectForKey:key];
    return v ? [v boolValue] : (![key isEqualToString:kRain] && ![key isEqualToString:kLeaves]);
}
static BOOL NOVAOn(void) { return NOVAGet(kEnabled); }

@interface NOVAGlassOverlay : UIView
@property(nonatomic,strong) CAGradientLayer *sun;
@property(nonatomic,strong) CAEmitterLayer *snow;
@property(nonatomic,strong) CAEmitterLayer *rain;
@property(nonatomic,strong) CAEmitterLayer *leaves;
@property(nonatomic,strong) CMMotionManager *motion;
@property(nonatomic,strong) NSTimer *clockTimer;
@property(nonatomic,assign) BOOL motionActive;
- (void)refresh;
@end

static void NOVAPrefsChanged(CFNotificationCenterRef c, void *observer, CFStringRef n,
                             const void *o, CFDictionaryRef info) {
    NOVAGlassOverlay *v = (__bridge NOVAGlassOverlay *)observer;
    dispatch_async(dispatch_get_main_queue(), ^{ [v refresh]; });
}

@implementation NOVAGlassOverlay
- (UIImage *)particle:(NSInteger)kind {
    CGSize s = kind == 0 ? CGSizeMake(18,18) : (kind == 1 ? CGSizeMake(5,22) : CGSizeMake(22,14));
    UIGraphicsBeginImageContextWithOptions(s, NO, 0);
    CGContextRef c = UIGraphicsGetCurrentContext();
    if (kind == 0) {
        CGContextSetStrokeColorWithColor(c, [UIColor colorWithWhite:1 alpha:.95].CGColor);
        CGContextSetLineWidth(c, 1.5);
        CGContextMoveToPoint(c,9,1); CGContextAddLineToPoint(c,9,17);
        CGContextMoveToPoint(c,1,9); CGContextAddLineToPoint(c,17,9);
        CGContextMoveToPoint(c,3,3); CGContextAddLineToPoint(c,15,15);
        CGContextMoveToPoint(c,15,3); CGContextAddLineToPoint(c,3,15);
        CGContextStrokePath(c);
    } else if (kind == 1) {
        CGContextSetFillColorWithColor(c, [UIColor colorWithRed:.70 green:.88 blue:1 alpha:.8].CGColor);
        CGContextFillEllipseInRect(c, CGRectMake(1,0,3,20));
    } else {
        CGContextSetFillColorWithColor(c, [UIColor colorWithRed:.96 green:.57 blue:.22 alpha:.92].CGColor);
        CGContextMoveToPoint(c,1,7); CGContextAddQuadCurveToPoint(c,11,-2,21,5);
        CGContextAddQuadCurveToPoint(c,18,14,5,13); CGContextClosePath(c); CGContextFillPath(c);
        CGContextSetStrokeColorWithColor(c, [UIColor colorWithRed:.45 green:.23 blue:.08 alpha:.8].CGColor);
        CGContextSetLineWidth(c,1); CGContextMoveToPoint(c,4,10); CGContextAddLineToPoint(c,18,4); CGContextStrokePath(c);
    }
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}
- (CAEmitterLayer *)emitterWithImage:(UIImage *)image rate:(float)rate lifetime:(float)life
                            velocity:(float)velocity scale:(float)scale spin:(float)spin {
    CAEmitterLayer *layer = [CAEmitterLayer layer];
    layer.emitterShape = kCAEmitterLayerLine;
    layer.emitterMode = kCAEmitterLayerSurface;
    layer.renderMode = kCAEmitterLayerOldestFirst;
    CAEmitterCell *cell = [CAEmitterCell emitterCell];
    cell.contents = (id)image.CGImage;
    cell.birthRate = rate;
    cell.lifetime = life;
    cell.velocity = velocity;
    cell.velocityRange = velocity * .48;
    cell.xAcceleration = 5;
    cell.yAcceleration = 10;
    cell.scale = scale;
    cell.scaleRange = scale * .5;
    cell.alphaSpeed = -.012;
    cell.spinRange = spin;
    layer.emitterCells = @[cell];
    layer.birthRate = 0;
    return layer;
}
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.backgroundColor = UIColor.clearColor;
        self.userInteractionEnabled = NO;
        self.clipsToBounds = YES;
        self.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;

        _sun = [CAGradientLayer layer];
        _sun.startPoint = CGPointMake(.12,0); _sun.endPoint = CGPointMake(.88,1);
        _sun.colors = @[(id)[UIColor colorWithRed:1 green:.78 blue:.30 alpha:.48].CGColor,
                        (id)[UIColor colorWithRed:1 green:.91 blue:.68 alpha:.17].CGColor,
                        (id)UIColor.clearColor.CGColor];
        _sun.locations = @[@0,@.42,@1];
        [self.layer addSublayer:_sun];

        _snow = [self emitterWithImage:[self particle:0] rate:34 lifetime:17 velocity:42 scale:.34 spin:1.8];
        _rain = [self emitterWithImage:[self particle:1] rate:55 lifetime:5 velocity:235 scale:.7 spin:.05];
        _leaves = [self emitterWithImage:[self particle:2] rate:12 lifetime:13 velocity:34 scale:.65 spin:3.4];
        [self.layer addSublayer:_snow]; [self.layer addSublayer:_rain]; [self.layer addSublayer:_leaves];

        _motion = [[CMMotionManager alloc] init];
        _motion.accelerometerUpdateInterval = .10;
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(appActive)
            name:UIApplicationDidBecomeActiveNotification object:nil];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(appInactive)
            name:UIApplicationWillResignActiveNotification object:nil];
        self.clockTimer = [NSTimer scheduledTimerWithTimeInterval:60 target:self selector:@selector(refresh) userInfo:nil repeats:YES];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(refresh) name:NSSystemClockDidChangeNotification object:nil];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(refresh) name:NSSystemTimeZoneDidChangeNotification object:nil];
        CFNotificationCenterAddObserver(CFNotificationCenterGetDarwinNotifyCenter(),
            (__bridge const void *)self, NOVAPrefsChanged, kChanged, NULL,
            CFNotificationSuspensionBehaviorDeliverImmediately);
        [self refresh];
    }
    return self;
}
- (void)layoutSubviews {
    [super layoutSubviews];
    self.sun.frame = self.bounds;
    NSArray *layers = @[self.snow,self.rain,self.leaves];
    for (CAEmitterLayer *layer in layers) {
        layer.frame = self.bounds;
        layer.emitterPosition = CGPointMake(CGRectGetMidX(self.bounds), -2);
        layer.emitterSize = CGSizeMake(MAX(1,self.bounds.size.width * 1.18), 1);
    }
}
- (void)refresh {
    BOOL enabled = NOVAOn();
    NSInteger hour = [[NSCalendar currentCalendar] component:NSCalendarUnitHour fromDate:[NSDate date]];
    BOOL day = hour >= 7 && hour < 14;
    [CATransaction begin]; [CATransaction setAnimationDuration:1.4];
    self.sun.opacity = (enabled && day && NOVAGet(kSun)) ? 1 : 0;
    self.snow.birthRate = (enabled && !day && NOVAGet(kSnow)) ? 1 : 0;
    self.rain.birthRate = (enabled && NOVAGet(kRain)) ? 1 : 0;
    self.leaves.birthRate = (enabled && NOVAGet(kLeaves)) ? 1 : 0;
    [CATransaction commit];
    if (enabled && (NOVAGet(kSnow) || NOVAGet(kRain) || NOVAGet(kLeaves))) [self startMotion];
    else [self stopMotion];
}
- (void)startMotion {
    if (self.motionActive || !self.window || !self.motion.accelerometerAvailable) return;
    self.motionActive = YES;
    __weak typeof(self) weakSelf = self;
    [self.motion startAccelerometerUpdatesToQueue:[NSOperationQueue mainQueue]
        withHandler:^(CMAccelerometerData *data, NSError *error) {
            __strong typeof(weakSelf) self = weakSelf;
            if (!self || error || !self.motionActive) return;
            double x = data.acceleration.x, y = data.acceleration.y;
            CGFloat dx = (CGFloat)MAX(-65, MIN(65, x * 95));
            CGFloat dy = (CGFloat)MAX(-30, MIN(30, -y * 35));
            for (CAEmitterLayer *layer in @[self.snow,self.rain,self.leaves]) {
                for (CAEmitterCell *cell in layer.emitterCells) {
                    cell.xAcceleration = 5 + dx;
                    cell.yAcceleration = 10 + dy;
                }
                layer.emitterPosition = CGPointMake(CGRectGetMidX(self.bounds) + dx * .35, -2 + dy * .15);
            }
        }];
}
- (void)stopMotion {
    if (!self.motionActive) return;
    self.motionActive = NO;
    [self.motion stopAccelerometerUpdates];
}
- (void)appActive { [self refresh]; }
- (void)appInactive { [self stopMotion]; }
- (void)didMoveToWindow {
    [super didMoveToWindow];
    if (self.window) [self refresh]; else [self stopMotion];
}
- (void)dealloc {
    [self stopMotion];
    CFNotificationCenterRemoveObserver(CFNotificationCenterGetDarwinNotifyCenter(),
        (__bridge const void *)self, kChanged, NULL);
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}
@end

@interface NOVAGlassPanel : UIView @end
@implementation NOVAGlassPanel
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.userInteractionEnabled = NO;
        self.backgroundColor = [UIColor colorWithWhite:1 alpha:.035];
        self.layer.borderColor = [UIColor colorWithWhite:1 alpha:.16].CGColor;
        self.layer.borderWidth = 1; self.layer.cornerRadius = 18; self.layer.masksToBounds = YES;
    }
    return self;
}
@end

static void NOVAInstall(UIView *host, NSInteger tag, BOOL weather) {
    if (!host) return;
    UIView *old = [host viewWithTag:tag];
    if (old) { old.frame = host.bounds; return; }
    UIView *view = weather ? (UIView *)[[NOVAGlassOverlay alloc] initWithFrame:host.bounds]
                           : (UIView *)[[NOVAGlassPanel alloc] initWithFrame:host.bounds];
    view.tag = tag; view.userInteractionEnabled = NO;
    view.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [host insertSubview:view atIndex:0];
}

%group NOVAIconGlass
%hook SBIconImageView
- (void)layoutSubviews {
    %orig;
    CALayer *glass = nil;
    for (CALayer *candidate in self.layer.sublayers)
        if ([candidate.name isEqualToString:@"com.nova.glass.icon-sheen"]) { glass = candidate; break; }
    if (!glass) {
        CAGradientLayer *sheen = [CAGradientLayer layer];
        sheen.name = @"com.nova.glass.icon-sheen";
        sheen.colors = @[(id)[UIColor colorWithWhite:1 alpha:.20].CGColor,
                         (id)[UIColor colorWithWhite:1 alpha:.015].CGColor,
                         (id)[UIColor colorWithRed:.40 green:.70 blue:1 alpha:.08].CGColor];
        sheen.locations = @[@0,@.48,@1]; sheen.startPoint = CGPointMake(.1,0); sheen.endPoint = CGPointMake(.9,1);
        sheen.borderColor = [UIColor colorWithWhite:1 alpha:.28].CGColor; sheen.borderWidth = 1;
        [self.layer addSublayer:sheen]; glass = sheen;
    }
    glass.frame = self.bounds; glass.cornerRadius = self.layer.cornerRadius > 0 ? self.layer.cornerRadius : 18;
    glass.masksToBounds = YES;
}
%end
%end

%group NOVAHome
%hook SBIconController
- (void)viewDidAppear:(BOOL)animated { %orig; dispatch_async(dispatch_get_main_queue(), ^{ NOVAInstall(self.view, 0x4E4F5641, YES); }); }
- (void)viewDidLayoutSubviews { %orig; NOVAInstall(self.view, 0x4E4F5641, YES); }
%end
%end

%group NOVALockScreen
%hook CSCoverSheetViewController
- (void)viewDidAppear:(BOOL)animated { %orig; dispatch_async(dispatch_get_main_queue(), ^{ NOVAInstall(self.view, 0x4E4F5642, YES); }); }
- (void)viewDidLayoutSubviews { %orig; NOVAInstall(self.view, 0x4E4F5642, YES); }
%end
%end

static void NOVAStyleMessages(void) {
    if (![NSBundle.mainBundle.bundleIdentifier isEqualToString:@"com.apple.MobileSMS"]) return;
    UIColor *blue = [UIColor colorWithRed:.12 green:.48 blue:.96 alpha:1];
    UIColor *glass = [UIColor colorWithWhite:1 alpha:.76];
    UINavigationBar *nav = [UINavigationBar appearance];
    nav.translucent = YES; nav.barTintColor = glass; nav.tintColor = blue;
    nav.titleTextAttributes = @{NSForegroundColorAttributeName:[UIColor colorWithWhite:.10 alpha:1],
                                NSFontAttributeName:[UIFont systemFontOfSize:17 weight:UIFontWeightSemibold]};
    if ([nav respondsToSelector:@selector(setShadowImage:)]) nav.shadowImage = [UIImage new];
    UIToolbar *toolbar = [UIToolbar appearance];
    toolbar.translucent = YES; toolbar.barTintColor = glass; toolbar.tintColor = blue;
    UITableView *table = [UITableView appearance];
    table.backgroundColor = [UIColor colorWithWhite:.97 alpha:.96];
    UITableViewCell *cell = [UITableViewCell appearance];
    cell.tintColor = blue;
    UITextField *field = [UITextField appearance];
    field.tintColor = blue;
    UITextView *textView = [UITextView appearance];
    textView.tintColor = blue;
}

%ctor {
    @autoreleasepool {
        NSString *bundle = NSBundle.mainBundle.bundleIdentifier;
        if ([bundle isEqualToString:@"com.apple.MobileSMS"]) {
            dispatch_async(dispatch_get_main_queue(), ^{ NOVAStyleMessages(); });
        }
        if ([bundle isEqualToString:@"com.apple.springboard"]) {
            if (objc_getClass("SBIconController")) %init(NOVAHome);
            if (objc_getClass("CSCoverSheetViewController")) %init(NOVALockScreen);
            if (objc_getClass("SBIconImageView")) %init(NOVAIconGlass);
        }
    }
}
