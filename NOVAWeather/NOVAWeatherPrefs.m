#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>

@interface NOVAWeatherPrefsController : PSListController
@end

@implementation NOVAWeatherPrefsController
- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items=[NSMutableArray array];
        PSSpecifier *group=[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil];
        [items addObject:group];
        PSSpecifier *enabled=[PSSpecifier preferenceSpecifierNamed:@"Enable weather effects"
            target:self set:@selector(setPreferenceValue:specifier:)
            get:@selector(readPreferenceValue:)
            detail:nil cell:PSSwitchCell edit:nil];
        [enabled setProperty:@"com.nova.glass.enabled" forKey:@"key"];
        [enabled setProperty:@YES forKey:@"default"];
        [items addObject:enabled];
        PSSpecifier *info=[PSSpecifier preferenceSpecifierNamed:@"Sunlight: 07:00–13:59"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil];
        [items addObject:info];
        PSSpecifier *snow=[PSSpecifier preferenceSpecifierNamed:@"Snowfall: 14:00–06:59"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil];
        [items addObject:snow];
        _specifiers=[items copy];
    }
    return _specifiers;
}
- (id)readPreferenceValue:(PSSpecifier *)specifier {
    id value=[[NSUserDefaults standardUserDefaults] objectForKey:[specifier propertyForKey:@"key"]];
    return value ?: [specifier propertyForKey:@"default"];
}
- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)specifier {
    [[NSUserDefaults standardUserDefaults] setObject:value forKey:[specifier propertyForKey:@"key"]];
    [[NSUserDefaults standardUserDefaults] synchronize];
    CFNotificationCenterPostNotification(CFNotificationCenterGetDarwinNotifyCenter(),
        CFSTR("com.nova.glass/preferences-changed"), NULL, NULL, true);
}
@end
