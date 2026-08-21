#!/usr/bin/env python3
import wave,struct,math,json,sys
from pathlib import Path
def qc(path):
    with wave.open(str(path),"rb") as w:
        ch,sw,sr,n=w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(); raw=w.readframes(n)
    if sw!=2: return {"verdict":"HOLD","reason":"only PCM16 fixture supported","sample_rate":sr}
    vals=struct.unpack("<"+"h"*(len(raw)//2),raw)
    peak=max(abs(x) for x in vals)/32768 if vals else 0
    rms=math.sqrt(sum(x*x for x in vals)/max(1,len(vals)))/32768
    clip=sum(1 for x in vals if abs(x)>=32760)/max(1,len(vals))
    return {"sample_rate":sr,"channels":ch,"duration_seconds":n/sr,"peak":peak,"rms":rms,"clip_fraction":clip,
      "verdict":"PASS" if sr==48000 and clip<0.0001 and peak<1 else "FAIL"}
if __name__=="__main__": Path(sys.argv[2]).write_text(json.dumps(qc(Path(sys.argv[1])),indent=2))
