#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>

static NSString * const kNOVAPrefsSuite = @"com.nova.glass.weather";
static NSString * const kNOVAEnabledKey = @"com.nova.glass.enabled";
static NSString * const kNOVASunEnabledKey = @"com.nova.glass.sun.enabled";
static NSString * const kNOVASnowEnabledKey = @"com.nova.glass.snow.enabled";

@interface NOVAWeatherPrefsController : PSListController
@end

@implementation NOVAWeatherPrefsController
- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items = [NSMutableArray array];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];

        PSSpecifier *master = [PSSpecifier preferenceSpecifierNamed:@"Enable NOVA effects"
            target:self set:@selector(setPreferenceValue:specifier:)
            get:@selector(readPreferenceValue:)
            detail:nil cell:PSSwitchCell edit:nil];
        [master setProperty:kNOVAEnabledKey forKey:@"key"];
        [master setProperty:@YES forKey:@"default"];
        [items addObject:master];

        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"WEATHER"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];

        PSSpecifier *sun = [PSSpecifier preferenceSpecifierNamed:@"Daylight glow (07:00–13:59)"
            target:self set:@selector(setPreferenceValue:specifier:)
            get:@selector(readPreferenceValue:)
            detail:nil cell:PSSwitchCell edit:nil];
        [sun setProperty:kNOVASunEnabledKey forKey:@"key"];
        [sun setProperty:@YES forKey:@"default"];
        [items addObject:sun];

        PSSpecifier *snow = [PSSpecifier preferenceSpecifierNamed:@"Night snowfall (14:00–06:59)"
            target:self set:@selector(setPreferenceValue:specifier:)
            get:@selector(readPreferenceValue:)
            detail:nil cell:PSSwitchCell edit:nil];
        [snow setProperty:kNOVASnowEnabledKey forKey:@"key"];
        [snow setProperty:@YES forKey:@"default"];
        [items addObject:snow];

        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"Changes apply immediately"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        _specifiers = [items copy];
    }
    return _specifiers;
}
- (id)readPreferenceValue:(PSSpecifier *)specifier {
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    id value = [prefs objectForKey:[specifier propertyForKey:@"key"]];
    return value ?: [specifier propertyForKey:@"default"];
}
- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)specifier {
    NSUserDefaults *prefs = [[NSUserDefaults alloc] initWithSuiteName:kNOVAPrefsSuite];
    [prefs setObject:value forKey:[specifier propertyForKey:@"key"]];
    [prefs synchronize];
    CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),
        CFSTR("com.nova.glass/preferences-changed"), NULL, NULL, true);
}
@end
