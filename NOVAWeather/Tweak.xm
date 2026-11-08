#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <Foundation/Foundation.h>
#import <objc/runtime.h>
#import <math.h>

@interface NOVAWeatherOverlayView : UIView
@property (nonatomic, strong) CAGradientLayer *sunlightLayer;
@property (nonatomic, strong) CAEmitterLayer *snowLayer;
@property (nonatomic, strong) NSTimer *weatherTimer;
- (void)updateWeather;
- (void)handleApplicationActive:(NSNotification *)notification;
- (UIImage *)snowflakeImage;
@end

@implementation NOVAWeatherOverlayView

- (instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (!self) return nil;

    self.backgroundColor = UIColor.clearColor;
    self.userInteractionEnabled = NO;
    self.clipsToBounds = YES;
    self.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    self.accessibilityElementsHidden = YES;

    CAGradientLayer *sun = [CAGradientLayer layer];
    sun.type = kCAGradientLayerRadial;
    sun.colors = @[
        (__bridge id)[UIColor colorWithRed:1.0 green:0.91 blue:0.57 alpha:0.78].CGColor,
        (__bridge id)[UIColor colorWithRed:1.0 green:0.76 blue:0.35 alpha:0.28].CGColor,
        (__bridge id)[UIColor colorWithRed:1.0 green:0.82 blue:0.48 alpha:0.0].CGColor
    ];
    sun.locations = @[@0.0, @0.32, @1.0];
    sun.startPoint = CGPointMake(0.50, 0.04);
    sun.endPoint = CGPointMake(0.50, 0.95);
    sun.opacity = 0.0;
    [self.layer addSublayer:sun];
    self.sunlightLayer = sun;

    CAEmitterCell *flake = [CAEmitterCell emitterCell];
    flake.contents = (__bridge id)[self snowflakeImage].CGImage;
    flake.birthRate = 4.2;
    flake.lifetime = 10.0;
    flake.lifetimeRange = 3.0;
    flake.velocity = 38.0;
    flake.velocityRange = 22.0;
    flake.yAcceleration = 8.0;
    flake.xAcceleration = 1.5;
    flake.emissionLongitude = (CGFloat)M_PI_2;
    flake.emissionRange = 0.48;
    flake.scale = 0.12;
    flake.scaleRange = 0.075;
    flake.alphaSpeed = -0.025;
    flake.spinRange = 1.7;

    CAEmitterLayer *snow = [CAEmitterLayer layer];
    snow.emitterShape = kCAEmitterLayerLine;
    snow.emitterMode = kCAEmitterLayerSurface;
    snow.emitterPosition = CGPointMake(CGRectGetMidX(frame), 0.0);
    snow.emitterSize = CGSizeMake(frame.size.width, 1.0);
    snow.emitterCells = @[flake];
    snow.birthRate = 0.0;
    [self.layer addSublayer:snow];
    self.snowLayer = snow;

    [self updateWeather];
    __weak typeof(self) weakSelf = self;
    self.weatherTimer = [NSTimer scheduledTimerWithTimeInterval:60.0
                                                     repeats:YES
                                                       block:^(NSTimer *timer) {
        [weakSelf updateWeather];
    }];
    [[NSRunLoop mainRunLoop] addTimer:self.weatherTimer forMode:NSRunLoopCommonModes];
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(handleApplicationActive:)
                                                 name:UIApplicationDidBecomeActiveNotification
                                               object:nil];
    return self;
}

