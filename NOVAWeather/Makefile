ARCHS = arm64
TARGET = iphone:clang:12.4:12.0
INSTALL_TARGET_PROCESSES = SpringBoard

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = NOVAWeather
NOVAWeather_FILES = Tweak.xm
NOVAWeather_CFLAGS = -fobjc-arc
NOVAWeather_FRAMEWORKS = UIKit QuartzCore
NOVAWeather_LDFLAGS += -Wl,-segalign,4000

include $(THEOS_MAKE_PATH)/tweak.mk
