from pathlib import Path
import numpy as np, soundfile as sf, hashlib, json, subprocess, shutil, zipfile
from scipy.signal import butter, sosfilt

ROOT = Path("ROOM917_E01_CORE_CLUE_SFX_CANARIES_v1")
ROOT.mkdir(parents=True, exist_ok=True)
SR = 48000
SEED = 91720260822

def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def normalize_peak(y, peak_db=-9.0):
    peak=np.max(np.abs(y))+1e-12; return y*((10**(peak_db/20))/peak)
def hp_lp(y, lo=None, hi=None, order=3):
    nyq=SR/2
    if lo and hi: sos=butter(order,[lo/nyq,hi/nyq],btype="band",output="sos")
    elif lo: sos=butter(order,lo/nyq,btype="high",output="sos")
    elif hi: sos=butter(order,hi/nyq,btype="low",output="sos")
    else: return y
    if y.ndim==1: return sosfilt(sos,y)
    return np.stack([sosfilt(sos,y[:,c]) for c in range(y.shape[1])],axis=1)
def stereo_pan(mono, pan=0.0):
    l=np.sqrt((1-pan)/2); r=np.sqrt((1+pan)/2); return np.stack([mono*l,mono*r],axis=1)
def transient_click(n,rng,decay=.006,brightness=.8):
    t=np.arange(n)/SR; x=rng.standard_normal(n)*np.exp(-t/max(decay,1e-4)); x=hp_lp(x,800 if brightness>.5 else 300,10000 if brightness>.5 else 6000); return x/(np.max(np.abs(x))+1e-12)
def modal_strike(duration,freqs,decays,amps,rng,detune=.002):
    n=int(duration*SR); t=np.arange(n)/SR; y=np.zeros(n)
    for f,d,a in zip(freqs,decays,amps):
        ff=f*(1+rng.uniform(-detune,detune)); y+=a*np.sin(2*np.pi*ff*t+rng.uniform(0,2*np.pi))*np.exp(-t/d)
    k=min(n,int(.018*SR)); y[:k]+=.08*transient_click(k,rng,.002,.7); return y
def place(dst,src,start):
    end=min(len(dst),start+len(src))
    if end>start: dst[start:end]+=src[:end-start]

def m01_double_ring(v):
    rng=np.random.default_rng(SEED+100+v); dur=[.92,1.02,1.12][v]; n=int(dur*SR); y=np.zeros((n,2)); spacing=[.285,.330,.365][v]
    sets=[([880,1180,1760,2340],[.18,.13,.09,.07],[1,.65,.38,.22]),([820,1110,1650,2210],[.20,.145,.10,.075],[1,.70,.35,.20]),([940,1260,1880,2520],[.16,.12,.085,.06],[1,.62,.40,.18])]
    freqs,decays,amps=sets[v]
    for i,st in enumerate([.06,.06+spacing]):
        strike=modal_strike(.38,freqs,decays,amps,rng)*(1 if i==0 else .92); pan=[-.12,.06,-.03][v]; place(y,stereo_pan(strike,pan),int(st*SR)); ck=transient_click(int(.025*SR),rng,.004,.55)*.18; place(y,stereo_pan(ck,pan*.7),max(0,int((st-.012)*SR)))
    body=hp_lp(rng.standard_normal(n),70,350); body=body/(np.max(np.abs(body))+1e-12)*.015*np.exp(-np.arange(n)/(SR*.42)); y+=stereo_pan(body,0); return normalize_peak(y,[-9.8,-9.2,-10.1][v])

def m02_lamp_ping(v):
    rng=np.random.default_rng(SEED+200+v); dur=[.24,.29,.34][v]; n=int(dur*SR); y=np.zeros((n,2)); click=transient_click(int(.035*SR),rng,.0025,.9)*.26; pan=[-.18,.12,.22][v]; place(y,stereo_pan(click,pan),int(.018*SR))
    sets=[([3150,4420,6120],[.055,.038,.025],[1,.48,.22]),([2870,4080,5580],[.065,.045,.028],[1,.52,.20]),([3380,4740,6480],[.050,.036,.024],[1,.44,.18])]; freqs,decays,amps=sets[v]; ping=hp_lp(modal_strike(dur-.025,freqs,decays,amps,rng,.001),1600,9000); place(y,stereo_pan(ping*.72,pan),int(.025*SR)); return normalize_peak(y,[-18,-17,-18.5][v])

