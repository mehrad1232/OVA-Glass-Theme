#!/usr/bin/env python3
"""Generate NOVA Glass artwork: SnowBoard-ready icons plus editable high-resolution masters."""
from pathlib import Path
import math, random, plistlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
THEME=ROOT/"NOVA Glass.theme"
ICONS=THEME/"IconBundles"
WALLS=THEME/"Wallpapers"
MASTERS=THEME/"Artwork-Source"
for p in (ICONS,WALLS,MASTERS/"Icons",MASTERS/"Wallpapers"): p.mkdir(parents=True,exist_ok=True)

# Bundle identifiers are filenames SnowBoard can match. Third-party identifiers are best-effort;
# SnowBoard only applies an icon when the installed app uses the same bundle identifier.
APPS=[
("com.apple.mobilesafari","Safari","SA"),("com.apple.mobilemail","Mail","ML"),
("com.apple.mobilephone","Phone","PH"),("com.apple.MobileSMS","Messages","MS"),
("com.apple.Preferences","Settings","ST"),("com.apple.camera","Camera","CA"),
("com.apple.mobileslideshow","Photos","PO"),("com.apple.Music","Music","MU"),
("com.apple.mobilecal","Calendar","CA"),("com.apple.Maps","Maps","MP"),
("com.apple.weather","Weather","WE"),("com.apple.AppStore","App Store","AS"),
("com.apple.calculator","Calculator","CL"),("com.apple.VoiceMemos","Voice Memos","VM"),
("com.apple.compass","Compass","CO"),("com.apple.stocks","Stocks","SK"),
("com.apple.reminders","Reminders","RE"),("com.apple.notes","Notes","NO"),
("com.apple.facetime","FaceTime","FT"),("com.apple.podcasts","Podcasts","PC"),
("com.apple.iBooks","Books","BK"),("com.apple.findmyiphone","Find My","FM"),
("com.apple.mobiletimer","Clock","CK"),("com.apple.Health","Health","HE"),
("com.apple.Home","Home","HO"),("com.apple.Passbook","Wallet","WA"),
("com.apple.shortcuts","Shortcuts","SH"),("com.apple.tips","Tips","TI"),
("com.apple.measure","Measure","ME"),("com.apple.MobileStore","iTunes","IT"),
("com.facebook.Facebook","Facebook","FB"),("com.burbn.instagram","Instagram","IG"),
("net.whatsapp.WhatsApp","WhatsApp","WA"),("ph.telegra.Telegraph","Telegram","TG"),
("com.google.ios.youtube","YouTube","YT"),("com.google.Gmail","Gmail","GM"),
("com.google.chrome.ios","Chrome","CH"),("com.spotify.client","Spotify","SP"),
("com.netflix.Netflix","Netflix","NF"),("com.discord.Discord","Discord","DC"),
("com.zhiliaoapp.musically","TikTok","TT"),("com.snapchat.snapchat","Snapchat","SC"),
("com.reddit.Reddit","Reddit","RD"),("com.twitter.twitter","X","X"),
("com.pinterest","Pinterest","PI"),("tv.twitch","Twitch","TW"),
("com.microsoft.Office.Outlook","Outlook","OU"),("com.microsoft.skype","Skype","SK"),
("com.microsoft.OneDrive","OneDrive","OD"),("com.microsoft.teams","Teams","TM"),
("com.slack","Slack","SL"),("com.dropbox.Dropbox","Dropbox","DB"),
("com.amazon.Amazon","Amazon","AM"),("com.amazon.mShop.iPhone","Amazon Shopping","AS"),
("com.ubercab.UberClient","Uber","UB"),("com.ubercab.UberEats","Uber Eats","UE"),
("com.airbnb.app","Airbnb","AB"),("com.booking.BookingApp","Booking","BK"),
("com.evernote.iPhone.Evernote","Evernote","EV"),("com.todoist.ios","Todoist","TD"),
("com.notion.id","Notion","NT"),("com.openai.chat","ChatGPT","AI"),
("com.apple.freeform","Freeform","FR"),("com.apple.Pages","Pages","PG"),
("com.apple.Numbers","Numbers","NU"),("com.apple.Keynote","Keynote","KN"),
("com.apple.iMovie","iMovie","IM"),("com.apple.garageband","GarageBand","GB"),
("com.apple.podcasts","Podcasts","PD"),("com.apple.stocks","Stocks","ST"),
("com.apple.Translate","Translate","TR"),("com.apple.Files","Files","FI"),
("com.apple.Store","Apple Store","AS"),("com.apple.Passwords","Passwords","PW"),
("com.apple.Books","Books","BO"),("com.apple.TV","TV","TV"),
("com.apple.Maps","Maps","MA"),("com.apple.mobiletimer","Clock","CL"),
("com.apple.MobileAddressBook","Contacts","CT"),("com.apple.MobileContacts","Contacts","CO"),
("com.apple.Videos","Videos","VI"),("com.apple.Remote","Remote","RM"),
("com.apple.GameCenter","Game Center","GC"),("com.apple.iTunesStore","iTunes Store","IS"),
("com.apple.Passbook","Wallet","WL"),("com.apple.mobileme.fmip1","Find My","FM"),
("com.apple.mobileslideshow","Photos","PH"),("com.apple.mobilemail","Mail","ML"),
("com.apple.camera","Camera","CM"),("com.apple.mobilephone","Phone","PH"),
("com.apple.MobileSMS","Messages","MS"),("com.apple.Preferences","Settings","ST"),
("com.apple.mobilesafari","Safari","SF"),("com.apple.Music","Music","MU"),
("com.apple.mobilecal","Calendar","CA"),("com.apple.AppStore","App Store","AP"),
]
# De-duplicate while retaining first canonical display entry.
APPS=list(dict((a[0],a) for a in reversed(APPS)).values())[::-1]
FONT_PATHS=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
def font(size):
    for p in FONT_PATHS:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def draw_app_glyph(d, bundle, size):
    """Draw a distinct, clean glass-style pictogram instead of relying on initials."""
    b=bundle.lower()
    cx=size/2; cy=size/2
    scale=size/512
    ink=(245,252,255,238); soft=(210,241,255,155)
    w=max(4,int(9*scale))
    def line(points, fill=ink, width=w):
        d.line([(int(x*scale),int(y*scale)) for x,y in points],fill=fill,width=width,joint="curve")
    if "mobilephone" in b or b.endswith(".phone"):
        d.arc((int(164*scale),int(164*scale),int(348*scale),int(348*scale)),35,225,fill=ink,width=w*3)
        line([(190,190),(222,220),(205,244),(268,307),(292,287),(322,320)],ink,w*3)
    elif "mail" in b or "outlook" in b or "gmail" in b:
        d.rounded_rectangle((145*scale,185*scale,367*scale,330*scale),radius=int(22*scale),outline=ink,width=w*2)
        line([(151,198),(256,278),(361,198)],ink,w*2)
    elif "sms" in b or "whatsapp" in b or "telegraph" in b or "discord" in b:
        d.rounded_rectangle((142*scale,166*scale,370*scale,316*scale),radius=int(42*scale),outline=ink,width=w*2)
        line([(205,316),(184,350),(252,316)],ink,w*2)
        for x in (214,256,298): d.ellipse((int((x-6)*scale),int(235*scale),int((x+6)*scale),int(247*scale)),fill=soft)
    elif "camera" in b:
        d.rounded_rectangle((140*scale,190*scale,372*scale,330*scale),radius=int(28*scale),outline=ink,width=w*2)
        d.ellipse((205*scale,215*scale,307*scale,317*scale),outline=ink,width=w*2)
        d.ellipse((235*scale,245*scale,277*scale,287*scale),outline=soft,width=w)
        d.rounded_rectangle((185*scale,168*scale,250*scale,198*scale),radius=int(9*scale),fill=soft)
    elif "safari" in b or "compass" in b or "maps" in b:
        d.ellipse((155*scale,155*scale,357*scale,357*scale),outline=ink,width=w*2)
        line([(290,190),(250,260),(220,325),(275,280),(310,205)],ink,w*2)
        d.ellipse((245*scale,245*scale,267*scale,267*scale),fill=soft)
    elif "music" in b or "spotify" in b or "podcast" in b:
        line([(278,175),(278,302),(250,290),(225,300),(220,322),(240,337),(270,326),(292,307),(292,200),(344,213)],ink,w*3)
    elif "calendar" in b:
        d.rounded_rectangle((155*scale,165*scale,357*scale,350*scale),radius=int(22*scale),outline=ink,width=w*2)
        line([(155,220),(357,220)],ink,w*2)
        line([(205,145),(205,190)],ink,w*3); line([(307,145),(307,190)],ink,w*3)
        for x,y in [(205,260),(256,260),(307,260),(205,305),(256,305),(307,305)]:
            d.rounded_rectangle((int((x-9)*scale),int((y-9)*scale),int((x+9)*scale),int((y+9)*scale)),radius=int(5*scale),fill=soft)
    elif "photo" in b or "mobileslideshow" in b:
        for angle in range(0,360,60):
            import math
            a=math.radians(angle); x=cx+62*scale*math.cos(a); y=cy+62*scale*math.sin(a)
            d.ellipse((x-43*scale,y-43*scale,x+43*scale,y+43*scale),fill=(220,246,255,90),outline=ink,width=w)
        d.ellipse((cx-25*scale,cy-25*scale,cx+25*scale,cy+25*scale),fill=ink)
    elif "settings" in b or "preferences" in b:
        d.ellipse((180*scale,180*scale,332*scale,332*scale),outline=ink,width=w*3)
        d.ellipse((225*scale,225*scale,287*scale,287*scale),outline=soft,width=w*2)
        for angle in range(0,360,45):
            import math
            a=math.radians(angle); x1=cx+83*scale*math.cos(a); y1=cy+83*scale*math.sin(a)
            x2=cx+112*scale*math.cos(a); y2=cy+112*scale*math.sin(a)
            d.line((x1,y1,x2,y2),fill=ink,width=w*3)
    elif "weather" in b:
        d.ellipse((175*scale,210*scale,275*scale,310*scale),outline=ink,width=w*2)
        d.arc((190*scale,215*scale,365*scale,355*scale),180,360,fill=ink,width=w*2)
        line([(205,330),(335,330)],ink,w*2)
    elif "appstore" in b or "mobileinstaller" in b:
        line([(190,330),(256,180),(322,330)],ink,w*3); line([(218,270),(294,270)],ink,w*3)
        line([(205,190),(310,325)],soft,w*2)
    elif "clock" in b or "mobiletimer" in b:
        d.ellipse((160*scale,160*scale,352*scale,352*scale),outline=ink,width=w*2)
        line([(256,205),(256,260),(305,290)],ink,w*3)
    else:
        # A simple luminous monogram is the fallback for less common apps.
        f=font(int(size*.27))
        d.text((cx,cy),label[:1].upper(),font=f,fill=ink,anchor="mm")

