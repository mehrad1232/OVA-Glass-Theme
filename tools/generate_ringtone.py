#!/usr/bin/env python3
"""Create an original NOVA Glass notification/ringtone tone for iOS."""
import math, struct, wave
from pathlib import Path

OUT=Path("dist")
OUT.mkdir(exist_ok=True)
wav=OUT/"NOVA-Glass-Ringtone.wav"
rate=44100
duration=24.0
notes=[(0.0,659.25,0.55),(0.42,783.99,0.55),(0.84,987.77,0.75),
       (2.0,783.99,0.48),(2.42,987.77,0.48),(2.84,1318.51,1.0),
       (5.2,987.77,0.5),(5.7,1174.66,0.5),(6.2,1567.98,1.1),
       (9.0,1318.51,0.45),(9.5,1174.66,0.45),(10.0,987.77,1.2),
       (14.0,783.99,0.5),(14.5,987.77,0.5),(15.0,1174.66,1.2),
       (19.0,987.77,0.55),(19.6,1318.51,0.55),(20.2,1567.98,1.6)]
with wave.open(str(wav),"wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(rate)
    frames=[]
    for i in range(int(rate*duration)):
        t=i/rate
        sample=0.0
        for start,freq,length in notes:
            local=t-start
            if 0 <= local < length:
                attack=min(1.0,local/0.025)
                release=min(1.0,(length-local)/0.12)
                env=attack*release*math.exp(-local*1.1)
                sample += 0.23*env*(math.sin(2*math.pi*freq*local)+0.22*math.sin(4*math.pi*freq*local))
        sample=max(-0.95,min(0.95,sample))
        frames.append(struct.pack("<h",int(sample*32767)))
    f.writeframes(b"".join(frames))
print(f"Generated {wav} ({duration:.0f}s). Convert to .m4r with ffmpeg in CI.")
