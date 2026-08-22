#!/usr/bin/env python3
from pathlib import Path
import numpy as np, soundfile as sf, hashlib, json
from scipy.signal import butter, sosfilt
SR=48000; SEED=91720260823; OUT=Path('ROOM917_SUPPORT_SFX_CANARIES'); OUT.mkdir(exist_ok=True); rng=np.random.default_rng(SEED)
def bn(n,lo=None,hi=None):
 x=rng.standard_normal(n); ny=SR/2
 if lo and hi:sos=butter(4,[lo/ny,hi/ny],btype='band',output='sos')
 elif lo:sos=butter(4,lo/ny,btype='high',output='sos')
 elif hi:sos=butter(4,hi/ny,btype='low',output='sos')
 else:return x
 return sosfilt(sos,x)
def sp(x,pan=0,delay_ms=0):
 l=np.sqrt((1-pan)/2)*x; r=np.sqrt((1+pan)/2)*x
 if delay_ms:
  d=int(round(abs(delay_ms)*SR/1000))
  if delay_ms>0:r=np.concatenate([np.zeros(d),r])[:len(r)]
  else:l=np.concatenate([np.zeros(d),l])[:len(l)]
 return np.stack([l,r],1)
def norm(y,peak=.22):
 m=np.max(np.abs(y)); return y if m==0 else y*min(1.,peak/m)
def burst(dur,lo,hi,decay,amp=1,pan=0,delay_ms=0):
 n=int(dur*SR);t=np.arange(n)/SR;return sp(bn(n,lo,hi)*np.exp(-t/decay)*amp,pan,delay_ms)
def tonal(dur,freqs,decay,pan=0,peak=.2):
 n=int(dur*SR);t=np.arange(n)/SR;x=np.zeros(n);ph=rng.uniform(0,2*np.pi,len(freqs))
 for i,(f,a) in enumerate(freqs):x+=a*np.sin(2*np.pi*f*t+ph[i])*np.exp(-t/decay)
 return norm(sp(x,pan),peak)
def s01(v):
 n=int(2.2*SR);y=np.zeros((n,2));t=np.arange(n)/SR;fr=bn(n,70,1700);env=np.sin(np.pi*np.clip((t-.12)/1.8,0,1))**2;x=fr*env*.025+np.sin(2*np.pi*(150+25*v)*t)*env*.012;y+=sp(x,-.15+.15*v)
 for s in [.18,1.83]:
  p=burst(.24,120,2500,.045,.08,-.1+.1*v);a=int(s*SR);y[a:a+len(p)]+=p
 return norm(y,.16)
def s02(v):
 n=int(3.2*SR);y=np.zeros((n,2));times=[[.35,1.02,1.72,2.46],[.28,.95,1.62,2.30],[.40,1.08,1.78,2.52]][v]
 for j,s in enumerate(times):
  L=int(.28*SR);t=np.arange(L)/SR;x=bn(L,50,850)*np.exp(-t/.06)*.035+bn(L,650,3200)*np.exp(-t/.035)*.018;p=sp(x,-.06+.04*j);a=int(s*SR);y[a:a+L]+=p
 return norm(y,.13)
def s03(v):
 n=int(.9*SR);y=np.zeros((n,2));a=int(.24*SR)
 for j,dt in enumerate([0,.028,.061]):
  p=tonal(.18,[(2400+160*v+120*j,1.0),(4100+90*j,.32)],.055,.05*v-.05,.11);st=a+int(dt*SR);y[st:st+len(p)]+=p
 th=burst(.18,90,900,.035,.04,0);y[a:a+len(th)]+=th;return norm(y,.15)
def s04(v):
 n=int(2*SR);y=np.zeros((n,2))
 for j,s in enumerate([.22,.63]):
  p=burst(.2,180,4200,.025,.09,-.12+.24*j);a=int(s*SR);y[a:a+len(p)]+=p
 L=int(.8*SR);x=bn(L,120,1900)*np.sin(np.pi*np.arange(L)/L)**2*.022;a=int(.92*SR);y[a:a+L]+=sp(x,.05*v-.05);return norm(y,.15)
def s05(v):
 n=int(1.8*SR);t=np.arange(n)/SR;env=np.zeros(n);a=int(.25*SR);b=int(1.5*SR);env[a:b]=np.sin(np.linspace(0,np.pi,b-a))**1.5;x=bn(n,90,1500)*env*.022+np.sin(2*np.pi*(130+25*v)*t)*env*.013;y=sp(x,-.12+.12*v);p=burst(.16,180,2500,.025,.06,-.08);y[a:a+len(p)]+=p;return norm(y,.13)
def s06(v):
 n=int(1.6*SR);y=np.zeros((n,2));times=[[.22,.54,.88,1.20],[.20,.50,.84,1.18],[.26,.60,.94,1.28]][v]
 for j,s in enumerate(times):
  L=int(.12*SR);t=np.arange(L)/SR;x=bn(L,250,6000)*np.exp(-t/.014)*.06+np.sin(2*np.pi*(520+50*j)*t)*np.exp(-t/.03)*.025;p=sp(x,-.12+.08*j);a=int(s*SR);y[a:a+L]+=p
 return norm(y,.17)
def s09(v):
 n=int(3*SR);t=np.arange(n)/SR;x=bn(n,180,4200)*.010;x*=.35+.65*np.maximum(0,np.sin(2*np.pi*(.18+.04*v)*t+v))
 for s in [.9+.15*v,2.05-.08*v]:
  L=int(.22*SR);tt=np.arange(L)/SR;x[int(s*SR):int(s*SR)+L]+=bn(L,700,7000)*np.exp(-tt/.06)*.018
 return norm(sp(x,.12-.12*v,.1*v),.07)
