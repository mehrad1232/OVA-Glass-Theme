TARGET = iphone:clang:latest:12.0
ARCHS = arm64
FINALPACKAGE = 1
DEBUG = 0

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = NOVAWeather
NOVAWeather_FILES = Tweak.xm
NOVAWeather_CFLAGS = -fobjc-arc -Wno-deprecated-declarations
NOVAWeather_FRAMEWORKS = UIKit QuartzCore
NOVAWeather_INSTALL_TARGET_PROCESSES = SpringBoard

include $(THEOS_MAKE_PATH)/tweak.mk