def seamless_noise(rng,seconds,lo=280,hi=3600,warmth=0):
    n=int(seconds*SR); f=np.fft.rfftfreq(n,1/SR); spec=np.zeros(len(f),dtype=complex); mask=(f>=lo)&(f<=hi); phase=rng.uniform(0,2*np.pi,mask.sum()); mag=(np.maximum(f[mask],1)/1000)**(-.1-warmth)*rng.uniform(.6,1,mask.sum()); spec[mask]=mag*np.exp(1j*phase); y=np.fft.irfft(spec,n); return y/(np.max(np.abs(y))+1e-12)
def m03_copper_hiss(v):
    rng=np.random.default_rng(SEED+300+v); dur=20.; n=int(dur*SR); base=seamless_noise(rng,dur,[340,420,300][v],[3300,2900,3700][v],[.05,.12,0][v]); side=seamless_noise(rng,dur,900,4500,0)*.08; y=np.stack([base+side,base-side],axis=1); t=np.arange(n)/SR; tonal=np.zeros(n)
    for f,a in [([180,220,260][v],.035),([720,840,660][v],.012)]: tonal+=a*np.sin(2*np.pi*f*t+rng.uniform(0,2*np.pi))
    y+=stereo_pan(tonal,0)
    for st in rng.uniform(.5,dur-.5,[10,8,12][v]):
        d=int(rng.uniform(.006,.018)*SR); ck=transient_click(d,rng,.004,.7)*rng.uniform(.006,.015); place(y,stereo_pan(ck,rng.uniform(-.12,.12)),int(st*SR))
    am=.94+.06*np.sin(2*np.pi*[3,2,4][v]*np.arange(n)/n+rng.uniform(0,2*np.pi)); y*=am[:,None]; return normalize_peak(y,[-26,-27,-25.5][v])

def m05_two_part_cut(v):
    rng=np.random.default_rng(SEED+500+v); dur=[.48,.58,.66][v]; n=int(dur*SR); y=np.zeros((n,2)); st1=[.055,.060,.065][v]; ck1=transient_click(int(.055*SR),rng,.005,.55); mode1=modal_strike(.18,[420,730,1160],[.055,.045,.03],[1,.5,.25],rng); first=np.zeros(int(.20*SR)); first[:len(ck1)]+=ck1*.52; first[:len(mode1)]+=mode1*.34; place(y,stereo_pan(first,[-.05,.03,-.08][v]),int(st1*SR)); st2=st1+[.135,.175,.220][v]; ck2=transient_click(int(.05*SR),rng,.003,.85); mode2=modal_strike(.15,[980,1540,2460],[.038,.026,.018],[1,.45,.18],rng); second=np.zeros(int(.18*SR)); second[:len(ck2)]+=ck2*.42; second[:len(mode2)]+=mode2*.28; place(y,stereo_pan(second,[.02,-.04,.06][v]),int(st2*SR)); cutoff=min(n,int((st2+.16)*SR))
    if cutoff<n:
        fade=min(int(.015*SR),cutoff); y[cutoff-fade:cutoff]*=np.linspace(1,0,fade)[:,None]; y[cutoff:]=0
    return normalize_peak(y,[-12,-11.2,-12.8][v])

