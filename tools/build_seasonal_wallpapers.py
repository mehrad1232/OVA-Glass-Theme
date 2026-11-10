#!/usr/bin/env python3
"""Generate four original, high-resolution NOVA seasonal wallpapers."""
from pathlib import Path
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
THEME=ROOT/"NOVA Glass.theme"
WALLS=THEME/"Wallpapers"
MASTERS=THEME/"Artwork-Source"/"Wallpapers"
WALLS.mkdir(parents=True,exist_ok=True); MASTERS.mkdir(parents=True,exist_ok=True)

SCENES={
 "Spring":((24,48,73),(91,133,133),(226,166,180),(255,220,210)),
 "Summer":((15,49,78),(34,119,139),(238,183,105),(255,232,177)),
 "Autumn":((39,35,48),(116,69,55),(203,119,67),(245,190,117)),
 "Winter":((8,22,44),(37,75,111),(120,174,210),(225,244,255)),
}
def make(name,palette,seed,w,h):
 rng=random.Random(seed)
 yy,xx=np.mgrid[0:h,0:w]
 x=xx.astype(np.float32); y=yy.astype(np.float32)
 g=np.maximum(0,1-np.sqrt(((x-w*.23)/(w*.85))**2+((y-h*.16)/(h*.58))**2))
 t=np.clip(y/(h-1),0,1)
 arr=np.empty((h,w,3),dtype=np.float32)
 for c in range(3):
  arr[:,:,c]=palette[0][c]*(1-t)+palette[1][c]*t + (palette[2][c]-palette[0][c])*g*.48
 # Subtle film grain, generated deterministically.
 noise=np.random.default_rng(seed).normal(0,1.6,(h,w,1))
 arr=np.clip(arr+noise,0,255).astype(np.uint8)
 im=Image.fromarray(arr,"RGB").convert("RGBA")
 glow=Image.new("RGBA",(w,h),(0,0,0,0)); gd=ImageDraw.Draw(glow,"RGBA")
 gd.ellipse((-w*.24,-h*.17,w*.70,h*.39),fill=(*palette[3],48))
 glow=glow.filter(ImageFilter.GaussianBlur(max(12,w//24)))
 im=Image.alpha_composite(im,glow)
 d=ImageDraw.Draw(im,"RGBA")
 # Layered translucent glass light ribbons, no hard rectangular frame.
 d.ellipse((w*.42,h*.55,w*1.35,h*1.22),fill=(225,245,255,9))
 d.arc((-w*.35,h*.32,w*1.25,h*1.25),205,330,fill=(235,248,255,28),width=max(2,w//420))
 if name=="Spring":
  # Floating sakura petals with soft highlights.
  for _ in range(42):
   cx=rng.randrange(-20,w+20); cy=rng.randrange(-30,h+30); r=rng.randrange(max(5,w//150),max(8,w//75))
   col=(255,rng.randrange(165,220),rng.randrange(190,225),rng.randrange(85,175))
   d.ellipse((cx-r,cy-r*.55,cx+r,cy+r*.55),fill=col)
   d.line((cx-r*.65,cy,cx+r*.65,cy),fill=(255,245,245,75),width=max(1,w//700))
 elif name=="Summer":
  # Warm sun disc and long translucent rays.
  cx,cy=int(w*.76),int(h*.20); r=int(w*.17)
  d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(255,226,164,40))
  d.ellipse((cx-r*.72,cy-r*.72,cx+r*.72,cy+r*.72),fill=(255,239,195,38))
  for a in range(0,360,30):
   rad=math.radians(a); x1=cx+math.cos(rad)*r*1.25; y1=cy+math.sin(rad)*r*1.25
   x2=cx+math.cos(rad)*r*2.5; y2=cy+math.sin(rad)*r*2.5
   d.line((x1,y1,x2,y2),fill=(255,226,170,24),width=max(2,w//230))
  for _ in range(24):
   cx2=rng.randrange(w); cy2=rng.randrange(h)
   d.ellipse((cx2,cy2,cx2+w//180,cy2+w//180),fill=(255,239,190,rng.randrange(45,110)))
 elif name=="Autumn":
  # Falling leaves with a central vein and a soft amber edge.
  for _ in range(58):
   cx=rng.randrange(-20,w+20); cy=rng.randrange(-30,h+30); rw=rng.randrange(max(8,w//100),max(12,w//45)); rh=int(rw*.58)
   col=rng.choice([(221,135,65,170),(190,83,57,160),(239,177,83,165),(147,86,54,165)])
   leaf=Image.new("RGBA",(rw*3,rw*3),(0,0,0,0)); ld=ImageDraw.Draw(leaf,"RGBA")
   ld.ellipse((rw*.35,rw*.85,rw*2.65,rw*2.15),fill=col)
   ld.line((rw*.48,rw*1.5,rw*2.52,rw*1.5),fill=(255,224,169,135),width=max(1,rw//10))
   leaf=leaf.rotate(rng.randrange(360),resample=Image.Resampling.BICUBIC)
   im.alpha_composite(leaf,(cx-rw,cy-rw))
 elif name=="Winter":
  # Distinct snow crystals plus fine drifting snow.
  for _ in range(75):
   cx=rng.randrange(w); cy=rng.randrange(h); r=rng.randrange(max(3,w//260),max(5,w//130))
   d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(235,248,255,rng.randrange(55,160)))
   if r>5:
    for a in (0,60,120):
     rad=math.radians(a); dx=math.cos(rad)*r*1.8; dy=math.sin(rad)*r*1.8
     d.line((cx-dx,cy-dy,cx+dx,cy+dy),fill=(238,249,255,110),width=max(1,w//850))
 # Gentle vignette keeps app icons legible over the wallpaper.
 yy2,xx2=np.mgrid[0:h,0:w]
 nx=(xx2-w/2)/(w*.72); ny=(yy2-h/2)/(h*.72)
 vign=np.clip(1-.20*np.maximum(0,nx*nx+ny*ny-.25),.72,1)
 rgb=np.asarray(im.convert("RGB")).astype(np.float32)*vign[:,:,None]
 im=Image.fromarray(np.clip(rgb,0,255).astype(np.uint8),"RGB")
 return im

for idx,(name,palette) in enumerate(SCENES.items(),1):
 master=make(name,palette,800+idx,1170,2532)
 small=master.resize((640,1136),Image.Resampling.LANCZOS)
 master.save(MASTERS/f"NOVA-Glass-{name}-Season-Master.png",format="PNG",optimize=True)
 small.save(WALLS/f"NOVA-Glass-{name}-Season-iPhone5s.png",format="PNG",optimize=True)
 with Image.open(WALLS/f"NOVA-Glass-{name}-Season-iPhone5s.png") as im:
  assert im.size==(640,1136) and im.mode=="RGB"
print("PASS: four original seasonal wallpapers generated at 640x1136 and 1170x2532.")
