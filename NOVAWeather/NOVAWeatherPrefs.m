#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>
#import <CoreFoundation/CoreFoundation.h>

static NSString * const kSuite = @"com.nova.glass.weather";
static CFStringRef const kChanged = CFSTR("com.nova.glass/preferences-changed");

@interface NOVAWeatherPrefsController : PSListController @end
@implementation NOVAWeatherPrefsController
- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"NOVA Glass";
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p registerDefaults:@{
        @"com.nova.glass.enabled":@YES,
        @"com.nova.glass.sun.enabled":@YES,
        @"com.nova.glass.snow.enabled":@YES,
        @"com.nova.glass.rain.enabled":@NO,
        @"com.nova.glass.leaves.enabled":@NO
    }];
}
- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items = [NSMutableArray array];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        PSSpecifier *(^sw)(NSString *,NSString *,NSNumber *) = ^PSSpecifier *(NSString *title, NSString *key, NSNumber *value) {
            PSSpecifier *s = [PSSpecifier preferenceSpecifierNamed:title target:self
                set:@selector(setPreferenceValue:specifier:) get:@selector(readPreferenceValue:)
                detail:nil cell:PSSwitchCell edit:nil];
            [s setProperty:key forKey:@"key"]; [s setProperty:value forKey:@"default"];
            return s;
        };
        [items addObject:sw(@"Enable NOVA effects",@"com.nova.glass.enabled",@YES)];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"WEATHER & NATURE"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:sw(@"Daylight glow (07:00–13:59)",@"com.nova.glass.sun.enabled",@YES)];
        [items addObject:sw(@"Night snowfall",@"com.nova.glass.snow.enabled",@YES)];
        [items addObject:sw(@"Rainfall",@"com.nova.glass.rain.enabled",@NO)];
        [items addObject:sw(@"Falling autumn leaves",@"com.nova.glass.leaves.enabled",@NO)];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"Motion response uses the accelerometer"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"MESSAGES"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"Modern blue and white glass styling"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        _specifiers = [items copy];
    }
    return _specifiers;
}
- (id)readPreferenceValue:(PSSpecifier *)s {
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id v = [p objectForKey:[s propertyForKey:@"key"]];
    return v ?: [s propertyForKey:@"default"] ?: @NO;
}
- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)s {
    NSString *key = [s propertyForKey:@"key"];
    if (!key.length) return;
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p setBool:[value boolValue] forKey:key]; [p synchronize];
    CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),kChanged,NULL,NULL,true);
}
@end
