#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>
#import <objc/runtime.h>
#import <objc/message.h>

static NSString * const kSuite = @"com.nova.glass.messages";
static NSString * const kEnabled = @"messages.enabled";
static NSString * const kBubbles = @"messages.bubbles";
static NSString * const kComposer = @"messages.composer";
static NSString * const kList = @"messages.list";
static const void *kNOVAEffectKey = &kNOVAEffectKey;
static const void *kNOVABorderKey = &kNOVABorderKey;

static BOOL NOVASetting(NSString *key, BOOL fallback) {
    NSUserDefaults *defaults = [[NSUserDefaults alloc] initWithSuiteName:kSuite];
    id value = [defaults objectForKey:key];
    return value ? [value boolValue] : fallback;
}
static BOOL NOVAEnabled(void) { return NOVASetting(kEnabled, YES); }
static BOOL NOVAIsMessages(void) {
    return [NSBundle.mainBundle.bundleIdentifier isEqualToString:@"com.apple.MobileSMS"];
}
static BOOL NOVANameContains(NSString *name, NSArray<NSString *> *tokens) {
    for (NSString *token in tokens) if ([name rangeOfString:token options:NSCaseInsensitiveSearch].location != NSNotFound) return YES;
    return NO;
}
static BOOL NOVAIsOutgoing(UIView *view) {
    for (NSString *selectorName in @[@"isFromMe", @"isOutgoing", @"isFromCurrentUser"]) {
        SEL selector = NSSelectorFromString(selectorName);
        if ([view respondsToSelector:selector]) {
            @try { return ((BOOL (*)(id, SEL))objc_msgSend)(view, selector); }
            @catch (__unused NSException *exception) {}
        }
    }
    NSString *name = NSStringFromClass(view.class);
    return NOVANameContains(name, @[@"Outgoing", @"FromMe", @"FromSelf"]);
}
static void NOVAAddBlur(UIView *view, UIBlurEffectStyle style, CGFloat radius) {
    UIVisualEffectView *effect = objc_getAssociatedObject(view, kNOVAEffectKey);
    if (!effect) {
        effect = [[UIVisualEffectView alloc] initWithEffect:[UIBlurEffect effectWithStyle:style]];
        effect.userInteractionEnabled = NO;
        effect.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
        effect.layer.cornerRadius = radius;
        effect.clipsToBounds = YES;
        objc_setAssociatedObject(view, kNOVAEffectKey, effect, OBJC_ASSOCIATION_RETAIN_NONATOMIC);
        [view insertSubview:effect atIndex:0];
    }
    effect.frame = view.bounds;
    effect.layer.cornerRadius = radius;
}
static void NOVAStyleBubble(UIView *view) {
    BOOL outgoing = NOVAIsOutgoing(view);
    UIColor *tint = outgoing
        ? [UIColor colorWithRed:.20 green:.53 blue:.98 alpha:.32]
        : [UIColor colorWithWhite:1 alpha:.72];
    view.backgroundColor = tint;
    view.layer.cornerRadius = 19;
    view.layer.masksToBounds = YES;
    view.layer.borderWidth = 1;
    view.layer.borderColor = [UIColor colorWithWhite:1 alpha:outgoing ? .48 : .88].CGColor;
    NOVAAddBlur(view, UIBlurEffectStyleLight, 19);
}
static void NOVAStyleComposer(UIView *view) {
    view.backgroundColor = [UIColor colorWithWhite:1 alpha:.32];
    view.layer.cornerRadius = 18;
    view.layer.borderWidth = 1;
    view.layer.borderColor = [UIColor colorWithWhite:1 alpha:.72].CGColor;
    view.layer.masksToBounds = YES;
    NOVAAddBlur(view, UIBlurEffectStyleExtraLight, 18);
}
static void NOVAStyleListCell(UIView *view) {
    view.backgroundColor = [UIColor colorWithWhite:1 alpha:.18];
    view.layer.cornerRadius = 13;
    view.layer.masksToBounds = YES;
}
static void NOVAStyleMessagesView(UIView *view) {
    if (!NOVAEnabled() || !NOVAIsMessages()) return;
    NSString *name = NSStringFromClass(view.class);
    if (NOVASetting(kBubbles, YES) &&
        NOVANameContains(name, @[@"CKBalloonView", @"CKMessageBalloon", @"CKTranscriptBalloon"])) {
        NOVAStyleBubble(view);
        return;
    }
    if (NOVASetting(kComposer, YES) &&
        NOVANameContains(name, @[@"CKMessageEntryView", @"CKMessageEntryContainer", @"CKInputView"])) {
        NOVAStyleComposer(view);
        return;
    }
    if (NOVASetting(kList, YES) &&
        NOVANameContains(name, @[@"CKConversationListCell", @"CKConversationListCollectionViewCell"])) {
        NOVAStyleListCell(view);
        return;
    }
    if (NOVASetting(kList, YES) &&
        NOVANameContains(name, @[@"CKConversationListView", @"CKConversationListTableView"])) {
        view.backgroundColor = [UIColor colorWithWhite:.95 alpha:.96];
    }
}

%group NOVAMessagesOnly
%hook UIView
- (void)layoutSubviews {
    %orig;
    NOVAStyleMessagesView(self);
}
%end
%end

%ctor {
    @autoreleasepool {
        if (NOVAIsMessages()) {
            dispatch_async(dispatch_get_main_queue(), ^{
                %init(NOVAMessagesOnly);
                UINavigationBar *bar = [UINavigationBar appearance];
                bar.translucent = YES;
                bar.barTintColor = [UIColor colorWithWhite:1 alpha:.66];
                bar.tintColor = [UIColor colorWithRed:.12 green:.48 blue:.96 alpha:1];
                bar.titleTextAttributes = @{
                    NSForegroundColorAttributeName:[UIColor colorWithWhite:.08 alpha:1],
                    NSFontAttributeName:[UIFont systemFontOfSize:17 weight:UIFontWeightSemibold]
                };
                bar.shadowImage = [UIImage new];
                UIToolbar *toolbar = [UIToolbar appearance];
                toolbar.translucent = YES;
                toolbar.barTintColor = [UIColor colorWithWhite:1 alpha:.62];
                toolbar.tintColor = bar.tintColor;
                UITextField *field = [UITextField appearance];
                field.tintColor = bar.tintColor;
                UITextView *textView = [UITextView appearance];
                textView.tintColor = bar.tintColor;
                UITableView *table = [UITableView appearance];
                table.backgroundColor = [UIColor colorWithWhite:.96 alpha:1];
                UITableViewCell *cell = [UITableViewCell appearance];
                cell.backgroundColor = UIColor.clearColor;
                cell.tintColor = bar.tintColor;
            });
        }
    }
}
