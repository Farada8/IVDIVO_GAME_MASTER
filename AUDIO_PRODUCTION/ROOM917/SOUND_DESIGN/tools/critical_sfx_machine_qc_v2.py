#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, find_peaks

SR=48000
ASSETS=["S07_TRANSFORMER_WAKE","S08_RELAY_RIPPLE","S10_SELECTOR_916","S11_GLASS_LAMP_916_PING",
"S13_INTERNAL_DOUBLE_RING_OLD","S14_UNMARKED_GLASS_LAMP_PING","S17_COPPER_HISS","S19_TWO_PART_LINE_CUT"]

def load(wav_dir,aid,c):
    x,sr=sf.read(Path(wav_dir)/f"{aid}_CANDIDATE_SYNTH0{c}.wav",always_2d=True)
    if sr!=SR: raise ValueError(f"BAD_SR:{aid}:{c}:{sr}")
    return x.mean(axis=1)

def bp(y,lo,hi):
    sos=butter(4,[lo/(SR/2),hi/(SR/2)],btype="bandpass",output="sos")
    return sosfilt(sos,y)

def rms(y): return float(np.sqrt(np.mean(y*y))+1e-20)
def phone_ret(y): return float(20*np.log10(rms(bp(y,180,7000))/rms(y)))

def spectral(y):
    mag=np.abs(np.fft.rfft(y*np.hanning(len(y)))); f=np.fft.rfftfreq(len(y),1/SR)
    tot=mag.sum()+1e-20
    centroid=float((f*mag).sum()/tot)
    cs=np.cumsum(mag)/tot
    roll=float(f[min(np.searchsorted(cs,.85),len(f)-1)])
    power=mag**2+1e-20
    flat=float(np.exp(np.mean(np.log(power)))/np.mean(power))
    return centroid,roll,flat

