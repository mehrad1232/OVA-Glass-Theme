ARCHS = arm64
TARGET = iphone:clang:latest:12.0
INSTALL_TARGET_PROCESSES = SpringBoard MobilePhone InCallService

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = NOVAExperience
NOVAExperience_FILES = Tweak.xm
NOVAExperience_CFLAGS = -fobjc-arc -Wno-deprecated-declarations
NOVAExperience_FRAMEWORKS = UIKit QuartzCore
NOVAExperience_PLIST = NOVAExperience.plist

include $(THEOS_MAKE_PATH)/tweak.mk
