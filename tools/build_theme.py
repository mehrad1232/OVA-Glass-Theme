#!/usr/bin/env python3
"""Build NOVA Glass SnowBoard assets. Requires Pillow."""
from pathlib import Path
import math, random, plistlib
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]; THEME=ROOT/"NOVA Glass.theme"
ICONS=THEME/"IconBundles"; WALLS=THEME/"Wallpapers"
ICONS.mkdir(parents=True,exist_ok=True); WALLS.mkdir(parents=True,exist_ok=True)
APPS={
"com.apple.mobilesafari":("Safari","compass"),"com.apple.mobilemail":("Mail","mail"),"com.apple.mobilephone":("Phone","phone"),"com.apple.MobileSMS":("Messages","chat"),"com.apple.Preferences":("Settings","gear"),"com.apple.camera":("Camera","camera"),"com.apple.mobileslideshow":("Photos","flower"),"com.apple.Music":("Music","music"),"com.apple.mobilecal":("Calendar","calendar"),"com.apple.Maps":("Maps","pin"),"com.apple.weather":("Weather","sun"),"com.apple.AppStore":("App Store","appstore"),"com.apple.calculator":("Calculator","calculator"),"com.apple.VoiceMemos":("Voice Memos","wave"),"com.apple.compass":("Compass","compass"),"com.apple.stocks":("Stocks","chart"),"com.apple.reminders":("Reminders","check"),"com.apple.notes":("Notes","note"),"com.apple.facetime":("FaceTime","video"),"com.apple.podcasts":("Podcasts","podcast"),"com.apple.iBooks":("Books","book"),"com.apple.findmyiphone":("Find iPhone","radar"),"com.apple.mobiletimer":("Clock","clock"),"com.apple.Health":("Health","heart"),"com.apple.Home":("Home","home"),"com.apple.Passbook":("Wallet","wallet"),"com.apple.shortcuts":("Shortcuts","bolt"),"com.apple.tips":("Tips","bulb"),"com.apple.measure":("Measure","ruler"),"com.apple.MobileStore":("iTunes Store","star")}
S=360
def font(n):
 for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]:
  if Path(p).exists(): return ImageFont.truetype(p,n)
 return ImageFont.load_default()
def rounded_mask():
 m=Image.new("L",(S,S),0); ImageDraw.Draw(m).rounded_rectangle((0,0,S-1,S-1),76,fill=255); return m
