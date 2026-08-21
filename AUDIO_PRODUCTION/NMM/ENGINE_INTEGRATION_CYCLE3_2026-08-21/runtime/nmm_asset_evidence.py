from __future__ import annotations
from pathlib import Path
import hashlib,wave,math
import numpy as np
SR=48000

def read_wav(path):
 with wave.open(str(path),'rb') as w:
  ch=w.getnchannels(); sw=w.getsampwidth(); sr=w.getframerate(); n=w.getnframes(); data=w.readframes(n)
 if sr!=48000 or ch not in (1,2) or sw not in (2,3,4) or n<=0: raise ValueError('FAIL_CANONICAL_INGEST')
 if sw==2: x=np.frombuffer(data,dtype='<i2').astype(np.float64)/32768
 else: raise ValueError('ONLY_PCM16_LOCAL_LAB')
 if ch==2: x=x.reshape(-1,2).mean(1)
 return x,sr,ch,sw,data

def metrics(path):
 x,sr,ch,sw,data=read_wav(path); peak=float(np.max(np.abs(x))); rms=float(np.sqrt(np.mean(x*x)))
 crest=20*math.log10(max(peak,1e-12)/max(rms,1e-12)); spec=np.abs(np.fft.rfft(x*np.hanning(len(x))))+1e-12; f=np.fft.rfftfreq(len(x),1/sr); centroid=float((f*spec).sum()/spec.sum())
 return {'path':str(path),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'sample_rate_hz':sr,'channels':ch,'sample_width_bytes':sw,'duration_s':len(x)/sr,'peak_dbfs':20*math.log10(max(peak,1e-12)),'rms_dbfs':20*math.log10(max(rms,1e-12)),'crest_db':crest,'spectral_centroid_hz':centroid,'gate':'PASS'}
def normalize_rms(in_path,out_path,target_dbfs=-20.0):
 x,sr,ch,sw,data=read_wav(in_path); rms=np.sqrt(np.mean(x*x)); target=10**(target_dbfs/20); gain=target/max(rms,1e-12); y=np.clip(x*gain,-0.98,0.98); pcm=(y*32767).astype('<i2')
 Path(out_path).parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(out_path),'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
 return {'gain_db':20*math.log10(gain),'pre':metrics(in_path),'post':metrics(out_path),'identity_transform':'GAIN_ONLY_NO_EQ'}