def glass_icon(bundle, label, initials, size=512):
    seed=sum((i+1)*ord(c) for i,c in enumerate(bundle))
    rng=random.Random(seed)
    im=Image.new("RGB",(size,size))
    pix=im.load()
    for y in range(size):
        ty=y/(size-1)
        for x in range(size):
            glow=max(0,1-math.sqrt(((x-size*.27)/(size*.92))**2+((y-size*.12)/(size*.72))**2))
            lower=max(0,min(1,ty))
            base=(int(7+24*glow+8*lower),int(38+94*glow+18*lower),int(65+126*glow+24*lower))
            n=rng.randint(-13,13)
            pix[x,y]=tuple(max(0,min(255,v+n)) for v in base)
    d=ImageDraw.Draw(im,"RGBA")
    # Borderless liquid-glass layers: diffuse luminous wash, no hard icon outlines.
    d.rounded_rectangle((size*.035,size*.035,size*.965,size*.965),radius=int(size*.22),fill=(210,240,255,12))
    d.ellipse((size*.12,size*.10,size*.88,size*.86),fill=(225,247,255,18))
    d.ellipse((size*.23,size*.20,size*.77,size*.76),fill=(255,255,255,10))
    draw_app_glyph(d,bundle,size)
    d.ellipse((size*.20,size*.07,size*.72,size*.25),fill=(255,255,255,18))
    return im

