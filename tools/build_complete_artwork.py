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
for p in ICON_DIR.glob("*.png"): p.unlink()
for p in SETTINGS.glob("*.png"): p.unlink()

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
("com.apple.iTunesStore","appstore"),("com.apple.Pages","book"),("com.apple.Numbers","chart"),
("com.apple.Keynote","chart"),("com.apple.iMovie","video"),("com.apple.garageband","music"),
("com.apple.Translate","globe"),("com.apple.Files","folder"),("com.apple.Store","bag"),
("com.apple.TV","play"),("com.apple.Videos","play"),("com.apple.Remote","play"),
("com.apple.GameCenter","game"),("com.apple.mobileme.fmip1","radar"),
("com.google.Drive","cloud"),("com.google.Maps","globe"),("com.google.Photos","photos"),
("com.facebook.Messenger","chat"),("com.amazon.mShop.iPhone","bag"),
("com.evernote.iPhone.Evernote","notes"),("com.microsoft.skydrive","cloud"),
("com.google.Docs","book"),("com.google.Sheets","chart"),("com.google.Slides","chart"),
("com.apple.mobilephone","phone"),("com.apple.VoiceMemos","voice"),
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
        line([(290,120),(290,315)],18,white); line([(290,130),(385,105),(385,295)],18,white)
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
    # Premium borderless liquid-glass tile: no perimeter stroke or white frame.
    random.seed(seed)
    import numpy as np
    yy,xx=np.mgrid[0:size,0:size]
    x=xx.astype(np.float32); y=yy.astype(np.float32)
    palettes={
      "phone":(58,166,210),"video":(105,126,235),"messages":(67,190,150),
      "chat":(84,164,224),"social":(205,116,178),"community":(226,120,91),
      "camera":(185,145,214),"mail":(85,156,210),"music":(183,112,202),
      "play":(225,90,110),"settings":(115,153,185),"clock":(78,148,190),
      "calendar":(226,104,105),"heart":(223,105,137),"cloud":(102,165,205),
      "weather":(90,174,205),"home":(185,145,105),"paperplane":(87,167,218),
      "pin":(226,125,110),"radar":(93,183,171),"compass":(98,148,212),
      "bag":(194,151,104),"wallet":(186,151,104),"checklist":(94,177,149),
      "notes":(195,172,104),"calculator":(105,154,185),"ruler":(116,168,188),
      "globe":(83,156,202),"safari":(82,161,211),"spark":(150,163,225),
      "bulb":(224,182,91),"car":(105,158,191),"bed":(169,142,187),
      "food":(210,145,102),"people":(118,160,193),"game":(139,125,207),
      "podcast":(170,127,208),"book":(128,157,186),"chart":(85,169,158),
      "contacts":(102,164,190),"appstore":(92,157,208)
    }
    accent=palettes.get(kind,(112,158,190))
    # Smooth radial glass illumination, gently colored by app family.
    dx=(x-size*.27)/(size*.92); dy=(y-size*.16)/(size*.82)
    bloom=np.maximum(0,1-np.sqrt(dx*dx+dy*dy))**1.7
    lower=np.clip(y/(size-1),0,1)
    edge=np.clip(np.minimum.reduce([x,y,size-1-x,size-1-y])/(size*.18),0,1)
    arr=np.empty((size,size,4),dtype=np.uint8)
    for c,base in enumerate((7,22,39)):
        tint=accent[c]
        val=base + bloom*(tint*.54) + lower*(tint*.12) + np.maximum(0,1-np.sqrt(((x-size*.84)/(size*.55))**2+((y-size*.9)/(size*.5))**2))*(tint*.13)
        arr[:,:,c]=np.clip(val,0,255).astype(np.uint8)
    arr[:,:,3]=255
    im=Image.fromarray(arr,"RGBA")
    d=ImageDraw.Draw(im,"RGBA")
    # Diffuse glass reflections; highlights stay inside the icon silhouette.
    d.ellipse((size*.06,size*.015,size*.94,size*.60),fill=(220,245,255,13))
    d.ellipse((size*.16,size*.04,size*.83,size*.43),fill=(255,255,255,12))
    d.polygon([(size*.02,size*.03),(size*.76,size*.03),(size*.50,size*.13),(size*.12,size*.18)],fill=(255,255,255,12))
    # A soft colored halo behind the pictogram separates it from the background.
    halo=Image.new("RGBA",(size,size),(0,0,0,0))
    hd=ImageDraw.Draw(halo,"RGBA")
    hd.ellipse((size*.22,size*.20,size*.78,size*.78),fill=(*accent,42))
    halo=halo.filter(ImageFilter.GaussianBlur(size*.075))
    im=Image.alpha_composite(im,halo)
    d=ImageDraw.Draw(im,"RGBA")
    draw_glyph(d,kind)
    # Fine top reflection and lower refraction, not an outline around the tile.
    d.arc((size*.12,size*.08,size*.88,size*.74),198,338,fill=(255,255,255,28),width=max(1,size//170))
    d.ellipse((size*.18,size*.80,size*.82,size*1.08),fill=(*accent,13))
    mask=Image.new("L",(size,size),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,size-1,size-1),radius=int(size*.225),fill=255)
    im.putalpha(mask)
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
    im=icon(kind,sum(ord(ch)*(i+1) for i,ch in enumerate(name)))
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
