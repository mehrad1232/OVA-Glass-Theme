#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>
#import <CoreFoundation/CoreFoundation.h>

static NSString * const kNOVAPrefsSuite = @"com.nova.glass.weather";
static NSString * const kNOVAEnabledKey = @"com.nova.glass.enabled";
static NSString * const kNOVASunEnabledKey = @"com.nova.glass.sun.enabled";
static NSString * const kNOVASnowEnabledKey = @"com.nova.glass.snow.enabled";
static CFStringRef const kNOVAPrefsChanged = CFSTR("com.nova.glass/preferences-changed");

@interface NOVAWeatherPrefsController : PSListController
@end

@implementation NOVAWeatherPrefsController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"NOVA Glass";
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    NSDictionary *defaults = @{
        kNOVAEnabledKey: @YES,
        kNOVASunEnabledKey: @YES,
        kNOVASnowEnabledKey: @YES
    };
    [prefs registerDefaults:defaults];
}

- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items = [NSMutableArray array];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];

        PSSpecifier *(^switchSpecifier)(NSString *, NSString *) = ^PSSpecifier *(NSString *title, NSString *key) {
            PSSpecifier *specifier = [PSSpecifier preferenceSpecifierNamed:title
                target:self set:@selector(setPreferenceValue:specifier:)
                get:@selector(readPreferenceValue:)
                detail:nil cell:PSSwitchCell edit:nil];
            [specifier setProperty:key forKey:@"key"];
            [specifier setProperty:@YES forKey:@"default"];
            [specifier setProperty:@YES forKey:@"enabled"];
            return specifier;
        };

        [items addObject:switchSpecifier(@"Enable NOVA effects", kNOVAEnabledKey)];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"WEATHER"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:switchSpecifier(@"Daylight glow (07:00–13:59)", kNOVASunEnabledKey)];
        [items addObject:switchSpecifier(@"Night snowfall (14:00–06:59)", kNOVASnowEnabledKey)];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"Changes apply immediately"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        _specifiers = [items copy];
    }
    return _specifiers;
}

- (id)readPreferenceValue:(PSSpecifier *)specifier {
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    NSString *key = [specifier propertyForKey:@"key"];
    id value = [prefs objectForKey:key];
    if (!value) value = [specifier propertyForKey:@"default"];
    return value ?: @YES;
}

- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)specifier {
    NSString *key = [specifier propertyForKey:@"key"];
    if (key.length == 0) return;
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    [prefs setBool:[value boolValue] forKey:key];
    BOOL saved = [prefs synchronize];
    if (!saved) NSLog(@"[NOVA Glass] Preference sync returned NO for %@", key);
    CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),
        kNOVAPrefsChanged, NULL, NULL, true);
    [self reloadSpecifier:specifier];
}

@end
