import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from scene_state_graph import validate_graph
from body_foley_compiler import compile_body_foley
from spatial_sound_compiler import compile_spatial_sound
from music_mix_compiler import compile_music_mix
from runtime_pipeline import run


def graph_base():
    return {
        "schema_version":"1.0","project_id":"TEST","scene_id":"S1","source_hash":"abc","delivery_mode":"DRAMATIZED",
        "scene_objective":"A tests B without forcing an answer.",
        "listener_point_of_audition":{"listener_position":"between_A_B","listener_orientation":"toward_pair","pov_mode":"OBJECTIVE_SCENE","mono_safe":True},
        "world_state":{"location_id":"POOL"},
        "beats":[{
            "beat_id":"B1","source_text_ids":["u1","u2"],"story_change":"B sees through A.",
            "listener":{"must_understand":["B noticed"],"may_feel":["pressure"],"must_wait_for":["admission"],"focus_owner":"DIALOGUE","suppress":[]},
            "world":{"location_id":"POOL","ambience":["distant_festival","water"]},
            "sound_policy":{"music":{"allowed":False,"reason":"performance must carry beat"}},
            "turns":[
                {"turn_id":"u1","speaker_id":"B","speaker_role":"CHARACTER","exact_text":"Ты опять посмотрел на часы.",
                 "reactivity":{"class":"IMMEDIATE","heard_event":"A checks reflected clock","response_impulse":"call it out","entry_trigger":"recognition"},
                 "knowledge":{},"attention":{},"want":"make A admit it","tactic":"TEST","subtext":"I see you",
                 "emotion":{"felt":{"primary":"concern","intensity":3},"shown":{"primary":"dry calm","intensity":2},"transition_cause":"noticed clock"},
                 "relationship":{},"status":{},"listening":{},"body":{"mouth_state":"CLEAR","speech_allowed":True},
                 "performance":{"reply_mode":"IMMEDIATE","tempo":"natural","projection":"small","phrase_ending":"clean","breath":"NONE","playable_behavior":["matter-of-fact"]},
                 "rhythm":{"pause_before":"SHORT","pause_after":"NONE","pause_function":"RECOGNITION"},
                 "space":{"distance":"NEAR","head_orientation":"toward_A","ear_specific":False,"mono_fallback":"center-preserved"},
                 "state_in":"observing","state_out":"pressing"},
                {"turn_id":"u2","speaker_id":"A","speaker_role":"CHARACTER","exact_text":"Нет.",
                 "reactivity":{"class":"IMMEDIATE","heard_event":"B calls out clock check","response_impulse":"deny too quickly","entry_trigger":"threat to control"},
                 "knowledge":{},"attention":{},"want":"recover control","tactic":"DENY","subtext":"do not expose me",
                 "emotion":{"felt":{"primary":"anxiety","intensity":5},"shown":{"primary":"confidence","intensity":4},"transition_cause":"B sees through him","leakage":["slightly too quick"]},
                 "relationship":{},"status":{},"listening":{},"body":{"mouth_state":"CLEAR","speech_allowed":True},
                 "performance":{"reply_mode":"IMMEDIATE","tempo":"quick","projection":"small","phrase_ending":"clipped","breath":"NONE","playable_behavior":["too-fast denial"]},
                 "rhythm":{"pause_before":"NONE","pause_after":"SHORT","pause_function":"STATUS"},
                 "space":{"distance":"NEAR","head_orientation":"toward_B","ear_specific":False,"mono_fallback":"center-preserved"},
                 "state_in":"controlled","state_out":"defensive"}
            ]
        }]
    }


class RuntimeTests(unittest.TestCase):
    def test_graph_and_compilers_pass(self):
        g=graph_base()
        self.assertEqual(validate_graph(g)["gate"],"PASS")
        self.assertEqual(compile_body_foley(g)["gate"],"PASS")
        self.assertEqual(compile_spatial_sound(g)["gate"],"PASS")
        self.assertEqual(compile_music_mix(g)["gate"],"PASS")

    def test_music_requires_value_change(self):
        g=graph_base(); g["beats"][0]["sound_policy"]["music"]={"allowed":True,"story_function":"AFTERMATH"}
        self.assertEqual(compile_music_mix(g)["gate"],"FAIL")

    def test_ear_specific_requires_mono(self):
        g=graph_base(); g["beats"][0]["turns"][0]["space"].update({"ear_specific":True,"mono_fallback":None})
        self.assertEqual(compile_spatial_sound(g)["gate"],"FAIL")

    def test_runtime_pipeline_emits_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(graph_base(),d)
            self.assertEqual(result["gate"],"PASS")
            self.assertTrue((Path(d)/"ACTOR_DIRECTOR_SCORE.json").exists())
            self.assertTrue((Path(d)/"BODY_FOLEY_PLAN.json").exists())
            self.assertTrue((Path(d)/"SPATIAL_SOUND_WORLD_PLAN.json").exists())
            self.assertTrue((Path(d)/"MUSIC_MIX_INTENT.json").exists())

if __name__=="__main__": unittest.main()
