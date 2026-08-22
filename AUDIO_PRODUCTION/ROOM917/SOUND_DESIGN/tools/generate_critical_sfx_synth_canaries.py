from pathlib import Path
import numpy as np, soundfile as sf, hashlib, json
from scipy.signal import butter, sosfilt

SR=48000
OUT=Path('ROOM917_CRITICAL_SFX_CANARIES'); OUT.mkdir(exist_ok=True)
SEED=91720260822
rng=np.random.default_rng(SEED)

def candidate_seed(asset_id,v):
    token=f'{SEED}|{asset_id}|{v}'.encode()
    return int.from_bytes(hashlib.sha256(token).digest()[:8],'big')

def band_noise(n,lo=None,hi=None):
    x=rng.standard_normal(n); ny=SR/2
    if lo and hi: sos=butter(4,[lo/ny,hi/ny],btype='band',output='sos')
    elif lo: sos=butter(4,lo/ny,btype='high',output='sos')
    elif hi: sos=butter(4,hi/ny,btype='low',output='sos')
    else: return x
    return sosfilt(sos,x)

def stereo_pan(mono,pan=0.0,delay_ms=0.0):
    l=np.sqrt((1-pan)/2)*mono; r=np.sqrt((1+pan)/2)*mono
    if delay_ms:
        d=int(round(abs(delay_ms)*SR/1000))
        if delay_ms>0: r=np.concatenate([np.zeros(d),r])[:len(r)]
        else: l=np.concatenate([np.zeros(d),l])[:len(l)]
    return np.stack([l,r],1)

def norm(y,peak=0.22):
    m=np.max(np.abs(y)); return y if m==0 else y*min(1.0,peak/m)

def metal_ping(dur,freqs,decay,attack_ms=0.4,pan=0.0,delay_ms=0.0,peak=0.22):
    n=int(dur*SR); t=np.arange(n)/SR; x=np.zeros(n); phases=rng.uniform(0,2*np.pi,len(freqs))
    for i,(f,a) in enumerate(freqs): x += a*np.sin(2*np.pi*f*t+phases[i])*np.exp(-t/decay)
    atk=max(1,int(attack_ms*SR/1000)); x[:atk]*=np.linspace(0,1,atk); x += band_noise(n,1500,9000)*np.exp(-t/0.025)*0.02
    return norm(stereo_pan(x,pan,delay_ms),peak)

def click(dur=0.18,body=420,pan=0,peak=0.28):
    n=int(dur*SR); t=np.arange(n)/SR; x=band_noise(n,120,9000)*np.exp(-t/0.015)*0.12; x += np.sin(2*np.pi*body*t)*np.exp(-t/0.04)*0.22
    return norm(stereo_pan(x,pan,0),peak)

def old_double_ring(v):
    # Exactly one double-ring event = two countable electromechanical bell pulses.
    y=np.zeros((int(1.55*SR),2)); f1,f2,dec=[(835,1030,0.23),(780,990,0.27),(900,1110,0.20)][v]
    for s in [0.24,0.62]:
        p=metal_ping(0.48,[(f1,1.0),(f2,0.65),(2*f1,0.16)],dec,pan=(-0.05+0.05*v),peak=0.23); a=int(s*SR); y[a:a+len(p)]+=p
    return norm(y,0.26)

def lamp_ping(v,unmarked=False):
    base=[[(2280,1.0),(3420,0.38),(4910,0.20)],[(2390,1.0),(3560,0.36),(5050,0.18)],[(2180,1.0),(3320,0.42),(4760,0.18)]][v]
    pan=[-0.05,0.0,0.06][v]; delay=0.0
    if unmarked: pan=[0.32,0.42,0.26][v]; delay=[0.18,0.25,0.12][v]
    y=metal_ping(0.55,base,0.105+0.01*v,attack_ms=0.25,pan=pan,delay_ms=delay,peak=0.15)
    if unmarked:
        n=len(y); t=np.arange(n)/SR; mount=np.sin(2*np.pi*(760+40*v)*t)*np.exp(-t/0.045)*0.012; y += stereo_pan(mount,pan*0.8,delay*0.5)
    return norm(y,0.16)

def copper_hiss(v):
    n=int(4.0*SR); x=band_noise(n,350,4200); x=x/(np.std(x)+1e-12)*0.025
    for tm,amp in [[(1.0,0.018),(2.7,0.012)],[(0.65,0.012),(2.05,0.02),(3.2,0.01)],[(1.35,0.014),(2.35,0.014)]][v]:
        a=int(tm*SR); L=int(0.035*SR); env=np.exp(-np.arange(L)/(SR*0.006)); x[a:a+L]+=band_noise(L,900,7000)*env*amp
    return norm(stereo_pan(x,[0.0,-0.04,0.03][v],0),0.07)

