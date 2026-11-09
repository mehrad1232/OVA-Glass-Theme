#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>

@interface NOVAGlassOverlay : UIView
@property(nonatomic,strong) CAGradientLayer *sunLayer;
@property(nonatomic,strong) CAEmitterLayer *snowLayer;
@property(nonatomic,strong) NSTimer *clockTimer;
@end

@implementation NOVAGlassOverlay
- (instancetype)initWithFrame:(CGRect)frame {
    if ((self = [super initWithFrame:frame])) {
        self.backgroundColor = UIColor.clearColor;
        self.userInteractionEnabled = NO;
        self.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        _sunLayer = [CAGradientLayer layer];
        _sunLayer.frame = CGRectMake(-frame.size.width*.25, -frame.size.height*.2, frame.size.width*1.5, frame.size.height*.75);
        _sunLayer.startPoint = CGPointMake(.5, .5); _sunLayer.endPoint = CGPointMake(1, 1);
        _sunLayer.colors = @[(id)[UIColor colorWithRed:1 green:.91 blue:.58 alpha:.28].CGColor,(id)[UIColor colorWithWhite:1 alpha:.10].CGColor,(id)UIColor.clearColor.CGColor];
        _sunLayer.locations = @[@0,@.35,@1];
        [self.layer addSublayer:_sunLayer];
        _snowLayer = [CAEmitterLayer layer];
        _snowLayer.emitterPosition = CGPointMake(frame.size.width/2, -12);
        _snowLayer.emitterSize = CGSizeMake(frame.size.width*1.3, 1);
        _snowLayer.emitterShape = kCAEmitterLayerLine;
        CAEmitterCell *flake = [CAEmitterCell emitterCell];
        flake.contents = (id)[self snowflakeImage].CGImage;
        flake.birthRate = 7; flake.lifetime = 12; flake.velocity = 42; flake.velocityRange = 22;
        flake.xAcceleration = 5; flake.yAcceleration = 8; flake.scale = .22; flake.scaleRange = .16;
        flake.alphaSpeed = -.025; flake.spinRange = 1.2;
        _snowLayer.emitterCells = @[flake];
        [self.layer addSublayer:_snowLayer];
        [self updateForClock];
        _clockTimer = [NSTimer scheduledTimerWithTimeInterval:60 target:self selector:@selector(updateForClock) userInfo:nil repeats:YES];
    }
    return self;
}
- (UIImage *)snowflakeImage {
    UIGraphicsBeginImageContextWithOptions(CGSizeMake(20,20), NO, 0);
    CGContextRef c = UIGraphicsGetCurrentContext(); CGContextSetStrokeColorWithColor(c, [UIColor colorWithWhite:1 alpha:.9].CGColor); CGContextSetLineWidth(c, 2);
    CGContextMoveToPoint(c,10,1); CGContextAddLineToPoint(c,10,19); CGContextMoveToPoint(c,1,10); CGContextAddLineToPoint(c,19,10);
    CGContextMoveToPoint(c,3,3); CGContextAddLineToPoint(c,17,17); CGContextMoveToPoint(c,17,3); CGContextAddLineToPoint(c,3,17); CGContextStrokePath(c);
    UIImage *image=UIGraphicsGetImageFromCurrentImageContext(); UIGraphicsEndImageContext(); return image;
}
- (void)updateForClock {
    NSInteger hour = NSCalendar.currentCalendar.component(NSCalendarUnitHour, fromDate:NSDate.date);
    BOOL daylight = (hour >= 7 && hour < 14);
    [CATransaction begin]; [CATransaction setAnimationDuration:2.0];
    self.sunLayer.opacity = daylight ? 1.0 : 0.0;
    self.snowLayer.birthRate = daylight ? 0.0 : 1.0;
    [CATransaction commit];
}
- (void)layoutSubviews {
    [super layoutSubviews];
    self.sunLayer.frame = CGRectMake(-self.bounds.size.width*.25, -self.bounds.size.height*.2, self.bounds.size.width*1.5, self.bounds.size.height*.75);
    self.snowLayer.frame = self.bounds; self.snowLayer.emitterPosition = CGPointMake(self.bounds.size.width/2, -12); self.snowLayer.emitterSize = CGSizeMake(self.bounds.size.width*1.3,1);
}
- (void)dealloc { [self.clockTimer invalidate]; }
@end

%hook SpringBoard
- (void)applicationDidFinishLaunching:(id)application {
    %orig;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(4*NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            UIWindow *host = [UIApplication sharedApplication].keyWindow;
            if (!host) host = [UIApplication sharedApplication].windows.firstObject;
            if (!host) return;
            NOVAGlassOverlay *overlay = [[NOVAGlassOverlay alloc] initWithFrame:host.bounds];
            overlay.tag = 0x4E4F5641;
            [host addSubview:overlay];
        });
    });
}
%end
