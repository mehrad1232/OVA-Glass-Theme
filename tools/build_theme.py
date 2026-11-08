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

def draw_symbol(d,label,size,color):
    cx=size/2; cy=size*.49; u=size*.22; w=max(3,size//32)
    white=(250,254,255,235); soft=(230,248,255,190)
    def line(points,width=w): d.line(points,fill=white,width=width,joint="curve")
    if label in ("Safari","Compass"):
        d.ellipse((cx-u,cy-u,cx+u,cy+u),outline=white,width=w)
        d.polygon([(cx,cy-u*.72),(cx+u*.22,cy+u*.12),(cx-u*.12,cy+u*.48),(cx-u*.05,cy-u*.05)],fill=(255,255,255,225))
        d.polygon([(cx,cy+u*.72),(cx-u*.22,cy-u*.12),(cx+u*.12,cy-u*.48),(cx+u*.05,cy+u*.05)],fill=(110,210,255,200))
    elif label in ("Mail","Gmail","Outlook"):
        d.rounded_rectangle((cx-u*1.15,cy-u*.72,cx+u*1.15,cy+u*.72),radius=int(u*.16),outline=white,width=w)
        line([(cx-u*1.05,cy-u*.58),(cx,cy+u*.12),(cx+u*1.05,cy-u*.58)])
    elif label in ("Phone",):
        d.arc((cx-u,cy-u,cx+u,cy+u),35,225,fill=white,width=w*2)
        d.rounded_rectangle((cx-u*.82,cy-u*.82,cx-u*.38,cy-u*.38),radius=int(u*.15),fill=white)
        d.rounded_rectangle((cx+u*.38,cy+u*.38,cx+u*.82,cy+u*.82),radius=int(u*.15),fill=white)
    elif label in ("Messages","WhatsApp","Telegram","Discord","Slack","Facebook"):
        d.rounded_rectangle((cx-u*1.1,cy-u*.72,cx+u*1.1,cy+u*.55),radius=int(u*.3),outline=white,width=w)
        d.polygon([(cx-u*.45,cy+u*.52),(cx-u*.72,cy+u*.9),(cx+u*.02,cy+u*.55)],fill=white)
        for k in (-.42,0,.42): d.ellipse((cx+u*k-u*.09,cy-u*.08,cx+u*k+u*.09,cy+u*.1),fill=white)
    elif label in ("Settings",):
        d.ellipse((cx-u*.72,cy-u*.72,cx+u*.72,cy+u*.72),outline=white,width=w*2)
        d.ellipse((cx-u*.28,cy-u*.28,cx+u*.28,cy+u*.28),outline=white,width=w*2)
        for a in range(0,360,45):
            r1=u*.78; r2=u*1.12
            x1=cx+math.cos(math.radians(a))*r1; y1=cy+math.sin(math.radians(a))*r1
            x2=cx+math.cos(math.radians(a))*r2; y2=cy+math.sin(math.radians(a))*r2
            line([(x1,y1),(x2,y2)],w*2)
    elif label in ("Camera","FaceTime"):
        d.rounded_rectangle((cx-u*1.1,cy-u*.58,cx+u*1.1,cy+u*.62),radius=int(u*.2),outline=white,width=w)
        d.ellipse((cx-u*.38,cy-u*.38,cx+u*.38,cy+u*.38),outline=white,width=w*2)
        if label=="FaceTime": d.polygon([(cx+u*.95,cy-u*.3),(cx+u*1.45,cy-u*.58),(cx+u*1.45,cy+u*.58),(cx+u*.95,cy+u*.3)],outline=white)
    elif label in ("Photos",):
        for a in range(0,360,60):
            x=cx+math.cos(math.radians(a))*u*.48; y=cy+math.sin(math.radians(a))*u*.48
            d.ellipse((x-u*.43,y-u*.43,x+u*.43,y+u*.43),fill=(255,255,255,115),outline=soft,width=max(2,w//2))
    elif label in ("Music","Spotify","Podcasts","iTunes","iTunes Store","GarageBand"):
        if label=="Podcasts":
            d.ellipse((cx-u,cy-u,cx+u,cy+u),outline=white,width=w)
            d.ellipse((cx-u*.55,cy-u*.55,cx+u*.55,cy+u*.55),outline=white,width=w)
            d.ellipse((cx-u*.16,cy-u*.16,cx+u*.16,cy+u*.16),fill=white)
        else:
            line([(cx+u*.15,cy-u*.9),(cx+u*.15,cy+u*.45)],w*2)
            line([(cx+u*.15,cy-u*.9),(cx+u*.9,cy-u*1.05)],w*2)
            d.ellipse((cx-u*.62,cy+u*.22,cx+u*.16,cy+u*.82),fill=white)
            d.ellipse((cx-u*.08,cy+u*.08,cx+u*.7,cy+u*.68),fill=white)
    elif label in ("Calendar",):
        d.rounded_rectangle((cx-u,cy-u,cx+u,cy+u),radius=int(u*.15),outline=white,width=w)
        line([(cx-u,cy-u*.45),(cx+u,cy-u*.45)],w*2)
        for x in (-.45,0,.45):
            for y in (-.05,.42): d.ellipse((cx+u*x-u*.07,cy+u*y-u*.07,cx+u*x+u*.07,cy+u*y+u*.07),fill=white)
    elif label in ("Maps",):
        d.polygon([(cx-u*1.1,cy-u*.8),(cx-u*.35,cy-u*.55),(cx+u*.35,cy-u*.8),(cx+u*1.1,cy-u*.55),(cx+u*1.1,cy+u*.8),(cx+u*.35,cy+u*.55),(cx-u*.35,cy+u*.8),(cx-u*1.1,cy+u*.55)],outline=white)
        line([(cx-u*.35,cy-u*.55),(cx-u*.35,cy+u*.8)],w)
        line([(cx+u*.35,cy-u*.8),(cx+u*.35,cy+u*.55)],w)
        line([(cx-u*.7,cy+u*.3),(cx-u*.1,cy-u*.15),(cx+u*.4,cy+u*.18)],w*2)
    elif label in ("Weather",):
        d.ellipse((cx-u*.45,cy-u*.85,cx+u*.45,cy+u*.05),fill=(255,231,150,225))
        d.arc((cx-u*1.1,cy-u*.3,cx+u*.9,cy+u*1.1),180,360,fill=white,width=w*2)
        d.line((cx-u*.9,cy+u*.45,cx+u*.85,cy+u*.45),fill=white,width=w*2)
    elif label in ("App Store","Apple Store"):
        line([(cx-u*.8,cy+u*.8),(cx+u*.8,cy-u*.8)],w*2)
        line([(cx-u*.8,cy-u*.8),(cx+u*.8,cy+u*.8)],w*2)
        line([(cx-u*.95,cy+u*.2),(cx+u*.95,cy+u*.2)],w*2)
    elif label in ("Calculator",):
        d.rounded_rectangle((cx-u,cy-u,cx+u,cy+u),radius=int(u*.15),outline=white,width=w)
        for x in (-.35,.35):
            for y in (-.3,.25,.7): d.ellipse((cx+u*x-u*.11,cy+u*y-u*.11,cx+u*x+u*.11,cy+u*y+u*.11),fill=white)
    elif label in ("Voice Memos",):
        for i,h in enumerate((.25,.55,.9,.45,.72,.35,.6)):
            x=cx-u*.9+i*u*.3
            line([(x,cy-u*h),(x,cy+u*h)],w*2)
    elif label in ("Stocks",):
        line([(cx-u,cy+u*.65),(cx-u*.45,cy+u*.1),(cx-u*.05,cy+u*.3),(cx+u*.45,cy-u*.55),(cx+u,cy-u*.2)],w*2)
        for x,y in ((-1,.65),(-.45,.1),(-.05,.3),(.45,-.55),(1,-.2)):
            d.ellipse((cx+u*x-u*.08,cy+u*y-u*.08,cx+u*x+u*.08,cy+u*y+u*.08),fill=white)
    elif label in ("Reminders",):
        for y in (-.55,0,.55):
            d.ellipse((cx-u,cy+u*y-u*.12,cx-u+u*.24,cy+u*y+u*.12),outline=white,width=w)
            line([(cx-u*.55,cy+u*y),(cx+u,cy+u*y)],w*2)
    elif label in ("Notes","Files","Passwords","Translate","Tips"):
        d.rounded_rectangle((cx-u*.8,cy-u,cx+u*.8,cy+u),radius=int(u*.12),outline=white,width=w)
        if label=="Tips":
            d.ellipse((cx-u*.35,cy-u*.55,cx+u*.35,cy+u*.15),outline=white,width=w*2)
            line([(cx-u*.2,cy+u*.25),(cx+u*.2,cy+u*.25)],w*2)
            line([(cx-u*.15,cy+u*.48),(cx+u*.15,cy+u*.48)],w*2)
        else:
            for y in (-.45,0,.45): line([(cx-u*.45,cy+u*y),(cx+u*.45,cy+u*y)],w)
    elif label in ("Books",):
        d.polygon([(cx,cy-u*.8),(cx-u,cy-u),(cx-u,cy+u*.8),(cx,cy+u),(cx,cy-u*.8),(cx+u,cy-u),(cx+u,cy+u*.8),(cx,cy+u)],outline=white)
        line([(cx,cy-u*.8),(cx,cy+u)],w)
    elif label in ("Find My",):
        for radius in (u*.35,u*.7,u*1.05): d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=white,width=max(2,w//2))
        d.ellipse((cx-u*.12,cy-u*.12,cx+u*.12,cy+u*.12),fill=white)
    elif label in ("Clock",):
        d.ellipse((cx-u,cy-u,cx+u,cy+u),outline=white,width=w*2)
        line([(cx,cy),(cx,cy-u*.62)],w*2); line([(cx,cy),(cx+u*.55,cy+u*.15)],w*2)
    elif label in ("Health",):
        pts=[(cx,cy+u*.9),(cx-u*1.0,cy-u*.05),(cx-u*.8,cy-u*.75),(cx-u*.25,cy-u*.7),(cx,cy-u*.25),(cx+u*.25,cy-u*.7),(cx+u*.8,cy-u*.75),(cx+u,cy-u*.05)]
        d.polygon(pts,fill=(255,255,255,205))
    elif label in ("Home",):
        d.polygon([(cx-u*1.15,cy),(cx,cy-u),(cx+u*1.15,cy),(cx+u*.85,cy+u),(cx-u*.85,cy+u)],outline=white)
        d.rectangle((cx-u*.25,cy+u*.15,cx+u*.25,cy+u),outline=white,width=w)
    elif label in ("Wallet",):
        d.rounded_rectangle((cx-u*1.1,cy-u*.65,cx+u*1.1,cy+u*.65),radius=int(u*.15),outline=white,width=w)
        d.rounded_rectangle((cx+u*.25,cy-u*.25,cx+u*1.1,cy+u*.25),radius=int(u*.1),outline=white,width=w)
        d.ellipse((cx+u*.45,cy-u*.06,cx+u*.58,cy+u*.06),fill=white)
    elif label in ("Shortcuts",):
        d.polygon([(cx-u,cy),(cx-u*.35,cy-u*.75),(cx+u*.3,cy),(cx-u*.35,cy+u*.75)],outline=white)
        d.polygon([(cx-u*.1,cy),(cx+u*.55,cy-u*.75),(cx+u,cy),(cx+u*.55,cy+u*.75)],outline=white)
    elif label in ("Measure",):
        d.rounded_rectangle((cx-u*1.1,cy-u*.35,cx+u*1.1,cy+u*.35),radius=int(u*.1),outline=white,width=w)
        for i in range(7):
            x=cx-u*.9+i*u*.3
            line([(x,cy-u*.3),(x,cy-u*(.08 if i%2 else .18))],w)
    elif label in ("Videos","TV","iMovie","Game Center"):
        d.rounded_rectangle((cx-u,cy-u*.7,cx+u,cy+u*.7),radius=int(u*.16),outline=white,width=w)
        d.polygon([(cx-u*.25,cy-u*.38),(cx+u*.45,cy),(cx-u*.25,cy+u*.38)],fill=white)
    elif label in ("Contacts",):
        d.ellipse((cx-u*.32,cy-u*.85,cx+u*.32,cy-u*.2),outline=white,width=w*2)
        d.arc((cx-u,cy-u*.15,cx+u,cy+u),180,360,fill=white,width=w*2)
    else:
        return False
    return True

def glass_icon(bundle, label, initials, size=512):
    color=app_color(bundle)
    im=Image.new("RGBA",(size,size),(0,0,0,0))
    top=(max(0,color[0]//2),max(0,color[1]//2),max(0,color[2]//2))
    bottom=(min(255,color[0]+42),min(255,color[1]+54),min(255,color[2]+62))
    gradient=ImageDraw.Draw(im)
    for y in range(size):
        t=y/(size-1)
        row=tuple(int(top[i]+(bottom[i]-top[i])*t) for i in range(3))
        gradient.line((0,y,size,y),fill=(*row,255))
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
    if not draw_symbol(d,label,size,color):
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
    gradient=ImageDraw.Draw(im)
    for y in range(height):
        t=y/(height-1)
        base=mix(palette[0],palette[1],min(1.0,t/0.48)) if t<0.48 else mix(palette[1],palette[2],(t-0.48)/0.52)
        gradient.line((0,y,width,y),fill=base)
    overlay=Image.new("RGBA",(width,height),(0,0,0,0))
    d=ImageDraw.Draw(overlay,"RGBA")
    if seed in (101,202):
        sx=int(width*.22); sy=int(height*.17); radius=int(width*.23)
        d.ellipse((sx-radius,sy-radius,sx+radius,sy+radius),fill=(255,225,155,28),outline=(255,247,220,72),width=max(1,width//320))
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
