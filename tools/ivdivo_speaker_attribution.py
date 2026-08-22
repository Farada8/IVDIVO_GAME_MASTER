from __future__ import annotations

import argparse, json, math, re, zipfile
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

SPEECH_VERBS = (
    "said|asked|answered|replied|added|called|shouted|whispered|murmured|"
    "continued|snapped|told|warned|reported|confirmed|objected|responded"
)

@dataclass(frozen=True)
class Evidence:
    segment_id: str
    speaker: str
    method: str
    evidence: object


def wilson_lower_bound(successes: int, total: int, z: float = 1.96) -> float:
    if total <= 0:
        return 0.0
    p = successes / total
    denom = 1 + z*z/total
    centre = p + z*z/(2*total)
    spread = z * math.sqrt((p*(1-p) + z*z/(4*total))/total)
    return (centre - spread) / denom


def rule_auto_promotable(successes: int, total: int, min_n: int = 30,
                         min_precision: float = 0.98, min_wilson_lb: float = 0.90) -> bool:
    if total < min_n:
        return False
    precision = successes / total if total else 0.0
    return precision >= min_precision and wilson_lower_bound(successes, total) >= min_wilson_lb


def same_paragraph_prefix(text: str) -> str:
    return text.split("\n\n", 1)[0]


def same_paragraph_suffix(text: str) -> str:
    return text.rsplit("\n\n", 1)[-1]


def last_nonempty_paragraph(text: str) -> str:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return parts[-1] if parts else ""


