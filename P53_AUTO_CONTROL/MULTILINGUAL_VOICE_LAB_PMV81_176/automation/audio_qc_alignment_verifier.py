#!/usr/bin/env python3
import wave,sys,struct,json,hashlib,math

def qc(path):
    b=open(path,'rb').read(); h=hashlib.sha256(b).hexdigest()
    with wave.open(path,'rb') as w:
        ch=w.getnchannels(); sw=w.getsampwidth(); sr=w.getframerate(); n=w.getnframes(); raw=w.readframes(n)
    if sw!=2: return {'file':path,'sha256':h,'verdict':'FAIL','reason':'ONLY_PCM16_FIXTURE_SUPPORTED'}
    vals=struct.unpack('<'+'h'*(len(raw)//2),raw); peak=max(abs(x) for x in vals) if vals else 0
    rms=math.sqrt(sum(x*x for x in vals)/len(vals)) if vals else 0; clip=sum(1 for x in vals if abs(x)>=32767); silence=sum(1 for x in vals if abs(x)<50)/max(1,len(vals))
    return {'file':path,'sha256':h,'channels':ch,'sample_rate':sr,'frames':n,'duration_sec':n/sr if sr else 0,'peak':peak,'rms':rms,'clip_samples':clip,'silence_fraction':round(silence,4),'verdict':'FAIL' if clip else 'PASS'}
if __name__=='__main__': print(json.dumps(qc(sys.argv[1]),indent=2))
