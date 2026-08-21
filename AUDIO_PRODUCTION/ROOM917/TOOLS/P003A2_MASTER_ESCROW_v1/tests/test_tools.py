from pathlib import Path
import json, subprocess, sys, tempfile, wave
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / "p003a2_interval_analyzer.py"
ES = ROOT / "master_escrow.py"


def pack24(values):
    values = np.asarray(values, dtype=np.int32).reshape(-1)
    values = np.where(values < 0, values + (1 << 24), values).astype(np.uint32)
    b = np.empty((values.size, 3), dtype=np.uint8)
    b[:,0] = values & 0xFF
    b[:,1] = (values >> 8) & 0xFF
    b[:,2] = (values >> 16) & 0xFF
    return b.tobytes()


def make_test_wav(path: Path):
    sr=48000; ch=2
    parts=[]
    for dur, db in [(0.2,-20),(0.3,None),(0.2,-60),(0.3,-20)]:
        n=int(sr*dur)
        if db is None:
            x=np.zeros(n,dtype=np.float64)
        else:
            amp=10**(db/20)
            t=np.arange(n)/sr
            x=amp*np.sin(2*np.pi*1000*t)
        pcm=np.clip(np.round(x*(2**23-1)), -(2**23), 2**23-1).astype(np.int32)
        stereo=np.column_stack([pcm,pcm]).reshape(-1)
        parts.append(pack24(stereo))
    with wave.open(str(path),'wb') as w:
        w.setnchannels(ch); w.setsampwidth(3); w.setframerate(sr)
        for p in parts: w.writeframes(p)


def test_analyzer_and_escrow():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); wav=td/'test.wav'; make_test_wav(wav)
        outj=td/'out.json'; outc=td/'out.csv'
        subprocess.run([sys.executable,str(AN),str(wav),'--thresholds','-85','-50','-45','--output-json',str(outj),'--output-csv',str(outc)],check=True)
        data=json.loads(outj.read_text())
        assert data['summary']['-85.0']['below_threshold_seconds'] == 0.3
        assert data['summary']['-50.0']['below_threshold_seconds'] == 0.5
        assert data['summary']['-45.0']['below_threshold_seconds'] == 0.5
        assert all(iv['classification']=='UNKNOWN_REQUIRES_LISTEN_OR_LIVE_TIMELINE' for iv in data['intervals'])

        esc=td/'escrow'; manifest=td/'manifest.json'
        subprocess.run([sys.executable,str(ES),str(wav),'--dest-dir',str(esc),'--asset-id','TEST_ASSET','--manifest',str(manifest)],check=True)
        m=json.loads(manifest.read_text())
        assert m['byte_parity'] is True
        assert (esc/'test.wav').read_bytes()==wav.read_bytes()

if __name__=='__main__':
    test_analyzer_and_escrow(); print('PASS')