def glyph(d,k):
 w=(245,252,255,245); s=(197,235,255,235); c=180
 if k=="mail": d.rounded_rectangle((88,112,272,246),18,outline=w,width=12); d.line((96,126,180,190,264,126),fill=w,width=12)
 elif k=="phone": d.arc((104,92,256,268),35,145,fill=w,width=25); d.rounded_rectangle((94,91,145,151),15,fill=w); d.rounded_rectangle((215,209,266,269),15,fill=w)
 elif k=="chat":
  d.rounded_rectangle((78,91,282,238),42,outline=w,width=12); d.polygon([(120,226),(103,272),(165,235)],fill=w)
  for x in (135,180,225): d.ellipse((x-7,155,x+7,169),fill=w)
 elif k=="gear":
  d.ellipse((119,119,241,241),outline=w,width=17); d.ellipse((157,157,203,203),outline=w,width=12)
  for a in range(0,360,45):
   r=math.radians(a); d.line((c+67*math.cos(r),c+67*math.sin(r),c+92*math.cos(r),c+92*math.sin(r)),fill=w,width=16)
 elif k=="camera": d.rounded_rectangle((78,118,282,250),25,outline=w,width=12); d.rounded_rectangle((120,95,175,128),10,fill=w); d.ellipse((139,145,221,227),outline=w,width=13); d.ellipse((166,172,194,200),fill=s)
 elif k in ("compass","radar"): d.ellipse((91,91,269,269),outline=w,width=12); d.ellipse((116,116,244,244),outline=s,width=5); d.polygon([(180,112),(211,198),(180,180),(149,198)],fill=w)
 elif k=="flower":
  for a in range(0,360,60):
   r=math.radians(a); x,y=c+42*math.cos(r),c+42*math.sin(r); d.ellipse((x-34,y-34,x+34,y+34),fill=w)
  d.ellipse((157,157,203,203),fill=(111,203,255,255))
 elif k=="music": d.line((205,92,205,226),fill=w,width=15); d.line((205,92,270,78),fill=w,width=15); d.line((270,78,270,205),fill=w,width=15); d.ellipse((125,205,190,270),fill=w); d.ellipse((222,185,287,250),fill=w)
 elif k=="calendar": d.rounded_rectangle((95,100,265,263),20,outline=w,width=12); d.line((95,148,265,148),fill=w,width=12); d.line((137,84,137,124),fill=w,width=12); d.line((223,84,223,124),fill=w,width=12); d.text((180,190),"7",font=font(65),fill=w,anchor="mm")
 elif k=="pin": d.ellipse((111,82,249,220),outline=w,width=13); d.polygon([(111,168),(180,285),(249,168)],fill=w); d.ellipse((157,128,203,174),fill=(75,153,205,255))
 elif k=="sun":
  d.ellipse((132,132,228,228),outline=w,width=13)
  for a in range(0,360,45):
   r=math.radians(a); d.line((180+65*math.cos(r),180+65*math.sin(r),180+91*math.cos(r),180+91*math.sin(r)),fill=w,width=11)
 elif k=="appstore": d.line((118,245,218,89),fill=w,width=17); d.line((242,245,142,89),fill=w,width=17); d.line((102,202,258,202),fill=w,width=17)
 elif k=="calculator":
  d.rounded_rectangle((111,78,249,282),18,outline=w,width=12); d.rounded_rectangle((130,98,230,143),8,fill=s)
  for y in (174,221,258):
   for x in (148,180,212): d.ellipse((x-8,y-8,x+8,y+8),fill=w)
 elif k=="wave": d.line([(x,180+38*math.sin((x-82)/13)) for x in range(82,280,4)],fill=w,width=12)
 elif k=="chart": d.line((95,260,95,105,265,105),fill=w,width=10); d.line((112,224,153,188,190,205,249,132),fill=w,width=13)
 elif k=="check":
  for y in (125,185,245): d.rounded_rectangle((95,y-18,130,y+17),8,outline=w,width=8); d.line((155,y,175,y+18,220,y-24),fill=w,width=9)
 elif k=="note":
  d.rounded_rectangle((105,78,255,282),15,outline=w,width=12)
  for y in (145,185,225): d.line((133,y,225,y),fill=w,width=8)
 elif k=="video": d.rounded_rectangle((78,112,235,248),22,outline=w,width=12); d.polygon([(235,150),(282,125),(282,235),(235,210)],fill=w)
 elif k=="podcast": d.ellipse((130,84,230,184),outline=w,width=12); d.arc((105,100,255,260),0,180,fill=w,width=12); d.line((180,220,180,270),fill=w,width=12)
 elif k=="book": d.rounded_rectangle((83,100,177,258),14,outline=w,width=12); d.rounded_rectangle((183,100,277,258),14,outline=w,width=12); d.line((180,105,180,258),fill=s,width=8)
 elif k=="clock": d.ellipse((92,92,268,268),outline=w,width=13); d.line((180,180,180,125),fill=w,width=12); d.line((180,180,228,205),fill=w,width=12)
 elif k=="heart": d.polygon([(180,265),(90,170),(90,130),(120,95),(155,95),(180,125),(205,95),(240,95),(270,130),(270,170)],fill=w)
 elif k=="home": d.polygon([(78,170),(180,85),(282,170),(260,170),(260,270),(100,270),(100,170)],fill=(245,252,255,225)); d.rectangle((160,202,200,270),fill=(65,125,160,255))
 elif k=="wallet": d.rounded_rectangle((85,112,275,250),22,outline=w,width=12); d.rounded_rectangle((185,150,280,210),12,fill=w); d.ellipse((207,172,222,187),fill=(70,145,190,255))
 elif k=="bolt": d.polygon([(194,70),(110,190),(172,190),(150,290),(252,150),(190,150)],fill=w)
 elif k=="bulb": d.ellipse((118,82,242,210),outline=w,width=13); d.line((145,212,215,212),fill=w,width=13); d.line((150,239,210,239),fill=w,width=13); d.line((160,263,200,263),fill=w,width=13)
 elif k=="ruler":
  d.rounded_rectangle((100,100,260,260),12,outline=w,width=12)
  for x in (135,170,205,240): d.line((x,105,x,145),fill=w,width=7)
 else: d.ellipse((110,110,250,250),outline=w,width=14); d.text((180,180),"N",font=font(80),fill=w,anchor="mm")
