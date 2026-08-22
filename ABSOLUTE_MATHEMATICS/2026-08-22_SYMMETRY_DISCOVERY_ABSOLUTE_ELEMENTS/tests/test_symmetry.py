import unittest, sys
from pathlib import Path
ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from symmetry_discovery import *

class SymmetryTests(unittest.TestCase):
    def test_01_S4_count(self):
        G=all_perms(4)
        self.assertEqual(len(G),24)
        self.assertEqual(relation_type_count(4,G),4)
    def test_02_block_count(self):
        G=closure([(1,0,2,3),(0,1,3,2)],4)
        self.assertEqual(len(G),4)
        self.assertEqual(relation_type_count(4,G),8)
    def test_03_C4_count(self):
        G=closure([(1,2,3,0)],4)
        self.assertEqual(len(G),4)
        self.assertEqual(relation_type_count(4,G),5)
    def test_04_identity_count(self):
        self.assertEqual(relation_type_count(4,[identity(4)]),15)
    def test_05_burnside(self):
        groups=[all_perms(4),closure([(1,0,2,3),(0,1,3,2)],4),closure([(1,2,3,0)],4),[identity(4)]]
        for G in groups:
            self.assertEqual(relation_type_count(4,G),burnside_subset_orbit_count(4,G))
    def test_06_discover_symmetric(self):
        self.assertEqual(discover_exact_symmetry(task_symmetric,4,300,1)["size"],24)
    def test_07_discover_block(self):
        self.assertEqual(discover_exact_symmetry(task_block,4,300,1)["size"],4)
    def test_08_discover_role(self):
        self.assertEqual(discover_exact_symmetry(task_role,4,300,1)["size"],1)
    def test_09_intrinsic_rank(self):
        self.assertEqual(jacobian_rank_squarefree([.2,.4,.7,1.1]),4)
    def test_10_orbit_feature_fit(self):
        G=discover_exact_symmetry(task_block,4,300,1)["group"]
        self.assertLess(benchmark_task(task_block,G,4,2)["hidden_rmse"],1e-7)
    def test_11_minimal_feature_results_exist(self):
        import json
        m=json.loads((ROOT/"experiments/MINIMAL_INVARIANT_FEATURES.json").read_text())
        self.assertEqual(m["minimal_task_sufficient"]["S4_SYMMETRIC"]["minimal_task_sufficient"]["min_dim"],2)
        self.assertEqual(m["minimal_task_sufficient"]["BLOCK_S2xS2"]["minimal_task_sufficient"]["min_dim"],4)
        self.assertEqual(m["minimal_task_sufficient"]["IDENTITY_ROLE"]["minimal_task_sufficient"]["min_dim"],4)
        self.assertEqual(m["minimal_task_sufficient"]["CYCLE_GRAPH"]["minimal_task_sufficient"]["min_dim"],1)
    def test_12_multitask_monotonic_control(self):
        import json
        m=json.loads((ROOT/"experiments/MINIMAL_INVARIANT_FEATURES.json").read_text())
        self.assertEqual(m["multitask_S4"]["min_dim"],3)
    def test_13_intervention_refinement_counts(self):
        import json
        d=json.loads((ROOT/"experiments/INTERVENTION_SYMMETRY_REFINEMENT.json").read_text())
        self.assertEqual(d["OBSERVATIONAL_ONLY"]["relation_types"],4)
        self.assertEqual(d["ONE_ADDRESSABLE_ROLE"]["relation_types"],7)
        self.assertEqual(d["TWO_ADDRESSABLE_ROLES"]["relation_types"],11)
        self.assertEqual(d["ALL_ROLES_ADDRESSABLE"]["relation_types"],15)
    def test_14_group_refinement_sizes(self):
        import json
        d=json.loads((ROOT/"experiments/INTERVENTION_SYMMETRY_REFINEMENT.json").read_text())
        self.assertEqual([d[k]["group_size"] for k in ["OBSERVATIONAL_ONLY","ONE_ADDRESSABLE_ROLE","TWO_ADDRESSABLE_ROLES","ALL_ROLES_ADDRESSABLE"]],[24,6,2,1])

if __name__=="__main__":
    unittest.main()
