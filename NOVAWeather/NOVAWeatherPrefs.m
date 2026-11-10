#import <UIKit/UIKit.h>
#import <Preferences/PSListController.h>
#import <Preferences/PSSpecifier.h>

static NSString * const kSuite = @"com.nova.glass.messages";
@interface NOVAWeatherPrefsController : PSListController @end
@implementation NOVAWeatherPrefsController
- (void)viewDidLoad {
    [super viewDidLoad];
    self.title = @"NOVA Messages";
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p registerDefaults:@{
        @"messages.enabled":@YES, @"messages.bubbles":@YES,
        @"messages.composer":@YES, @"messages.list":@YES,
        @"messages.snow":@YES, @"messages.iceBlue":@YES
    }];
}
- (NSArray *)specifiers {
    if (!_specifiers) {
        NSMutableArray *items = [NSMutableArray array];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA GLASS • MESSAGES"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        PSSpecifier *(^sw)(NSString *,NSString *) = ^PSSpecifier *(NSString *title, NSString *key) {
            PSSpecifier *s = [PSSpecifier preferenceSpecifierNamed:title target:self
                set:@selector(setPreferenceValue:specifier:) get:@selector(readPreferenceValue:)
                detail:nil cell:PSSwitchCell edit:nil];
            [s setProperty:key forKey:@"key"];
            [s setProperty:@YES forKey:@"default"];
            return s;
        };
        [items addObject:sw(@"Enable NOVA Glass", @"messages.enabled")];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"MESSAGE SURFACES"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:sw(@"Glass message bubbles", @"messages.bubbles")];
        [items addObject:sw(@"Glass composer and input", @"messages.composer")];
        [items addObject:sw(@"Frosted conversation list", @"messages.list")];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA ATMOSPHERE"
            target:nil set:nil get:nil detail:nil cell:PSGroupCell edit:nil]];
        [items addObject:sw(@"Ice-blue glass tint", @"messages.iceBlue")];
        [items addObject:sw(@"Soft falling snow", @"messages.snow")];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"Designed for iPhone 5s • iOS 12"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        [items addObject:[PSSpecifier preferenceSpecifierNamed:@"NOVA • WHITE / ICE BLUE • LIQUID GLASS"
            target:nil set:nil get:nil detail:nil cell:PSStaticTextCell edit:nil]];
        _specifiers = [items copy];
    }
    return _specifiers;
}
- (id)readPreferenceValue:(PSSpecifier *)s {
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id value = [p objectForKey:[s propertyForKey:@"key"]];
    return value ?: [s propertyForKey:@"default"] ?: @NO;
}
- (void)setPreferenceValue:(id)value specifier:(PSSpecifier *)s {
    NSString *key = [s propertyForKey:@"key"];
    if (!key.length) return;
    NSUserDefaults *p = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    [p setBool:[value boolValue] forKey:key];
    [p synchronize];
}
@end