def causal_onsets(y,smooth_ms=8,flux_ms=25,min_gap_ms=120,threshold_frac=0.30):
    env=np.abs(y); win=max(1,int(smooth_ms*SR/1000))
    sm=np.convolve(env,np.ones(win)/win,mode="same")
    log=np.log1p(sm/(sm.max()+1e-12)*20.0)
    lag=max(1,int(flux_ms*SR/1000)); flux=np.zeros_like(log)
    flux[lag:]=np.maximum(0.0,log[lag:]-log[:-lag])
    w2=max(1,int(8*SR/1000)); fs=np.convolve(flux,np.ones(w2)/w2,mode="same")
    if fs.max()==0:return []
    peaks,_=find_peaks(fs,height=fs.max()*threshold_frac,
                       distance=int(min_gap_ms*SR/1000),
                       prominence=fs.max()*0.05)
    return [float(p/SR) for p in peaks]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--wav-dir",required=True); ap.add_argument("--out",required=True)
    a=ap.parse_args()
    records=[]; checks=[]
    for aid in ASSETS:
        for c in (1,2,3):
            y=load(a.wav_dir,aid,c); cent,roll,flat=spectral(y); onsets=causal_onsets(y)
            rec={"asset_id":aid,"candidate":c,"phone_retention_db":round(phone_ret(y),2),
                 "centroid_hz":round(cent,1),"rolloff85_hz":round(roll,1),
                 "spectral_flatness":round(flat,7),"causal_onsets_s":[round(t,4) for t in onsets],
                 "causal_onset_count":len(onsets)}
            records.append(rec); status="PASS"; detail={}
            if aid=="S07_TRANSFORMER_WAKE":
                f=np.fft.rfftfreq(len(y),1/SR); sp=np.abs(np.fft.rfft(y*np.hanning(len(y))))
                idx=np.where((f>=45)&(f<=55))[0]; peak=float(f[idx[np.argmax(sp[idx])]])
                detail={"fundamental_hz":round(peak,3)}; status="PASS" if abs(peak-50)<=.2 else "FAIL"
            elif aid=="S08_RELAY_RIPPLE":
                detail={"events":len(onsets)}; status="PASS" if 3<=len(onsets)<=6 else "FAIL"
            elif aid=="S10_SELECTOR_916":
                detail={"events":len(onsets)}; status="PASS" if len(onsets)==1 else "FAIL"
            elif aid=="S13_INTERNAL_DOUBLE_RING_OLD":
                detail={"events":len(onsets),"onsets_s":rec["causal_onsets_s"]}
                status="PASS" if len(onsets)==2 and .25<=onsets[1]-onsets[0]<=.55 else "FAIL"
            elif aid=="S17_COPPER_HISS":
                f=np.fft.rfftfreq(len(y),1/SR); sp=np.abs(np.fft.rfft(y*np.hanning(len(y))))**2
                p50=sp[(f>=49)&(f<=51)].sum(); band=sp[(f>=350)&(f<=4200)].sum()
                ratio=10*np.log10((p50+1e-20)/(band+1e-20))
                detail={"50hz_vs_band_db":round(float(ratio),2)}
                status="PASS" if ratio<-45 and rec["phone_retention_db"]>-8 else "FAIL"
            elif aid=="S19_TWO_PART_LINE_CUT":
                tail=y[int(1.75*SR):]; detail={"events":len(onsets),"onsets_s":rec["causal_onsets_s"],
                "post_cut_peak":float(np.max(np.abs(tail)))}
                status="PASS" if len(onsets)==2 and .18<=onsets[1]-onsets[0]<=.45 and np.max(np.abs(tail))==0 else "FAIL"
            elif aid in ("S11_GLASS_LAMP_916_PING","S14_UNMARKED_GLASS_LAMP_PING"):
                status="PASS" if rec["phone_retention_db"]>-12 else "FAIL"
            checks.append({"gate":"cue_specific","asset_id":aid,"candidate":c,**detail,"status":status})

    by={(r["asset_id"],r["candidate"]):r for r in records}
    for x in (1,2,3):
        for y in (1,2,3):
            a1=by[("S11_GLASS_LAMP_916_PING",x)]; a2=by[("S14_UNMARKED_GLASS_LAMP_PING",y)]
            d=abs(a1["centroid_hz"]-a2["centroid_hz"])
            checks.append({"gate":"S11_vs_S14","a":x,"b":y,"delta_hz":round(d,1),"status":"PASS" if d>=180 else "FAIL"})
            r=by[("S13_INTERNAL_DOUBLE_RING_OLD",x)]; c=by[("S19_TWO_PART_LINE_CUT",y)]
            cd=abs(r["centroid_hz"]-c["centroid_hz"]); rd=abs(r["rolloff85_hz"]-c["rolloff85_hz"])
            fr=c["spectral_flatness"]/(r["spectral_flatness"]+1e-20)
            checks.append({"gate":"S13_vs_S19","a":x,"b":y,"status":"PASS" if cd>=500 and rd>=800 and fr>=1.5 else "FAIL"})
            s=by[("S10_SELECTOR_916",x)]; rr=by[("S08_RELAY_RIPPLE",y)]
            checks.append({"gate":"S10_vs_S08","a":x,"b":y,"status":"PASS" if s["causal_onset_count"]==1 and rr["causal_onset_count"]>=3 else "FAIL"})
    failures=[x for x in checks if x["status"]!="PASS"]
    report={"schema_version":"room917.critical_sfx_machine_qc/2.2",
            "measurement":"LOG_ENVELOPE_POSITIVE_FLUX_CAUSAL_ONSET_DETECTOR",
            "candidate_count":24,"checks_count":len(checks),"failures_count":len(failures),
            "status":"PASS" if not failures else "FAIL","records":records,"checks":checks,"failures":failures}
    Path(a.out).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"checks":len(checks),"failures":len(failures)},indent=2))
    return 0 if not failures else 1
if __name__=="__main__": raise SystemExit(main())
