#!/usr/bin/env python3
"""IVDIVO Microphone Choreography compiler v1.0

Planning compiler, not a full acoustic simulator.
Transforms semantic 3-D actor keyframes into renderer-neutral spatial automation targets.
No absolute timestamps are generated; semantic anchors are preserved.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
from typing import Any

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def wrap_deg(d: float) -> float:
    return (d + 180.0) % 360.0 - 180.0

def dist(a, b):
    return math.sqrt(sum((float(a[i])-float(b[i]))**2 for i in range(3)))

def bearing_deg(origin, target) -> float:
    dx = float(target[0]) - float(origin[0])
    dy = float(target[1]) - float(origin[1])
    return math.degrees(math.atan2(dx, dy))

def elevation_deg(origin, target) -> float:
    dx = float(target[0]) - float(origin[0])
    dy = float(target[1]) - float(origin[1])
    dz = float(target[2]) - float(origin[2])
    return math.degrees(math.atan2(dz, math.hypot(dx, dy)))

def cardioid_pattern_gain_db(angle_deg: float, pattern: str) -> float:
    """Planning estimate only; not a measured microphone profile."""
    a = math.radians(abs(wrap_deg(angle_deg)))
    p = pattern.upper()
    if p == "OMNI":
        amp = 1.0
    elif p == "FIGURE_8":
        amp = abs(math.cos(a))
    elif p == "CARDIOID":
        amp = 0.5 * (1.0 + math.cos(a))
    elif p == "SUPERCARDIOID":
        amp = abs(0.37 + 0.63 * math.cos(a))
    elif p == "HYPERCARDIOID":
        amp = abs(0.25 + 0.75 * math.cos(a))
    else:
        amp = 1.0
    return max(-30.0, 20.0 * math.log10(max(amp, 0.0316)))

def distance_gain_db(distance_m: float, reference_m: float=1.0) -> float:
    d=max(distance_m, 0.05)
    r=max(reference_m, 0.05)
    return clamp(-20.0*math.log10(d/r), -24.0, 12.0)

def head_offaxis_hf_loss_db(angle: float) -> float:
    return -9.0 * (abs(wrap_deg(angle))/180.0) ** 1.35

def room_send(distance_m: float) -> float:
    return clamp(0.15 + 0.17*math.log1p(max(distance_m,0.0)*2.0), 0.1, 0.8)

def pan_fallback(azimuth_deg: float) -> float:
    return clamp(azimuth_deg/90.0, -1.0, 1.0)

def intelligibility_risk(distance_m, mic_gain_db, hf_loss_db, occlusion):
    score=0
    if distance_m>4: score+=1
    if distance_m>8: score+=1
    if mic_gain_db<-12: score+=1
    if hf_loss_db<-5: score+=1
    if str(occlusion).upper() not in ("NONE","OPEN","CLEAR",""): score+=2
    return "HIGH" if score>=4 else ("MEDIUM" if score>=2 else "LOW")

def compile_scene(scene: dict[str, Any]) -> dict[str, Any]:
    listener=scene["listener"]
    lpos=listener["position"]
    lyaw=float(listener.get("orientation_deg",[0,0,0])[0])
    mics={m["mic_id"]:m for m in scene.get("microphones",[])}
    default_mic=next(iter(mics.values()), None)
    warnings=[]
    compiled=[]

    topology=scene.get("capture_topology")
    if any(e.get("ear_target") in ("LEFT","RIGHT") for e in scene.get("near_ear_events",[])):
        if topology not in ("BINAURAL_HEAD","VIRTUAL_BINAURAL","STEREO_PAIR","MULTI_MIC_ISO","VIRTUAL_STEREO"):
            warnings.append({"code":"FAIL_CAPTURE_TOPOLOGY_MISMATCH","detail":"ear-specific event requested with non-spatial topology"})

    for tr in scene.get("trajectories",[]):
        actor=tr["actor_id"]
        mic_id=tr.get("mic_id") or (default_mic and default_mic["mic_id"])
        mic=mics.get(mic_id) if mic_id else None
        if mic is None:
            warnings.append({"code":"FAIL_MIC_BLOCKING","actor_id":actor,"detail":"no microphone defined"})
            continue

        mpos=mic["position"]
        myaw=float(mic.get("orientation_deg",[0,0,0])[0])
        ref=float(mic.get("reference_distance_m",1.0))
        safe=float(mic.get("safe_min_distance_m",0.1))
        pattern=mic.get("polar_pattern","OMNI")
        last_pos=None

        for k in tr.get("keyframes",[]):
            pos=k["position"]
            dl=dist(lpos,pos)
            dm=dist(mpos,pos)
            az_listener=wrap_deg(bearing_deg(lpos,pos)-lyaw)
            elev=elevation_deg(lpos,pos)
            mic_inc=wrap_deg(bearing_deg(mpos,pos)-myaw)
            head_yaw=float(k.get("head_yaw_deg",k.get("body_yaw_deg",0.0)))
            voice_angle=wrap_deg(bearing_deg(pos,lpos)-head_yaw)

            dg=distance_gain_db(dm,ref)
            mg=cardioid_pattern_gain_db(mic_inc,pattern)
            hf=head_offaxis_hf_loss_db(voice_angle)
            rs=room_send(dl)
            occ=k.get("occlusion","NONE")
            risk=intelligibility_risk(dl,mg,hf,occ)

            if dm<safe:
                warnings.append({"code":"FAIL_MIC_BLOCKING","actor_id":actor,"anchor":k["anchor"],"detail":f"distance {dm:.3f}m < safe_min {safe:.3f}m"})
            if last_pos is not None and dist(last_pos,pos)>8.0 and tr.get("interpolation","LINEAR")!="CUT":
                warnings.append({"code":"FAIL_ACTOR_TELEPORT","actor_id":actor,"anchor":k["anchor"],"detail":"large uncut position jump"})
            last_pos=pos

            compiled.append({
                "actor_id":actor,
                "trajectory_id":tr["trajectory_id"],
                "anchor":k["anchor"],
                "position":pos,
                "body_yaw_deg":float(k.get("body_yaw_deg",0.0)),
                "head_yaw_deg":head_yaw,
                "distance_listener_m":round(dl,4),
                "azimuth_listener_deg":round(az_listener,3),
                "elevation_listener_deg":round(elev,3),
                "distance_mic_m":round(dm,4),
                "mic_incidence_deg":round(mic_inc,3),
                "voice_to_listener_angle_deg":round(voice_angle,3),
                "estimated_distance_gain_db":round(dg,3),
                "estimated_mic_pattern_gain_db":round(mg,3),
                "estimated_head_offaxis_hf_loss_db":round(hf,3),
                "recommended_room_send":round(rs,4),
                "recommended_pan_fallback":round(pan_fallback(az_listener),4),
                "ear_target":k.get("ear_target","NONE"),
                "occlusion":occ,
                "intelligibility_risk":risk,
                "foley_links":k.get("foley_links",[]),
                "speech_unit_links":k.get("speech_unit_links",[]),
                "planning_only":True
            })

    return {
        "schema_version":"1.0",
        "scene_id":scene["scene_id"],
        "mode":scene["mode"],
        "capture_topology":topology,
        "acoustic_passport_id":scene["acoustic_passport_id"],
        "compiled_spatial_keyframes":compiled,
        "warnings":warnings,
        "note":"Automation values are planning targets; final DSP must be calibrated against acoustic passport/render topology."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("scene_json")
    p.add_argument("--output",required=True)
    a=p.parse_args()
    scene=json.loads(Path(a.scene_json).read_text(encoding="utf-8"))
    result=compile_scene(scene)
    Path(a.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"PASS compiled {len(result['compiled_spatial_keyframes'])} keyframes; warnings={len(result['warnings'])}; output={a.output}")

if __name__=="__main__":
    main()