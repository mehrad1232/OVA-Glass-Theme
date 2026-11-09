ARCHS = arm64
TARGET = iphone:clang:latest:12.0
INSTALL_TARGET_PROCESSES = SpringBoard

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = NOVAWeather
NOVAWeather_FILES = Tweak.xm
NOVAWeather_CFLAGS = -fobjc-arc -Wno-deprecated-declarations
NOVAWeather_FRAMEWORKS = UIKit QuartzCore
NOVAWeather_PLIST = NOVAWeather.plist
NOVAWeather_LDFLAGS += -Wl,-segalign,4000

BUNDLE_NAME = NOVAWeatherPrefs
NOVAWeatherPrefs_FILES = NOVAWeatherPrefs.m
NOVAWeatherPrefs_INSTALL_PATH = /Library/PreferenceBundles
NOVAWeatherPrefs_FRAMEWORKS = UIKit
NOVAWeatherPrefs_LDFLAGS += -undefined dynamic_lookup
NOVAWeatherPrefs_CFLAGS = -fobjc-arc

include $(THEOS_MAKE_PATH)/tweak.mk
include $(THEOS_MAKE_PATH)/bundle.mk