def make_icon(bundle,kind):
 im=Image.new("RGBA",(S,S),(0,0,0,0)); px=im.load()
 for y in range(S):
  t=y/(S-1)
  for x in range(S):
   g=max(0,1-math.sqrt(((x-95)/330)**2+((y-35)/260)**2)); px[x,y]=(int(22+28*g+9*t),int(62+65*g+18*t),int(91+82*g+20*t),255)
 m=rounded_mask(); im.putalpha(m)
 ov=Image.new("RGBA",(S,S),(0,0,0,0)); od=ImageDraw.Draw(ov); od.rounded_rectangle((7,7,S-8,S-8),70,outline=(226,248,255,190),width=5); od.rounded_rectangle((18,18,S-19,150),58,fill=(255,255,255,25))
 ov.putalpha(Image.composite(ov.getchannel("A"),Image.new("L",(S,S),0),m)); im=Image.alpha_composite(im,ov); glyph(ImageDraw.Draw(im),kind)
 im.resize((120,120),Image.Resampling.LANCZOS).save(ICONS/f"{bundle}.png",optimize=True)
for bundle,(_,kind) in APPS.items(): make_icon(bundle,kind)
W,H=640,1136
def make_wallpaper(filename, palette, seed, snow=False):
 rng=random.Random(seed); wall=Image.new("RGB",(W,H)); pix=wall.load()
 for y in range(H):
  t=y/(H-1)
  for x in range(W):
   g=max(0.0,1.0-math.sqrt(((x-115)/560)**2+((y-120)/650)**2))
   base=tuple(int(palette[i][0]+(palette[i][1]-palette[i][0])*g+(palette[i][2]-palette[i][0])*t) for i in range(3))
   # Independent subtle per-channel grain keeps the full-resolution PNG genuinely detailed.
   pix[x,y]=tuple(max(0,min(255,c+rng.randrange(-20,21))) for c in base)
 d=ImageDraw.Draw(wall,"RGBA")
 d.ellipse((-220,-260,430,390),fill=(142,218,255,28),outline=(225,248,255,70),width=3)
 d.ellipse((360,600,900,1140),outline=(170,225,255,35),width=3)
 d.rounded_rectangle((38,38,W-38,H-38),radius=48,outline=(225,245,255,60),width=2)
 if snow:
  for _ in range(180):
   x=rng.randrange(W); y=rng.randrange(H); r=rng.choice((1,1,2))
   d.ellipse((x-r,y-r,x+r,y+r),fill=(235,249,255,rng.randrange(90,220)))
 wall.save(WALLS/filename,optimize=False)
make_wallpaper("NOVA-Glass-Day-iPhone5s.png",((8,30,65),(28,105,150),(8,18,35)),12058,False)
make_wallpaper("NOVA-Glass-Night-iPhone5s.png",((3,9,27),(16,37,76),(1,4,15)),12059,True)
(THEME/"Wallpaper-Preview.html").write_text("""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NOVA Glass Preview</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#09192f;color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif}body{background:linear-gradient(145deg,rgba(12,45,75,.15),rgba(5,13,27,.35)),url('Wallpapers/NOVA-Glass-Day-iPhone5s.png') center/cover}.glass{position:absolute;left:8%;right:8%;top:20%;padding:24px;border:1px solid #ffffff55;border-radius:28px;background:#ffffff18;box-shadow:0 15px 45px #0005}#clock{font-size:58px;font-weight:200;letter-spacing:-3px}#date{opacity:.8;font-size:16px}.snow{position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(2px 2px at 20% 30%,#fff9 99%,transparent),radial-gradient(2px 2px at 70% 60%,#fff8 99%,transparent);background-size:170px 190px;animation:fall 8s linear infinite}@keyframes fall{to{background-position:0 190px,0 190px}}</style></head><body><div class="glass"><div id="clock"></div><div id="date"></div></div><div class="snow" id="snow"></div><script>function tick(){const d=new Date(),h=d.getHours();document.getElementById('clock').textContent=d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});document.getElementById('date').textContent=d.toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'});document.getElementById('snow').style.opacity=(h>=7&&h<14)?'0':'1'}tick();setInterval(tick,1000);</script></body></html>""",encoding="utf-8")
with (THEME/"Info.plist").open("rb") as f: info=plistlib.load(f)
info["ThemeVersion"]="2.0.0"; info["ThemeDescription"]="NOVA Glass icon pack for iOS 12, with 30 native PNG app icons and an iPhone 5s glass wallpaper."
with (THEME/"Info.plist").open("wb") as f: plistlib.dump(info,f,sort_keys=False)
with (THEME/"Info.plist").open("rb") as f: plistlib.load(f)
icons=list(ICONS.glob("*.png")); assert len(icons)==len(APPS)
for p in icons:
 with Image.open(p) as im: assert im.format=="PNG" and im.size==(120,120)
with Image.open(WALLS/"NOVA-Glass-iPhone5s.png") as im: assert im.format=="PNG" and im.size==(640,1136)
print(f"VALID: {len(icons)} PNG icons; 640x1136 wallpaper; plist valid.")