def compile_aliases(alias_map: Dict[str, List[str]]) -> List[Tuple[re.Pattern, str, str]]:
    out=[]
    for speaker, aliases in alias_map.items():
        for alias in aliases:
            out.append((re.compile(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", re.I), speaker, alias))
    return sorted(out, key=lambda x: -len(x[2]))


def _nonoverlapping_longest_matches(text: str, alias_patterns):
    found=[]
    for pat, speaker, alias in alias_patterns:
        for m in pat.finditer(text):
            found.append((m.start(),m.end(),speaker,m.group(0)))
    kept=[]
    for item in found:
        a,b,sp,raw=item
        if any(c<=a and b<=d and (d-c)>(b-a) for c,d,_,_ in found):
            continue
        kept.append(item)
    return kept


PREPOSITIONAL_MODIFIERS = (
    "on|to|with|behind|beside|from|for|of|by|near|toward|towards|under|over|"
    "inside|outside|at|in|into|onto|through|across|around|between|among|against|off"
)


def _alias_is_modifier(text: str, start: int, end: int) -> bool:
    prefix=text[:start]
    suffix=text[end:]
    if re.search(r"\b(?:" + PREPOSITIONAL_MODIFIERS + r")\s+$", prefix, re.I):
        return True
    if re.match(r"[’']s\b", suffix, re.I):
        return True
    return False


def resolve_explicit_subject(text: str, alias_patterns) -> Optional[Tuple[str,str]]:
    found=[x for x in _nonoverlapping_longest_matches(text, alias_patterns)
           if not _alias_is_modifier(text, x[0], x[1])]
    speakers={s for _,_,s,_ in found}
    if len(speakers) != 1:
        return None
    a,b,s,raw=max(found, key=lambda t:t[0])
    return s,raw


def direct_pre_tag(narration_before: str, alias_patterns) -> Optional[Tuple[str,str]]:
    tail = same_paragraph_suffix(narration_before)
    m = re.search(r"([^.!?\n]{0,140}?)\b(" + SPEECH_VERBS + r")\s*[:,]?\s*$", tail, re.I)
    if not m:
        return None
    resolved = resolve_explicit_subject(m.group(1), alias_patterns)
    if not resolved:
        return None
    return resolved[0], m.group(0)


def standalone_pre_tag(narration_before: str, alias_patterns) -> Optional[Tuple[str,str]]:
    p = last_nonempty_paragraph(narration_before)
    if not p:
        return None
    m = re.fullmatch(r"\s*(.{1,120}?)\b(" + SPEECH_VERBS + r")\b(?:\s+(?:again|immediately|quietly|sharply|softly))?\s*[.!?:,]?\s*", p, re.I)
    if not m:
        return None
    resolved=resolve_explicit_subject(m.group(1), alias_patterns)
    if not resolved:
        return None
    return resolved[0], p


def direct_post_tag(narration_after: str, alias_patterns) -> Optional[Tuple[str,str]]:
    head = same_paragraph_prefix(narration_after)
    m = re.match(r"\s*([^.!?\n]{0,140}?)\b(" + SPEECH_VERBS + r")\b", head, re.I)
    if not m:
        return None
    resolved = resolve_explicit_subject(m.group(1), alias_patterns)
    if not resolved:
        return None
    return resolved[0], m.group(0)


def nearest_named_antecedent(text: str, alias_patterns, speaker_gender: Dict[str,str], pronoun: str) -> Optional[str]:
    gender = {"he":"M","she":"F"}.get(pronoun.lower())
    if not gender:
        return None
    p = last_nonempty_paragraph(text)
    candidates=[]
    for a,b,speaker,raw in _nonoverlapping_longest_matches(p,alias_patterns):
        if speaker_gender.get(speaker) == gender:
            candidates.append((a,speaker))
    if not candidates:
        return None
    if len({s for _,s in candidates}) != 1:
        return None
    return sorted(candidates)[-1][1]


def pronoun_post_tag(narration_before: str, narration_after: str,
                     alias_patterns, speaker_gender: Dict[str,str]) -> Optional[Tuple[str,str]]:
    head = same_paragraph_prefix(narration_after)
    m = re.match(r"\s*(he|she)\s+(" + SPEECH_VERBS + r")\b", head, re.I)
    if not m:
        return None
    speaker = nearest_named_antecedent(narration_before, alias_patterns, speaker_gender, m.group(1))
    if not speaker:
        return None
    return speaker, m.group(0)


def _sentence_chunks(paragraph: str) -> List[str]:
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", paragraph) if x.strip()]


def _alias_subject_at_sentence_start(sentence: str, alias_patterns) -> Optional[Tuple[str,str]]:
    found=_nonoverlapping_longest_matches(sentence, alias_patterns)
    edge=[x for x in found if x[0] <= 4 and not _alias_is_modifier(sentence, x[0], x[1])]
    speakers={x[2] for x in edge}
    if len(speakers) != 1:
        return None
    a,b,sp,raw=sorted(edge,key=lambda x:(x[0],-(x[1]-x[0])))[0]
    return sp,raw


def pronoun_subject_tracker_antecedent(narration_before: str, alias_patterns,
                                       speaker_gender: Dict[str,str], pronoun: str,
                                       max_paragraphs: int = 5) -> Optional[Tuple[str,list]]:
    target={"he":"M","she":"F"}.get(pronoun.lower())
    if not target:
        return None
    paras=[p.strip() for p in narration_before.split("\n\n") if p.strip()]
    subject=None; g=None; trace=[]
    for p in paras[-max_paragraphs:]:
        for sent in _sentence_chunks(p):
            explicit=_alias_subject_at_sentence_start(sent, alias_patterns)
            if explicit:
                subject=explicit[0]
                g=speaker_gender.get(subject)
                if g is None:
                    if re.search(r"\b(his|him|himself)\b", sent, re.I): g="M"
                    elif re.search(r"\b(her|hers|herself)\b", sent, re.I): g="F"
                trace.append({"kind":"EXPLICIT_SUBJECT","speaker":subject,"sentence":sent})
                continue
            m=re.match(r"(He|She)\b",sent,re.I)
            if m and subject:
                sg={"he":"M","she":"F"}[m.group(1).lower()]
                if g in (None,sg):
                    g=sg; trace.append({"kind":"PRONOUN_CONTINUITY","speaker":subject,"sentence":sent})
                else:
                    subject=None; g=None
                continue
            m=re.match(r"(His|Her)\b",sent,re.I)
            if m and subject:
                sg={"his":"M","her":"F"}[m.group(1).lower()]
                if g in (None,sg):
                    g=sg; trace.append({"kind":"POSSESSIVE_CONTINUITY","speaker":subject,"sentence":sent})
                else:
                    subject=None; g=None
                continue
    if subject and g in (None,target):
        return subject, trace[-4:]
    return None


def pronoun_subject_tracker_post_tag(narration_before: str, narration_after: str,
                                     alias_patterns, speaker_gender: Dict[str,str]) -> Optional[Tuple[str,dict]]:
    head=same_paragraph_prefix(narration_after)
    m=re.match(r"\s*(he|she)\s+("+SPEECH_VERBS+r")\b",head,re.I)
    if not m:
        return None
    if m.group(2).lower() == "added":
        rest=head[m.end():]
        if re.match(r"\s+(?:a|an|the|this|that|one|two|three|short|new)\b",rest,re.I):
            return None
    ant=pronoun_subject_tracker_antecedent(narration_before,alias_patterns,speaker_gender,m.group(1))
    if not ant:
        return None
    return ant[0], {"post_tag":m.group(0),"subject_trace":ant[1]}


def classify_and_attribute(segments: List[dict], alias_map: Dict[str,List[str]],
                           speaker_gender: Optional[Dict[str,str]] = None,
                           non_spoken_overrides: Optional[Iterable[str]] = None,
                           project_pronoun_subject_tracker_promoted: bool = False) -> List[Evidence]:
    speaker_gender = speaker_gender or {}
    non_spoken = set(non_spoken_overrides or [])
    alias_patterns = compile_aliases(alias_map)
    out=[]
    for i, seg in enumerate(segments):
        if seg.get("kind") != "DIALOGUE" and seg.get("type") != "DIALOGUE":
            continue
        sid=seg["segment_id"]
        if sid in non_spoken:
            continue
        prev = segments[i-1].get("exact_text","") if i>0 and (segments[i-1].get("kind") == "NARRATION" or segments[i-1].get("type") == "NARRATION") else ""
        nxt = segments[i+1].get("exact_text","") if i+1<len(segments) and (segments[i+1].get("kind") == "NARRATION" or segments[i+1].get("type") == "NARRATION") else ""
        candidates=[]
        pre=direct_pre_tag(prev, alias_patterns)
        if pre: candidates.append((pre[0],"PRE_DIRECT_TAG",pre[1]))
        post=direct_post_tag(nxt, alias_patterns)
        if post: candidates.append((post[0],"POST_DIRECT_TAG",post[1]))
        if project_pronoun_subject_tracker_promoted:
            pro2=pronoun_subject_tracker_post_tag(prev,nxt,alias_patterns,speaker_gender)
            if pro2: candidates.append((pro2[0],"AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER",pro2[1]))
        else:
            pro=pronoun_post_tag(prev,nxt,alias_patterns,speaker_gender)
            if pro: candidates.append((pro[0],"POST_PRONOUN_RESOLVED_REVIEW_CANDIDATE",pro[1]))
        speakers={c[0] for c in candidates}
        if len(speakers)==1:
            candidates.sort(key=lambda c:{"PRE_DIRECT_TAG":0,"POST_DIRECT_TAG":1,"AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER":2,"POST_PRONOUN_RESOLVED_REVIEW_CANDIDATE":3}.get(c[1],9))
            s,method,ev=candidates[0]
            out.append(Evidence(sid,s,method,ev))
    return out


def paragraph_keys(segments: List[dict]) -> Dict[str,Tuple[str,int]]:
    keys={}; chapter=None; pid=0
    for seg in segments:
        sid=seg["segment_id"]
        m=re.search(r"(?:^|_)(CH\d+)(?:_|$)", sid)
        ch=m.group(1) if m else "GLOBAL"
        if ch != chapter:
            chapter=ch; pid=0
        keys[sid]=(ch,pid)
        pid += seg.get("exact_text","").count("\n\n")
    return keys


def propagate_same_paragraph(segments: List[dict], seed: List[Evidence],
                             non_spoken_overrides: Optional[Iterable[str]] = None) -> List[Evidence]:
    non_spoken=set(non_spoken_overrides or [])
    keys=paragraph_keys(segments)
    by=defaultdict(list)
    for e in seed:
        by[keys[e.segment_id]].append(e)
    existing={e.segment_id for e in seed}
    out=[]
    for seg in segments:
        sid=seg["segment_id"]
        if sid in existing or sid in non_spoken or (seg.get("kind") != "DIALOGUE" and seg.get("type") != "DIALOGUE"):
            continue
        anchors=by.get(keys[sid],[])
        speakers={e.speaker for e in anchors}
        if len(speakers)==1:
            sp=next(iter(speakers))
            out.append(Evidence(sid,sp,"AUTO_SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION",{
                "paragraph":list(keys[sid]),
                "anchors":[{"segment_id":e.segment_id,"speaker":e.speaker,"method":e.method} for e in anchors]
            }))
    return out


def load_zip_segments(path: str) -> List[dict]:
    out=[]
    with zipfile.ZipFile(path) as z:
        for name in sorted([n for n in z.namelist() if re.fullmatch(r"CH\d{2}_SEGMENTS\.json", n)]):
            data=json.loads(z.read(name))
            out.extend(data if isinstance(data,list) else data["segments"])
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--segments-zip", required=True)
    p.add_argument("--config", required=True)
    p.add_argument("--overrides")
    p.add_argument("--out", required=True)
    p.add_argument("--project-same-paragraph-promoted", action="store_true")
    p.add_argument("--project-pronoun-subject-tracker-promoted", action="store_true")
    args=p.parse_args()
    cfg=json.load(open(args.config,encoding="utf-8"))
    overrides=[]
    if args.overrides:
        od=json.load(open(args.overrides,encoding="utf-8"))
        overrides=[x["segment_id"] for x in od.get("overrides",[])]
    segments=load_zip_segments(args.segments_zip)
    strong=classify_and_attribute(segments, cfg["aliases"], cfg.get("gender",{}), overrides, args.project_pronoun_subject_tracker_promoted)
    propagated=propagate_same_paragraph(segments,strong,overrides) if args.project_same_paragraph_promoted else []
    assignments=strong+propagated
    json.dump({
        "schema_version":"1.2",
        "policy":"FAIL_CLOSED_STRONG_LOCAL_ONLY",
        "strong_count":len(strong),
        "same_paragraph_project_promoted":bool(args.project_same_paragraph_promoted),
        "pronoun_subject_tracker_project_promoted":bool(args.project_pronoun_subject_tracker_promoted),
        "same_paragraph_added":len(propagated),
        "assignments":[e.__dict__ for e in assignments]
    }, open(args.out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
