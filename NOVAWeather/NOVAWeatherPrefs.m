#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>

static NSString * const kSuite = @"com.nova.glass.messages";

@interface NOVAWeatherPrefsController : PSListController
@end

@implementation NOVAWeatherPrefsController
- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"NOVA Messages";
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p registerDefaults:@{
        @"messages.enabled":@YES, @"messages.bubbles":@YES,
        @"messages.composer":@YES, @"messages.list":@YES,
        @"messages.snow":@YES, @"messages.rain":@NO,
        @"messages.sunshine":@NO, @"messages.leaves":@NO,
        @"messages.iceBlue":@YES
    }];
}

- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items = [NSMutableArray array];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS • MESSAGES"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        PSSpecifier *(^sw)(NSString *, NSString *) = ^PSSpecifier *(NSString *title, NSString *key) {
            PSSpecifier *specifier = [PSSpecifier preferenceSpecifierNamed:title
                target:self set:@selector(setPreferenceValue:specifier:)
                get:@selector(readPreferenceValue:) detail:nil cell:PSSwitchCell edit:nil];
            [specifier setProperty:key forKey:@"key"];
            [specifier setProperty:@YES forKey:@"default"];
            return specifier;
        };
        [items addObject:sw(@"Enable NOVA Glass", @"messages.enabled")];
        [items addObject:sw(@"Glass message bubbles", @"messages.bubbles")];
        [items addObject:sw(@"Glass composer and input", @"messages.composer")];
        [items addObject:sw(@"Frosted conversation list", @"messages.list")];
        [items addObject:sw(@"Ice-blue glass tint", @"messages.iceBlue")];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"ATMOSPHERE • CHOOSE EFFECTS"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:sw(@"Falling snow", @"messages.snow")];
        [items addObject:sw(@"Rainfall", @"messages.rain")];
        [items addObject:sw(@"Sunlight and warm rays", @"messages.sunshine")];
        [items addObject:sw(@"Falling autumn leaves", @"messages.leaves")];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:
            @"Atmosphere is drawn behind message cells so text and buttons remain readable. Multiple effects can be enabled together."
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        _specifiers = [items copy];
    }
    return _specifiers;
}
- (id)readPreferenceValue:(PSSpecifier *)specifier {
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id value = [p objectForKey:[specifier propertyForKey:@"key"]];
    return value ?: [specifier propertyForKey:@"default"] ?: @NO;
}
- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)specifier {
    NSString *key = [specifier propertyForKey:@"key"];
    if (!key.length) return;
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p setBool:[value boolValue] forKey:key];
    [p synchronize];
}
@end