generators={"M01_917_DOUBLE_INTERNAL_RING":m01_double_ring,"M02_GLASS_LAMP_PING":m02_lamp_ping,"M03_COPPER_HISS_BED":m03_copper_hiss,"M05_TWO_PART_ANALOGUE_CUT":m05_two_part_cut}
specs={"M01_917_DOUBLE_INTERNAL_RING":([.7,1.3],False),"M02_GLASS_LAMP_PING":([.15,.45],False),"M03_COPPER_HISS_BED":([15,25],True),"M05_TWO_PART_ANALOGUE_CUT":([.35,.8],False)}
receipt={"schema_version":"room917.core_clue_sfx_canary_receipt/1.0","date":"2026-08-22","project":"ROOM917","episode":"E01","status":"CANDIDATE_HOLD_HUMAN_BLIND_AUDITION_REQUIRED","seed":SEED,"provider_calls":0,"paid_synthesis_calls":0,"story_changed":False,"assets":[]}
ffmpeg=shutil.which("ffmpeg")
for asset_id,gen in generators.items():
    adir=ROOT/asset_id; adir.mkdir(exist_ok=True)
    for vi,label in enumerate("ABC"):
        y=gen(vi); wav=adir/f"{asset_id}_VAR_{label}.wav"; sf.write(wav,y,SR,subtype="PCM_24"); mp3=adir/f"{asset_id}_VAR_{label}.mp3"
        if ffmpeg: subprocess.run([ffmpeg,"-y","-hide_banner","-loglevel","error","-i",str(wav),"-codec:a","libmp3lame","-b:a","192k",str(mp3)],check=True)
        peak=float(np.max(np.abs(y))); mid=np.sqrt(np.mean(((y[:,0]+y[:,1])/2)**2)); side=np.sqrt(np.mean(((y[:,0]-y[:,1])/2)**2)); dur=len(y)/SR; seam_db=None
        if specs[asset_id][1]:
            d=np.diff(y,axis=0); seam=y[0]-y[-1]; dr=np.sqrt(np.mean(d*d,axis=0)); seam_db=[float(x) for x in 20*np.log10((np.abs(seam)+1e-12)/(dr+1e-12))]
        receipt["assets"].append({"asset_id":asset_id,"variant":label,"wav_path":str(wav),"wav_sha256":sha256(wav),"wav_size_bytes":wav.stat().st_size,"mp3_path":str(mp3) if mp3.exists() else None,"mp3_sha256":sha256(mp3) if mp3.exists() else None,"sample_rate_hz":SR,"bit_depth":24,"channels":2,"duration_s":dur,"sample_peak_dbfs":20*np.log10(peak+1e-12),"mid_to_side_rms_db":20*np.log10((mid+1e-12)/(side+1e-12)),"loop_seam_vs_internal_diff_rms_db_lr":seam_db,"duration_spec_pass":specs[asset_id][0][0]<=dur<=specs[asset_id][0][1],"clip_free":peak<.999,"status":"HOLD_HUMAN_BLIND_AUDITION_REQUIRED","production_binding":False})
sil=np.zeros((int(1.2*SR),2)); reels=[]
for asset_id in generators:
    chunks=[]
    for label in "ABC":
        y,_=sf.read(ROOT/asset_id/f"{asset_id}_VAR_{label}.wav",always_2d=True); chunks+=[y,sil.copy()]
    reel=np.concatenate(chunks[:-1]); rwav=ROOT/f"{asset_id}_BLIND_REEL_A_B_C.wav"; sf.write(rwav,reel,SR,subtype="PCM_24"); rmp3=ROOT/f"{asset_id}_BLIND_REEL_A_B_C.mp3"
    if ffmpeg: subprocess.run([ffmpeg,"-y","-hide_banner","-loglevel","error","-i",str(rwav),"-codec:a","libmp3lame","-b:a","192k",str(rmp3)],check=True)
    reels.append({"asset_id":asset_id,"wav":rwav.name,"mp3":rmp3.name if rmp3.exists() else None,"wav_sha256":sha256(rwav),"mp3_sha256":sha256(rmp3) if rmp3.exists() else None})
receipt["blind_reels"]=reels; receipt["laws"]=["NO_CANARY_IS_PRODUCTION_MASTER","NO_VARIANT_MAY_BE_LOCKED_WITHOUT_HUMAN_BLIND_CATEGORY_TEST","M03_REQUIRES_LOOP_SEAM_AND_MONO_PHONE_CHECK","M04_LULLABY_NOT_GENERATED_BECAUSE_PITCH_AND_CATE_IDENTITY_GATE_REMAINS_OPEN","EN_RU_BYTE_SHARED_ONLY_AFTER_ACCEPTED_SHA256_BINDING"]
(ROOT/"ROOM917_E01_CORE_CLUE_SFX_CANARY_RECEIPT_v1.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"LISTENING_INDEX.txt").write_text("ROOM 917 E01 — CORE CLUE SFX CANARIES v1\nSTATUS: CANDIDATE / HOLD — not production masters\n\nBlind reels contain A → 1.2 s silence → B → 1.2 s silence → C.\nM01: old internal double ring. Reject modern ringtone/doorbell/horror.\nM02: tiny glass/metal lamp activation ping. Reject magic/UI/music.\nM03: old copper line hiss. Reject voices/whispers/drone/digital glitch.\nM05: two-stage analogue disconnect. Reject door lock/digital/tape-stop.\nM04 lullaby intentionally NOT generated.\n\nHuman decision per category: A / B / C / NONE.\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False,indent=2))
