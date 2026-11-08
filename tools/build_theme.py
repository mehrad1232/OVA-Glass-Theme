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
GLASS_PALETTES=[
    (34,128,180),(72,91,190),(20,147,154),(55,130,145),
    (101,88,176),(35,155,130),(35,112,172),(120,95,170),
    (26,141,178),(72,122,158),(43,156,170),(84,104,183)
]
def font(size):
    for p in FONT_PATHS:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def app_color(bundle):
    seed=sum((i+1)*ord(c) for i,c in enumerate(bundle))
    return GLASS_PALETTES[seed % len(GLASS_PALETTES)]

def glass_icon(bundle, label, initials, size=512):
    color=app_color(bundle)
    im=Image.new("RGBA",(size,size),(0,0,0,0))
    pix=im.load()
    top=(max(0,color[0]//2),max(0,color[1]//2),max(0,color[2]//2))
    bottom=(min(255,color[0]+42),min(255,color[1]+54),min(255,color[2]+62))
    for y in range(size):
        t=y/(size-1)
        row=tuple(int(top[i]+(bottom[i]-top[i])*t) for i in range(3))
        for x in range(size):
            horizontal=max(0.0,1.0-abs(x-size*.5)/(size*.75))
            lift=int(18*horizontal*(1-t))
            pix[x,y]=(min(255,row[0]+lift),min(255,row[1]+lift),min(255,row[2]+lift),255)
    mask=Image.new("L",(size,size),0)
    md=ImageDraw.Draw(mask)
    md.rounded_rectangle((2,2,size-3,size-3),radius=int(size*.22),fill=255)
    im.putalpha(mask)
    glow=Image.new("RGBA",(size,size),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((size*.08,size*.02,size*.92,size*.76),fill=(color[0],color[1],color[2],58))
    glow=glow.filter(ImageFilter.GaussianBlur(max(2,int(size*.075))))
    im=Image.alpha_composite(im,glow)
    im.putalpha(mask)
    d=ImageDraw.Draw(im,"RGBA")
    d.polygon([(size*.05,size*.07),(size*.95,size*.07),(size*.63,size*.34),(size*.17,size*.31)],fill=(255,255,255,30))
    d.rounded_rectangle((size*.025,size*.025,size*.975,size*.975),radius=int(size*.22),outline=(231,249,255,220),width=max(2,size//85))
    d.rounded_rectangle((size*.055,size*.055,size*.945,size*.945),radius=int(size*.19),outline=(255,255,255,95),width=max(1,size//150))
    d.ellipse((size*.205,size*.205,size*.795,size*.795),fill=(255,255,255,20),outline=(235,250,255,145),width=max(2,size//95))
    d.arc((size*.245,size*.225,size*.755,size*.735),190,330,fill=(255,255,255,155),width=max(2,size//90))
    f=font(int(size*.245))
    d.text((size/2,size*.49),initials,font=f,fill=(250,254,255,248),anchor="mm",stroke_width=max(1,size//260),stroke_fill=(color[0],color[1],color[2],190))
    d.rounded_rectangle((size*.17,size*.835,size*.83,size*.89),radius=int(size*.025),fill=(238,250,255,72),outline=(255,255,255,70),width=max(1,size//220))
    return im

for bundle,label,initials in APPS:
    master=glass_icon(bundle,label,initials,512)
    master.save(MASTERS/"Icons"/(bundle+".png"),format="PNG",optimize=True)
    master.resize((120,120),Image.Resampling.LANCZOS).save(ICONS/(bundle+".png"),format="PNG",optimize=True)

# Full-size 1170x2532 master art plus correctly sized 640x1136 iPhone 5s versions.
WALLSPECS=[
("NOVA-Glass-Day-iPhone5s.png","NOVA-Glass-Day-Master.png",((12,43,78),(39,139,184),(8,20,42)),101,False),
("NOVA-Glass-Golden-iPhone5s.png","NOVA-Glass-Golden-Master.png",((54,73,105),(226,151,104),(27,29,62)),202,False),
("NOVA-Glass-Dusk-iPhone5s.png","NOVA-Glass-Dusk-Master.png",((26,36,83),(113,94,155),(8,12,38)),303,False),
("NOVA-Glass-Night-iPhone5s.png","NOVA-Glass-Night-Master.png",((2,9,28),(19,43,82),(1,4,16)),404,True),
("NOVA-Glass-Aurora-iPhone5s.png","NOVA-Glass-Aurora-Master.png",((4,21,48),(22,100,111),(2,8,27)),505,True),
("NOVA-Glass-Snow-iPhone5s.png","NOVA-Glass-Snow-Master.png",((8,19,43),(53,82,119),(3,8,20)),606,True),
]
def mix(a,b,t):
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def wallpaper(path, width, height, palette, seed, snow):
    rng=random.Random(seed)
    im=Image.new("RGB",(width,height))
    p=im.load()
    for y in range(height):
        t=y/(height-1)
        base=mix(palette[0],palette[1],min(1.0,t/0.48)) if t<0.48 else mix(palette[1],palette[2],(t-0.48)/0.52)
        for x in range(width):
            gx=max(0.0,1.0-abs(x-width*.24)/(width*.82))
            lift=int(28*gx*(1.0-t))
            p[x,y]=(min(255,base[0]+lift),min(255,base[1]+lift),min(255,base[2]+lift))
    overlay=Image.new("RGBA",(width,height),(0,0,0,0))
    d=ImageDraw.Draw(overlay,"RGBA")
    if seed in (101,202):
        sx=int(width*.22); sy=int(height*.17); radius=int(width*.23)
        d.ellipse((sx-radius,sy-radius,sx+radius,sy+radius),fill=(255,225,155,28),outline=(255,247,220,72),width=max(1,width//320))
        d.ellipse((sx-radius*.0,sy-radius*.0,sx+radius*.0,sy+radius*.0),fill=(255,245,205,0))
    if seed==505:
        for band in range(3):
            points=[]
            for x in range(-width//8,width+width//8,8):
                y=int(height*(.24+band*.09)+math.sin((x/width)*math.pi*2+band)*height*.035)
                points.append((x,y))
            d.line(points,fill=(65+band*22,210-band*18,220,40),width=max(4,width//35))
    d.ellipse((-width*.38,-height*.24,width*.74,height*.42),outline=(235,250,255,65),width=max(2,width//360))
    d.ellipse((width*.48,height*.54,width*1.35,height*1.14),outline=(185,225,255,48),width=max(2,width//420))
    if snow:
        count=max(50,int(width*height/7000))
        for _ in range(count):
            x=rng.randrange(width); y=rng.randrange(height); r=rng.choice((1,1,2,max(2,width//900)))
            d.ellipse((x-r,y-r,x+r,y+r),fill=(239,249,255,rng.randrange(95,220)))
    im=Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
    im.save(path,format="PNG",optimize=True)

for small,master,palette,seed,snow in WALLSPECS:
    wallpaper(MASTERS/"Wallpapers"/master,1170,2532,palette,seed,snow)
    wallpaper(WALLS/small,640,1136,palette,seed,snow)

# This HTML is a desktop/browser preview only; the live SpringBoard effect is in NOVAWeather.
(THEME/"Wallpaper-Preview.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOVA Glass Live Preview</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
body{background:linear-gradient(155deg,#183d62,#246f8d 45%,#07152b);transition:background 2s}
body[data-mode="night"]{background:linear-gradient(155deg,#020814,#102447 55%,#01040c)}
body[data-mode="dusk"]{background:linear-gradient(155deg,#27395d,#76506c 50%,#0a1228)}
.sun{position:absolute;inset:-35% -15% auto;height:80%;background:radial-gradient(ellipse at 40% 45%,rgba(255,248,206,.88),rgba(255,211,126,.3) 30%,transparent 70%);filter:blur(12px);opacity:0;transition:opacity 2s}
body[data-mode="day"] .sun{opacity:1}
.glass{position:absolute;left:8%;right:8%;top:19%;height:38%;border:1px solid #ffffff80;border-radius:30px;background:linear-gradient(135deg,#ffffff28,#ffffff05);box-shadow:inset 0 1px 2px #ffffff66,0 18px 55px #0005;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);padding:24px}
#clock{font-size:58px;font-weight:200;letter-spacing:-3px}#date{opacity:.8}
.snow{position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity 1.5s}
body[data-mode="night"] .snow{opacity:1}
.flake{position:absolute;top:-5%;width:3px;height:3px;border-radius:50%;background:#fff;box-shadow:0 0 8px #fff;animation:fall linear infinite}
@keyframes fall{to{transform:translate3d(28px,115vh,0)}}
</style></head>
<body data-mode="night"><div class="sun"></div><div class="glass"><div id="clock"></div><div id="date"></div></div><div class="snow" id="snow"></div>
<script>
(function(){
 var snow=document.getElementById('snow');
 for(var i=0;i<42;i++){var f=document.createElement('i');f.className='flake';f.style.left=(Math.random()*100)+'%';f.style.animationDuration=(7+Math.random()*9)+'s';f.style.animationDelay=(-Math.random()*14)+'s';f.style.opacity=(.25+Math.random()*.75).toString();snow.appendChild(f);}
 function tick(){var d=new Date(),h=d.getHours();document.body.dataset.mode=(h>=7&&h<14)?'day':(h>=19||h<7)?'night':'dusk';document.getElementById('clock').textContent=d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});document.getElementById('date').textContent=d.toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'});}
 tick();setInterval(tick,60000);
})();
</script></body></html>""",encoding="utf-8")

legacy=THEME/"Wallpaper.html"
if legacy.exists(): legacy.unlink()

plist=THEME/"Info.plist"
with plist.open("rb") as f: info=plistlib.load(f)
info["PackageName"]="NOVA Glass"
info["ThemeName"]="NOVA Glass"
info["ThemeType"]="Icons"
info["ThemeVersion"]="4.0.0"
info["ThemeDescription"]="Glossy glass icon artwork and six static wallpapers. Live time-based sunlight and snowfall require the separate NOVAWeather iOS 12 tweak."
with plist.open("wb") as f: plistlib.dump(info,f,sort_keys=False)
with plist.open("rb") as f: plistlib.load(f)

icons=list(ICONS.glob("*.png"))
masters=list((MASTERS/"Icons").glob("*.png"))
wallpapers=list(WALLS.glob("*.png"))
wall_masters=list((MASTERS/"Wallpapers").glob("*.png"))
assert len(icons)>=70, f"Expected at least 70 unique icons, got {len(icons)}"
assert len(masters)==len(icons), "Every active icon must have a source master"
assert len(wallpapers)==6 and len(wall_masters)==6
for p in icons:
    with Image.open(p) as im:
        assert im.format=="PNG" and im.size==(120,120) and im.mode=="RGBA",p
        assert im.getpixel((0,0))[3]==0, f"Icon corner must be transparent: {p}"
for p in masters:
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(512,512) and im.mode=="RGBA",p
for p in wallpapers:
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(640,1136),p
for p in wall_masters:
    with Image.open(p) as im: assert im.format=="PNG" and im.size==(1170,2532),p
assert not legacy.exists(), "Legacy Wallpaper.html must not be packaged as a SnowBoard live wallpaper"
assert (THEME/"Wallpaper-Preview.html").exists()
print(f"PASS: NOVA Glass v4.0.0; {len(icons)} transparent SnowBoard icons; 6 iPhone 5s wallpapers; 6 master wallpapers; preview only; legacy HTML removed.")