for bundle,label,initials in APPS:
    master=glass_icon(bundle,label,initials,512)
    master.save(MASTERS/"Icons"/(bundle+".png"),format="PNG",optimize=False)
    master.resize((120,120),Image.Resampling.LANCZOS).save(ICONS/(bundle+".png"),format="PNG",optimize=True)

# Full-size 1170x2532 master art plus correctly sized 640x1136 iPhone 5s versions.
WALLSPECS=[
("NOVA-Glass-Pearl-iPhone5s.png","NOVA-Glass-Pearl-Master.png",((224,239,250),(170,211,236),(44,91,130)),91,False),
("NOVA-Glass-Day-iPhone5s.png","NOVA-Glass-Day-Master.png",((12,43,78),(39,139,184),(8,20,42)),101,False),
("NOVA-Glass-Lavender-iPhone5s.png","NOVA-Glass-Lavender-Master.png",((57,55,106),(168,143,209),(28,24,64)),192,False),
("NOVA-Glass-Golden-iPhone5s.png","NOVA-Glass-Golden-Master.png",((54,73,105),(226,151,104),(27,29,62)),202,False),
("NOVA-Glass-Rose-iPhone5s.png","NOVA-Glass-Rose-Master.png",((82,49,78),(210,139,161),(34,21,53)),293,False),
("NOVA-Glass-Dusk-iPhone5s.png","NOVA-Glass-Dusk-Master.png",((26,36,83),(113,94,155),(8,12,38)),303,False),
("NOVA-Glass-Night-iPhone5s.png","NOVA-Glass-Night-Master.png",((2,9,28),(19,43,82),(1,4,16)),404,True),
("NOVA-Glass-Aurora-iPhone5s.png","NOVA-Glass-Aurora-Master.png",((4,21,48),(22,100,111),(2,8,27)),505,True),
("NOVA-Glass-Snow-iPhone5s.png","NOVA-Glass-Snow-Master.png",((8,19,43),(53,82,119),(3,8,20)),606,True),
("NOVA-Glass-Mint-iPhone5s.png","NOVA-Glass-Mint-Master.png",((12,59,69),(77,169,163),(4,22,35)),707,True),
]
def wallpaper(path, width, height, palette, seed, snow):
    # Vectorized rendering keeps GitHub Actions builds fast even for 1170x2532 masters.
    import numpy as np
    rng=np.random.default_rng(seed)
    yy,xx=np.mgrid[0:height,0:width]
    x=xx.astype(np.float32); y=yy.astype(np.float32)
    glow=np.maximum(0,1-np.sqrt(((x-width*.22)/(width*.82))**2+((y-height*.12)/(height*.68))**2))
    t=y/max(1,height-1)
    arr=np.empty((height,width,3),dtype=np.float32)
    for c in range(3):
        arr[:,:,c]=palette[c][0]+(palette[c][1]-palette[c][0])*glow+(palette[c][2]-palette[c][0])*t
    arr += rng.integers(-18,19,size=(height,width,1),dtype=np.int16)
    arr=np.clip(arr,0,255).astype(np.uint8)
    im=Image.fromarray(arr,"RGB")
    d=ImageDraw.Draw(im,"RGBA")
    d.ellipse((-width*.35,-height*.25,width*.68,height*.34),fill=(165,225,255,20),outline=(235,250,255,75),width=max(2,width//400))
    d.ellipse((width*.48,height*.52,width*1.35,height*1.12),outline=(185,225,255,50),width=max(2,width//500))
    d.rounded_rectangle((width*.055,height*.035,width*.945,height*.965),radius=int(width*.08),outline=(225,245,255,55),width=max(2,width//500))
    if snow:
        for _ in range(int(width*height/6000)):
            x0=int(rng.integers(width)); y0=int(rng.integers(height))
            r=int(rng.choice((1,1,2,max(2,width//900))))
            d.ellipse((x0-r,y0-r,x0+r,y0+r),fill=(239,249,255,int(rng.integers(95,225))))
    im.save(path,format="PNG",optimize=False)

for small,master,palette,seed,snow in WALLSPECS:
    big=MASTERS/"Wallpapers"/master
    wallpaper(big,1170,2532,palette,seed,snow)
    wallpaper(WALLS/small,640,1136,palette,seed,snow)

# Keep a truthful static preview: HTML animation is only a preview, not an iOS live wallpaper.
(THEME/"Wallpaper-Preview.html").write_text("""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NOVA Glass Preview</title><style>*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#06152b}body{background:url('Wallpapers/NOVA-Glass-Night-iPhone5s.png') center/cover}.glass{position:absolute;left:8%;right:8%;top:20%;padding:25px;border:1px solid #ffffff77;border-radius:30px;background:#ffffff20;backdrop-filter:blur(18px);box-shadow:0 18px 55px #0007}#clock{font-size:58px;font-weight:200;letter-spacing:-3px}#date{opacity:.85}.snow{position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(2px 2px at 20% 30%,#fff9 99%,transparent),radial-gradient(2px 2px at 70% 60%,#fff8 99%,transparent);background-size:170px 190px;animation:fall 8s linear infinite}@keyframes fall{to{background-position:0 190px,0 190px}}</style></head><body><div class="glass"><div id="clock"></div><div id="date"></div></div><div class="snow"></div><script>function tick(){const d=new Date();document.getElementById('clock').textContent=d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});document.getElementById('date').textContent=d.toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'})}tick();setInterval(tick,1000)</script></body></html>""",encoding="utf-8")

plist=THEME/"Info.plist"
with plist.open("rb") as f: info=plistlib.load(f)
info["ThemeName"]="NOVA Glass"
info["ThemeVersion"]="3.0.0"
info["ThemeDescription"]="NOVA Glass: 96 SnowBoard icon artworks, six iPhone 5s wallpapers, and 1170x2532 editable master artwork."
with plist.open("wb") as f: plistlib.dump(info,f,sort_keys=False)
with plist.open("rb") as f: plistlib.load(f)

icons=list(ICONS.glob("*.png"))
assert len(icons)>=70, f"Expected at least 70 unique icons, got {len(icons)}"
for p in icons:
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(120,120),p
for p in WALLS.glob("*.png"):
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(640,1136),p
masters=list((MASTERS/"Icons").glob("*.png"))
assert len(masters)==len(icons)
for p in (MASTERS/"Wallpapers").glob("*.png"):
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(1170,2532),p
print(f"PASS: {len(icons)} SnowBoard icons, {len(masters)} 512px icon masters, 6 iPhone 5s wallpapers, 6 full-size wallpaper masters.")