def s12(v):
 n=int(1.8*SR);y=np.zeros((n,2))
 for j,s in enumerate([.28,.55,.84,1.13,1.40]):
  L=int(.10*SR);t=np.arange(L)/SR;x=bn(L,500,7000)*np.exp(-t/.012)*.045;pan=-.55+j*(1.1/4)+(v-1)*.03;p=sp(x,pan);a=int(s*SR);y[a:a+L]+=p
 return norm(y,.11)
def s15(v):
 n=int(1.2*SR);y=np.zeros((n,2));p=burst(.12,400,7000,.012,.06,-.03);a=int(.22*SR);y[a:a+len(p)]+=p;L=int(.55*SR);t=np.arange(L)/SR;mech=(np.sin(2*np.pi*(95+8*v)*t)*.010+bn(L,80,1600)*.004)*np.clip(t/.15,0,1)*np.exp(-t/.9);a=int(.35*SR);y[a:a+L]+=sp(mech,.02);return norm(y,.09)
def s16(v):
 n=int(.9*SR);y=np.zeros((n,2));a=int(.28*SR);scr=burst(.16,180,6000,.03,.045,.02);y[a:a+len(scr)]+=scr;L=int(.12*SR);t=np.arange(L)/SR;x=bn(L,350,8500)*np.exp(-t/.012)*.065+np.sin(2*np.pi*(480+40*v)*t)*np.exp(-t/.025)*.03;p=sp(x,.02);st=a+int(.09*SR);y[st:st+L]+=p;return norm(y,.13)
def s20(v):
 n=int(3.4*SR);y=np.zeros((n,2));times=[[.25,.62,.98,1.31],[.22,.57,.91,1.25],[.28,.64,1.00,1.34]][v]
 for j,s in enumerate(times):
  L=int(.22*SR);t=np.arange(L)/SR;x=bn(L,60,3000)*np.exp(-t/.045)*(.026+.004*j);p=sp(x,.28-.12*j);a=int(s*SR);y[a:a+L]+=p
 a=int(1.72*SR);L=int(1.2*SR);t=np.arange(L)/SR;env=np.sin(np.pi*np.clip(t/1.0,0,1))**1.4;x=bn(L,90,1800)*env*.018+np.sin(2*np.pi*(145+12*v)*t)*env*.009;y[a:a+L]+=sp(x,-.18);p=burst(.18,120,2600,.03,.065,-.18);st=int(2.83*SR);y[st:st+len(p)]+=p;return norm(y,.14)
def s21(v):
 n=int(3*SR);x=bn(n,450,4000);x=x/(np.std(x)+1e-12)*[.014,.018,.011][v];t=np.arange(n)/SR;x*=np.exp(-t/[7.,5.5,9.][v]);return norm(sp(x,[0,.02,-.02][v]),.045)
def m01(v):
 n=int(3.5*SR);t=np.arange(n)/SR;freqs=[[65.41,98.,130.81],[61.74,92.5,123.47],[73.42,110.,146.83]][v];x=np.zeros(n)
 for i,f in enumerate(freqs):
  x+=np.sin(2*np.pi*f*t+rng.uniform(0,2*np.pi))*np.exp(-t/(1.6-.15*i))*[.55,.35,.22][i];x+=.12*np.sin(2*np.pi*2*f*t+rng.uniform(0,2*np.pi))*np.exp(-t/.9)
 atk=int(.012*SR);x[:atk]*=np.linspace(0,1,atk);x+=bn(n,500,4500)*np.exp(-t/.05)*.01;return norm(sp(x,0,.15*v),.12)
makers={'S01_REVOLVING_DOOR_GROAN':s01,'S02_JULIAN_MEASURED_STEPS_STONE':s02,'S03_KEYRING_PLACED_ON_DESK':s03,'S04_FLIGHT_CASE_OPEN':s04,'S05_WOOD_SWITCHBOARD_CABINET_OPEN':s05,'S06_DRY_TOGGLE_CLICKS':s06,'S09_CONDUIT_WIND_SCRATCH':s09,'S12_PROBE_CONTACT_CLICKS':s12,'S15_FIELD_RECORDER_START':s15,'S16_HEADSET_PLUG_SEAT':s16,'S20_FAST_JULIAN_STEPS_AND_DOOR':s20,'S21_DEAD_LINE_HISS':s21,'M01_END_LOW_PIANO_CHORD':m01}
rec={'schema_version':'room917.support_sfx_synthetic_canary_receipt/1.0','date':'2026-08-22','seed':SEED,'status':'CANDIDATE_HOLD_NOT_PRODUCTION_BOUND','assets':[],'scope_boundary':{'S18_THREE_SHALLOW_BREATHS':'DEFER_TO_ELEVENLABS_CAST_PERFORMANCE_STREAM_NOT_SYNTHESIZED_HERE'}}
for aid,maker in makers.items():
 for v in range(3):
  y=maker(v);name=f'{aid}_CANDIDATE_SYNTH0{v+1}';p=OUT/f'{name}.wav';sf.write(p,y,SR,subtype='PCM_24');d=p.read_bytes();rec['assets'].append({'contract_asset_id':aid,'candidate_id':name,'filename':p.name,'sha256':hashlib.sha256(d).hexdigest(),'size_bytes':len(d),'duration_seconds':len(y)/SR,'sample_rate_hz':SR,'bit_depth':24,'channels':2,'origin':'PROCEDURAL_SYNTHETIC_REFERENCE_ONLY','audition_status':'HOLD','production_binding':False})
(OUT/'ROOM917_E01_SUPPORT_SFX_SYNTHETIC_CANARY_RECEIPT_v1.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
