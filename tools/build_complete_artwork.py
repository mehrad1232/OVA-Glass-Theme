#!/usr/bin/env python3
"""Generate NOVA Glass icon artwork with recognizable vector pictograms (no monogram placeholders)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, random, plistlib

ROOT=Path(__file__).resolve().parents[1]
THEME=ROOT/"NOVA Glass.theme"
ICON_DIR=THEME/"IconBundles"
SETTINGS=THEME/"Bundles"/"com.apple.preferences-framework"
MASTER=THEME/"Artwork-Source"/"Icons"
for p in (ICON_DIR, SETTINGS, MASTER): p.mkdir(parents=True,exist_ok=True)

APPS=[
("com.apple.mobilesafari","safari"),("com.apple.mobilemail","mail"),("com.apple.mobilephone","phone"),
("com.apple.MobileSMS","messages"),("com.apple.Preferences","settings"),("com.apple.camera","camera"),
("com.apple.mobileslideshow","photos"),("com.apple.Music","music"),("com.apple.mobilecal","calendar"),
("com.apple.Maps","maps"),("com.apple.weather","weather"),("com.apple.AppStore","appstore"),
("com.apple.calculator","calculator"),("com.apple.VoiceMemos","voice"),("com.apple.compass","compass"),
("com.apple.stocks","chart"),("com.apple.reminders","checklist"),("com.apple.notes","notes"),
("com.apple.facetime","video"),("com.apple.podcasts","podcast"),("com.apple.iBooks","book"),
("com.apple.findmyiphone","radar"),("com.apple.mobiletimer","clock"),("com.apple.Health","heart"),
("com.apple.Home","home"),("com.apple.Passbook","wallet"),("com.apple.shortcuts","shortcuts"),
("com.apple.tips","bulb"),("com.apple.measure","ruler"),("com.apple.MobileAddressBook","contacts"),
("com.facebook.Facebook","social"),("com.burbn.instagram","camera"),("net.whatsapp.WhatsApp","messages"),
("ph.telegra.Telegraph","paperplane"),("com.google.ios.youtube","play"),("com.google.Gmail","mail"),
("com.google.chrome.ios","globe"),("com.spotify.client","music"),("com.netflix.Netflix","play"),
("com.discord.Discord","game"),("com.zhiliaoapp.musically","music"),("com.snapchat.snapchat","camera"),
("com.reddit.Reddit","community"),("com.twitter.twitter","social"),("com.pinterest","pin"),
("tv.twitch","game"),("com.microsoft.Office.Outlook","mail"),("com.microsoft.skype","video"),
("com.microsoft.OneDrive","cloud"),("com.microsoft.teams","people"),("com.slack","chat"),
("com.dropbox.Dropbox","cloud"),("com.amazon.Amazon","bag"),("com.ubercab.UberClient","car"),
("com.ubercab.UberEats","food"),("com.airbnb.app","home"),("com.booking.BookingApp","bed"),
("com.todoist.ios","checklist"),("com.notion.id","notes"),("com.openai.chat","spark"),
]
# Remove duplicate bundle IDs while preserving order.
APPS=list(dict((x[0],x) for x in reversed(APPS)).values())[::-1]

def draw_glyph(d,kind,cx=256,cy=252):
    white=(244,251,255,245); pale=(180,225,248,220)
    def line(points,w=18,fill=white): d.line(points,fill=fill,width=w,joint="curve")
    if kind in ("phone","video"):
        d.rounded_rectangle((170,112,342,392),radius=34,outline=white,width=18)
        line([(218,145),(294,145)],10,pale); d.ellipse((242,350,270,378),outline=pale,width=9)
        if kind=="video":
            d.polygon([(342,205),(402,172),(402,330),(342,297)],fill=pale)
    elif kind in ("messages","chat","social","community"):
        d.rounded_rectangle((112,132,400,340),radius=48,outline=white,width=18)
        d.polygon([(170,330),(142,390),(238,340)],fill=white)
        for x in (195,256,317): d.ellipse((x-10,226,x+10,246),fill=pale)
    elif kind in ("camera",):
        d.rounded_rectangle((112,168,400,360),radius=38,outline=white,width=18)
        d.rounded_rectangle((185,132,265,178),radius=12,fill=pale)
        d.ellipse((198,210,316,328),outline=white,width=18); d.ellipse((232,244,282,294),fill=pale)
    elif kind in ("mail",):
        d.rounded_rectangle((102,166,410,350),radius=28,outline=white,width=18)
        line([(118,190),(256,292),(394,190)],18,pale)
    elif kind in ("music",):
        line([(290,120),(290,315),18,white); line([(290,130),(385,105),(385,295)],18,white)
        d.ellipse((190,294,292,384),fill=pale); d.ellipse((285,274,390,365),fill=white)
    elif kind in ("play",):
        d.ellipse((105,105,407,407),outline=white,width=16); d.polygon([(220,165),(220,345),(355,255)],fill=pale)
    elif kind in ("settings",):
        d.ellipse((156,156,356,356),outline=white,width=24); d.ellipse((220,220,292,292),outline=pale,width=18)
        for a in range(0,360,45):
            r=118; x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
            d.rounded_rectangle((x-14,y-25,x+14,y+25),radius=8,fill=white)
    elif kind in ("clock","calendar"):
        d.ellipse((118,118,394,394),outline=white,width=18)
        line([(256,158),(256,258),(326,292)],18,pale)
        if kind=="calendar":
            d.rounded_rectangle((140,150,372,366),radius=24,outline=white,width=14)
            line([(140,210),(372,210)],12,pale)
            for x in (202,256,310):
                for y in (255,310): d.ellipse((x-8,y-8,x+8,y+8),fill=white)
    elif kind in ("heart",):
        d.arc((115,125,265,300),180,355,fill=white,width=22); d.arc((247,125,397,300),185,360,fill=white,width=22)
        line([(126,220),(256,382),(386,220)],22,white)
    elif kind in ("cloud","weather"):
        d.ellipse((125,205,290,360),outline=white,width=16); d.ellipse((205,145,350,330),outline=white,width=16)
        d.rounded_rectangle((145,250,360,350),radius=42,fill=(16,65,100,180),outline=white,width=14)
        line([(220,370),(200,405)],12,pale); line([(290,370),(270,405)],12,pale)
    elif kind in ("home",):
        d.polygon([(105,250),(256,115),(407,250),(375,250),(375,390),(137,390),(137,250)],outline=white,fill=(255,255,255,24))
        d.rectangle((220,285,292,390),outline=pale,width=14)
    elif kind in ("paperplane","pin","radar","compass"):
        if kind=="pin":
            d.ellipse((155,110,357,312),outline=white,width=18); d.polygon([(170,260),(256,410),(342,260)],fill=pale); d.ellipse((220,175,292,247),outline=pale,width=14)
        else:
            d.polygon([(118,235),(404,112),(300,398),(248,282)],outline=white,fill=(210,240,255,45)); line([(248,282),(404,112)],12,pale)
    elif kind in ("bag","wallet"):
        d.rounded_rectangle((130,190,382,370),radius=28,outline=white,width=18)
        d.arc((195,100,320,260),180,360,fill=pale,width=18); d.ellipse((295,260,330,295),fill=white)
    elif kind in ("checklist","notes","calculator","ruler"):
        d.rounded_rectangle((145,112,367,395),radius=24,outline=white,width=18)
        for y in (190,255,320):
            if kind=="checklist":
                line([(180,y),(198,y+18),(225,y-16)],12,pale); line([(248,y),(330,y)],10,white)
            else: line([(180,y),(330,y)],12,white)
        if kind=="calculator":
            for x in (205,256,307):
                for y in (205,270,335): d.ellipse((x-9,y-9,x+9,y+9),fill=pale)
    elif kind in ("globe","safari"):
        d.ellipse((116,116,396,396),outline=white,width=18)
        d.arc((185,116,327,396),90,270,fill=pale,width=14); d.arc((185,116,327,396),270,90,fill=pale,width=14)
        line([(128,220),(384,220)],12,pale); line([(128,292),(384,292)],12,pale)
    elif kind in ("spark","bulb"):
        if kind=="bulb":
            d.ellipse((175,110,337,290),outline=white,width=18); line([(210,300),(302,300)],18,pale); line([(218,340),(294,340)],18,white)
        else:
            for a in range(0,360,45):
                x=256+math.cos(math.radians(a))*118; y=252+math.sin(math.radians(a))*118
                line([(256,252),(x,y)],16,white)
            d.ellipse((215,211,297,293),fill=pale)
    elif kind in ("car","bed","food","people","game","podcast","book","chart","contacts","appstore"):
        if kind=="car":
            d.rounded_rectangle((115,220,397,340),radius=32,outline=white,width=18); d.polygon([(165,220),(215,155),(315,155),(360,220)],outline=pale,fill=(255,255,255,20))
            d.ellipse((160,310,220,370),fill=white); d.ellipse((300,310,360,370),fill=white)
        elif kind=="bed":
            d.rectangle((125,180,385,360),outline=white,width=18); d.rectangle((150,210,250,280),outline=pale,width=12); line([(125,300),(385,300)],14,white)
        elif kind=="people":
            for x,y in ((200,185),(310,185),(256,145)): d.ellipse((x-34,y-34,x+34,y+34),outline=white,width=13)
            d.arc((135,210,265,385),180,360,fill=pale,width=18); d.arc((245,210,375,385),180,360,fill=pale,width=18)
        elif kind=="book":
            d.polygon([(120,145),(250,175),(250,385),(120,350)],outline=white,fill=(255,255,255,20)); d.polygon([(392,145),(262,175),(262,385),(392,350)],outline=white,fill=(255,255,255,20)); line([(256,175),(256,385)],12,pale)
        else:
            d.rounded_rectangle((130,130,382,382),radius=48,outline=white,width=18); d.ellipse((205,205,307,307),outline=pale,width=16)
    else:
        d.ellipse((125,125,387,387),outline=white,width=18); d.ellipse((205,205,307,307),fill=pale)

def icon(kind,seed,size=512):
    random.seed(seed)
    im=Image.new("RGBA",(size,size),(5,25,45,255))
    px=im.load()
    for y in range(size):
        for x in range(size):
            g=max(0,1-math.sqrt(((x-size*.22)/(size*.9))**2+((y-size*.1)/(size*.75))**2))
            px[x,y]=(int(5+24*g),int(31+80*g),int(52+115*g),255)
    d=ImageDraw.Draw(im,"RGBA")
    d.rounded_rectangle((8,8,size-8,size-8),radius=int(size*.22),outline=(235,250,255,210),width=5)
    d.rounded_rectangle((22,22,size-22,size*.43),radius=80,fill=(255,255,255,22))
    # render glyph on 512 canvas; resize after for precise 2x assets
    draw_glyph(d,kind)
    return im

for bundle,kind in APPS:
    seed=sum((i+1)*ord(c) for i,c in enumerate(bundle))
    master=icon(kind,seed,512)
    master.save(MASTER/(bundle+".png"),optimize=True)
    master.resize((120,120),Image.Resampling.LANCZOS).save(ICON_DIR/(bundle+".png"),optimize=True)

# Settings preference glyphs: iOS 12 uses com.apple.preferences-framework.
settings=[
("AirplaneMode","paperplane"),("WiFi","globe"),("Bluetooth","spark"),("Cellular","chart"),
("Notifications","bell"),("Sounds","music"),("DoNotDisturb","moon"),("General","settings"),
("Display","bulb"),("Wallpaper","photos"),("Siri","spark"),("Privacy","shield"),
("Battery","battery"),("Accessibility","people"),("ControlCenter","settings"),
("EmergencySOS","heart"),("FaceID","people"),("iCloud","cloud"),("Passwords","wallet")
]
for name,kind in settings:
    im=icon(kind,hash(name)%100000)
    im.resize((58,58),Image.Resampling.LANCZOS).save(SETTINGS/(name+"@2x.png"),optimize=True)
    im.resize((87,87),Image.Resampling.LANCZOS).save(SETTINGS/(name+"@3x.png"),optimize=True)

# Add required SnowBoard theme metadata.
plist=THEME/"Info.plist"
with plist.open("rb") as f: info=plistlib.load(f)
info["PackageName"]="NOVA Glass"
info["ThemeType"]="Icons"
info["ThemeName"]="NOVA Glass"
info["ThemeVersion"]="4.0.0"
info["ThemeDescription"]="Frosted glass iconography and iOS 12 Settings glyphs for iPhone 5s."
with plist.open("wb") as f: plistlib.dump(info,f,sort_keys=False)
print("Generated",len(APPS),"recognizable pictogram app icons and",len(settings),"Settings icon families.")
