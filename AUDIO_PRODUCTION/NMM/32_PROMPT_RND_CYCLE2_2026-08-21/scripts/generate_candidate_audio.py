#!/usr/bin/env python3
from pathlib import Path
import numpy as np, wave, hashlib, json
SR=48000

def save_wav(path,x):
    x=np.asarray(x,float); m=max(1e-9,np.max(np.abs(x))); x=np.clip(x/m*0.82,-1,1)
    pcm=(x*32767).astype(np.int16)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def whistle(duration,f0,vibrato=0.0,harmonic=0.35,noise=0.02):
    n=int(SR*duration); t=np.arange(n)/SR
    env=np.ones(n); a=max(1,int(.012*SR)); d=max(1,int(.05*SR)); env[:a]=np.linspace(0,1,a); env[-d:]=np.linspace(1,0,d)
    freq=f0*(1+vibrato*np.sin(2*np.pi*6*t)); phase=2*np.pi*np.cumsum(freq)/SR
    rng=np.random.default_rng(int(f0+duration*1000))
    return (np.sin(phase)+harmonic*np.sin(2*phase+.2)+.18*np.sin(3*phase+.6)+noise*rng.normal(size=n))*env

SHORT=[('W_EXTRA_SHORT_A',.16,2350,0,.30,.018),('W_EXTRA_SHORT_B',.20,2650,.006,.24,.015),('W_EXTRA_SHORT_C',.23,2150,.004,.38,.020),('W_EXTRA_SHORT_D',.18,2950,.002,.20,.012)]
LONG=[('W_OFFICIAL_LONG_A',.72,3150,.004,.32,.025),('W_OFFICIAL_LONG_B',.88,3450,.006,.28,.020),('W_OFFICIAL_LONG_C',.64,2850,.005,.38,.030),('W_OFFICIAL_LONG_D',1.02,3250,.007,.24,.022)]

def main(out='generated_audio'):
    root=Path(out); (root/'whistles').mkdir(parents=True,exist_ok=True); (root/'environment').mkdir(parents=True,exist_ok=True)
    rows=[]
    for name,dur,f0,vib,harm,noise in SHORT+LONG:
        p=root/'whistles'/f'{name}.wav'; save_wav(p,whistle(dur,f0,vib,harm,noise)); rows.append({'asset_id':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    print(json.dumps({'sample_rate_hz':SR,'generated':rows},indent=2))

if __name__=='__main__': main()
