#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>

static NSString * const kNOVAEnabledKey = @"com.nova.glass.enabled";
static BOOL NOVAEnabled(void) {
    NSUserDefaults *prefs=[[NSUserDefaults alloc] initWithSuiteName:@"com.nova.glass.weather"];
    id value = [prefs objectForKey:kNOVAEnabledKey];
    return value ? [value boolValue] : YES;
}

@interface NOVAGlassOverlay : UIView
@property(nonatomic,strong) CAGradientLayer *sunLayer;
@property(nonatomic,strong) CAEmitterLayer *snowLayer;
@property(nonatomic,strong) NSTimer *clockTimer;
@property(nonatomic,assign) BOOL weatherEnabled;
@end

@implementation NOVAGlassOverlay
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.backgroundColor = UIColor.clearColor;
        self.userInteractionEnabled = NO;
        self.clipsToBounds = YES;
        self.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        _weatherEnabled = YES;
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
        flake.birthRate = 8; flake.lifetime = 13; flake.velocity = 38;
        flake.velocityRange = 24; flake.xAcceleration = 4; flake.yAcceleration = 7;
        flake.scale = .22; flake.scaleRange = .15; flake.alphaSpeed = -.022;
        flake.spinRange = 1.0;
        _snowLayer.emitterCells = @[flake];
        [self.layer addSublayer:_snowLayer];
        [self updateForClock];
        _clockTimer = [NSTimer scheduledTimerWithTimeInterval:60 target:self selector:@selector(updateForClock) userInfo:nil repeats:YES];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(updateForClock) name:NSSystemTimeZoneDidChangeNotification object:nil];
        [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(updateForClock) name:NSSystemClockDidChangeNotification object:nil];
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
    UIImage *image=UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}
- (void)updateForClock {
    if (!NOVAEnabled()) { self.sunLayer.opacity=0; self.snowLayer.birthRate=0; return; }
    NSInteger hour = [[NSCalendar currentCalendar] component:NSCalendarUnitHour fromDate:[NSDate date]];
    BOOL daylight = (hour >= 7 && hour < 14);
    [CATransaction begin]; [CATransaction setAnimationDuration:2.0];
    self.sunLayer.opacity = daylight ? 1.0 : 0.0;
    self.snowLayer.birthRate = daylight ? 0.0 : 1.0;
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
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}
@end

@interface NOVAGlassPanel : UIView
@end
@implementation NOVAGlassPanel
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self=[super initWithFrame:frame])) {
        self.userInteractionEnabled=NO;
        self.backgroundColor=[UIColor colorWithWhite:1 alpha:.045];
        self.layer.borderColor=[UIColor colorWithWhite:1 alpha:.20].CGColor;
        self.layer.borderWidth=1.0;
        self.layer.cornerRadius=18;
        self.layer.masksToBounds=YES;
        if ([UIBlurEffect class]) {
            UIVisualEffectView *blur=[[UIVisualEffectView alloc] initWithEffect:[UIBlurEffect effectWithStyle:UIBlurEffectStyleLight]];
            blur.alpha=.18; blur.frame=self.bounds;
            blur.autoresizingMask=UIViewAutoresizingFlexibleWidth|UIViewAutoresizingFlexibleHeight;
            [self addSubview:blur];
        }
    }
    return self;
}
@end

static void NOVAInstallOverlay(UIView *host, NSInteger tag, BOOL weather) {
    if (!host || !NOVAEnabled() || [host viewWithTag:tag]) return;
    UIView *overlay = weather ? (UIView *)[[NOVAGlassOverlay alloc] initWithFrame:host.bounds] : (UIView *)[[NOVAGlassPanel alloc] initWithFrame:host.bounds];
    overlay.tag=tag;
    overlay.autoresizingMask=UIViewAutoresizingFlexibleWidth|UIViewAutoresizingFlexibleHeight;
    [host addSubview:overlay];
}

%group NOVAIconGlass
%hook SBIconImageView
- (void)layoutSubviews {
    %orig;
    CALayer *glass=nil;
    for (CALayer *candidate in self.layer.sublayers) {
        if ([candidate.name isEqualToString:@"com.nova.glass.icon-sheen"]) { glass=candidate; break; }
    }
    if (!glass) {
        CAGradientLayer *sheen=[CAGradientLayer layer];
        sheen.name=@"com.nova.glass.icon-sheen";
        sheen.colors=@[(id)[UIColor colorWithWhite:1 alpha:.17].CGColor,
                       (id)[UIColor colorWithWhite:1 alpha:.015].CGColor,
                       (id)[UIColor colorWithWhite:1 alpha:.035].CGColor];
        sheen.locations=@[@0,@.42,@1];
        sheen.startPoint=CGPointMake(.1,0); sheen.endPoint=CGPointMake(.9,1);
        sheen.borderColor=[UIColor colorWithWhite:1 alpha:.30].CGColor;
        sheen.borderWidth=1.0;
        [self.layer addSublayer:sheen];
        glass=sheen;
    }
    glass.frame=self.bounds;
    glass.cornerRadius=self.layer.cornerRadius>0?self.layer.cornerRadius:18;
    glass.masksToBounds=YES;
}
%end
%end

%group NOVAHome
%hook SpringBoard
- (void)applicationDidFinishLaunching:(id)application {
    %orig;
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(3*NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        UIWindow *window=[UIApplication sharedApplication].keyWindow;
        if (!window) window=[UIApplication sharedApplication].windows.firstObject;
        NOVAInstallOverlay(window, 0x4E4F5641, YES);
    });
}
%end
%end

%group NOVALockScreen
%hook SBLockScreenViewController
- (void)viewDidAppear:(BOOL)animated {
    %orig;
    dispatch_async(dispatch_get_main_queue(), ^{
        NOVAInstallOverlay(self.view, 0x4E4F5642, NO);
    });
}
%end
%end

%group NOVAControlCenter
%hook CCUIControlCenterViewController
- (void)viewDidAppear:(BOOL)animated {
    %orig;
    dispatch_async(dispatch_get_main_queue(), ^{
        NOVAInstallOverlay(self.view, 0x4E4F5643, NO);
    });
}
%end
%end

%ctor {
    @autoreleasepool {
        if (objc_getClass("SpringBoard")) %init(NOVAHome);
        if (objc_getClass("CSCoverSheetViewController")) %init(NOVALockScreen);\n        else if (objc_getClass("SBLockScreenViewController")) %init(NOVALockScreen);\n        if (objc_getClass("SBIconImageView")) %init(NOVAIconGlass);
        if (objc_getClass("CCUIControlCenterViewController")) %init(NOVAControlCenter);
    }
}