- (UIImage *)snowflakeImage {
    CGSize size = CGSizeMake(32.0, 32.0);
    UIGraphicsBeginImageContextWithOptions(size, NO, 2.0);
    CGContextRef context = UIGraphicsGetCurrentContext();
    CGContextSetStrokeColorWithColor(context, [UIColor colorWithWhite:1.0 alpha:0.92].CGColor);
    CGContextSetLineWidth(context, 1.7);
    CGContextSetLineCap(context, kCGLineCapRound);
    CGPoint center = CGPointMake(16.0, 16.0);
    for (NSInteger arm = 0; arm < 6; arm++) {
        CGFloat angle = (CGFloat)arm * (CGFloat)M_PI / 3.0;
        CGFloat dx = cos(angle), dy = sin(angle);
        CGPoint end = CGPointMake(center.x + dx * 12.0, center.y + dy * 12.0);
        CGContextMoveToPoint(context, center.x, center.y);
        CGContextAddLineToPoint(context, end.x, end.y);
        for (NSInteger branch = 0; branch < 2; branch++) {
            CGFloat distance = 7.0 + (CGFloat)branch * 2.7;
            CGPoint junction = CGPointMake(center.x + dx * distance, center.y + dy * distance);
            CGFloat branchAngleA = angle + (CGFloat)M_PI * 0.78;
            CGFloat branchAngleB = angle - (CGFloat)M_PI * 0.78;
            CGContextMoveToPoint(context, junction.x, junction.y);
            CGContextAddLineToPoint(context, junction.x + cos(branchAngleA) * 4.0,
                                   junction.y + sin(branchAngleA) * 4.0);
            CGContextMoveToPoint(context, junction.x, junction.y);
            CGContextAddLineToPoint(context, junction.x + cos(branchAngleB) * 4.0,
                                   junction.y + sin(branchAngleB) * 4.0);
        }
    }
    CGContextStrokePath(context);
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return image;
}

- (void)layoutSubviews {
    [super layoutSubviews];
    self.sunlightLayer.frame = CGRectMake(0.0, -CGRectGetHeight(self.bounds) * 0.22,
                                         CGRectGetWidth(self.bounds),
                                         CGRectGetHeight(self.bounds) * 0.78);
    self.snowLayer.frame = self.bounds;
    self.snowLayer.emitterPosition = CGPointMake(CGRectGetMidX(self.bounds), 0.0);
    self.snowLayer.emitterSize = CGSizeMake(CGRectGetWidth(self.bounds), 1.0);
}

- (void)handleApplicationActive:(NSNotification *)notification {
    [self updateWeather];
}

- (void)updateWeather {
    NSDateComponents *components = [[NSCalendar currentCalendar]
        components:NSCalendarUnitHour | NSCalendarUnitMinute fromDate:[NSDate date]];
    NSInteger hour = components.hour;
    BOOL sunlight = hour >= 7 && hour < 14;
    BOOL nighttimeSnow = hour >= 19 || hour < 7;

    [CATransaction begin];
    [CATransaction setDisableActions:YES];
    self.sunlightLayer.opacity = sunlight ? 0.88 : 0.0;
    self.snowLayer.birthRate = nighttimeSnow ? 1.0 : 0.0;
    [CATransaction commit];
}

- (void)dealloc {
    [self.weatherTimer invalidate];
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}

@end

@interface SBFStaticWallpaperView : UIView
@end

static char kNOVAWeatherOverlayKey;

static void NOVAAttachWeatherOverlay(UIView *wallpaperView) {
    if (!wallpaperView || objc_getAssociatedObject(wallpaperView, &kNOVAWeatherOverlayKey)) return;
    NOVAWeatherOverlayView *overlay = [[NOVAWeatherOverlayView alloc] initWithFrame:wallpaperView.bounds];
    overlay.translatesAutoresizingMaskIntoConstraints = NO;
    [wallpaperView addSubview:overlay];
    [NSLayoutConstraint activateConstraints:@[
        [overlay.leadingAnchor constraintEqualToAnchor:wallpaperView.leadingAnchor],
        [overlay.trailingAnchor constraintEqualToAnchor:wallpaperView.trailingAnchor],
        [overlay.topAnchor constraintEqualToAnchor:wallpaperView.topAnchor],
        [overlay.bottomAnchor constraintEqualToAnchor:wallpaperView.bottomAnchor]
    ]];
    objc_setAssociatedObject(wallpaperView, &kNOVAWeatherOverlayKey, overlay, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
}

%hook SBFStaticWallpaperView

- (void)_setupContentView {
    %orig;
    NOVAAttachWeatherOverlay(self);
}

- (void)_setupContentViewWithOptions:(NSUInteger)options {
    %orig;
    NOVAAttachWeatherOverlay(self);
}

%end