def line_cut(v):
    # Two distinct events: recoverable first contact break, then final disconnect into absence.
    n=int(2.30*SR); x=band_noise(n,450,3900); x=x/(np.std(x)+1e-12)*0.018
    a1=[1.05,1.10,1.15][v]; a2=[1.42,1.46,1.52][v]
    i1=int(a1*SR); gap1=int([0.070,0.055,0.085][v]*SR)
    # Event 1: dry contact snap + short line loss + recovery.
    L1=int(0.075*SR); t1=np.arange(L1)/SR
    snap1=band_noise(L1,900,6500)*np.exp(-t1/0.009)*0.075 + np.sin(2*np.pi*(620+70*v)*t1)*np.exp(-t1/0.018)*0.030
    x[i1:i1+gap1]*=0.02; x[i1:i1+L1]+=snap1
    # Event 2: different lower mechanical snap, then hard absence.
    i2=int(a2*SR); L2=int(0.090*SR); t2=np.arange(L2)/SR
    snap2=band_noise(L2,120,2600)*np.exp(-t2/0.013)*0.085 + np.sin(2*np.pi*(250+35*v)*t2)*np.exp(-t2/0.022)*0.038
    x[i2:i2+L2]+=snap2; x[i2+L2:]=0
    return norm(stereo_pan(x,[0.0,0.02,-0.02][v],0),0.10)

def transformer(v):
    n=int(3.5*SR); t=np.arange(n)/SR; x=np.sin(2*np.pi*50*t)*0.018 + np.sin(2*np.pi*100*t)*[0.004,0.006,0.003][v]; rise=int([0.8,1.1,0.6][v]*SR); env=np.ones(n); env[:rise]=np.linspace(0,1,rise); x*=env; x += band_noise(n,30,180)*0.0015
    return norm(stereo_pan(x,0,0),0.035)

def relay_ripple(v):
    y=np.zeros((int(1.8*SR),2)); times=[[0.25,0.46,0.69,0.96],[0.22,0.43,0.70,1.03],[0.30,0.51,0.73,0.92,1.18]][v]
    for j,s in enumerate(times):
        p=click(0.13,body=380+35*j+20*v,pan=(-.08+.04*j),peak=0.18); a=int(s*SR); y[a:a+len(p)]+=p
    return norm(y,0.19)

def selector(v):
    y=np.zeros((int(0.7*SR),2)); p=click(0.18,body=[360,430,390][v],pan=[-.05,0,.04][v],peak=0.20); a=int(0.18*SR); y[a:a+len(p)]+=p; return y

makers={
 'S07_TRANSFORMER_WAKE':transformer,
 'S08_RELAY_RIPPLE':relay_ripple,
 'S10_SELECTOR_916':selector,
 'S11_GLASS_LAMP_916_PING':lambda v:lamp_ping(v,False),
 'S13_INTERNAL_DOUBLE_RING_OLD':old_double_ring,
 'S14_UNMARKED_GLASS_LAMP_PING':lambda v:lamp_ping(v,True),
 'S17_COPPER_HISS':copper_hiss,
 'S19_TWO_PART_LINE_CUT':line_cut,
}
receipt={'schema_version':'room917.critical_sfx_synthetic_canary_receipt/2.0','date':'2026-08-22','seed':SEED,'rng_policy':'PER_CANDIDATE_SHA256_DERIVED_SEED','status':'CANDIDATE_HOLD_NOT_PRODUCTION_BOUND','assets':[],'machine_design_fixes':['S13_EXACTLY_TWO_COUNTABLE_RING_PULSES','S19_STRONGER_FIRST_CONTACT_BREAK_AND_DISTINCT_FINAL_DISCONNECT'],'laws':['NO_STORY_CHANGE','NO_PROVIDER_SPEND','HUMAN_AUDITION_REQUIRED','IDENTITY_GATE_REQUIRED_BEFORE_BINDING']}
for aid,maker in makers.items():
    for v in range(3):
        rng=np.random.default_rng(candidate_seed(aid,v)); y=maker(v); name=f'{aid}_CANDIDATE_SYNTH0{v+1}'; p=OUT/f'{name}.wav'; sf.write(p,y,SR,subtype='PCM_24'); data=p.read_bytes(); receipt['assets'].append({'contract_asset_id':aid,'candidate_id':name,'filename':p.name,'sha256':hashlib.sha256(data).hexdigest(),'size_bytes':len(data),'duration_seconds':len(y)/SR,'sample_rate_hz':SR,'bit_depth':24,'channels':2,'origin':'PROCEDURAL_SYNTHETIC_REFERENCE_ONLY','audition_status':'HOLD','production_binding':False})
(OUT/'ROOM917_E01_CRITICAL_SFX_SYNTHETIC_CANARY_RECEIPT_v2.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
