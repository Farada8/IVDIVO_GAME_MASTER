import unittest, itertools, math, random
from pathlib import Path
import sys

ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'engine'))
from genesis_dynamics import *

class Cycle2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n2=enumerate_commutative_semigroups(2)
        cls.n3=enumerate_commutative_semigroups(3)

    def test_01_n2_count(self): self.assertEqual(len(self.n2),6)
    def test_02_n2_iso(self): self.assertEqual(len(isomorphism_classes(self.n2)),3)
    def test_03_n3_count(self): self.assertEqual(len(self.n3),63)
    def test_04_n3_iso(self): self.assertEqual(len(isomorphism_classes(self.n3)),12)
    def test_05_n3_diagonals(self): self.assertEqual(len({diagonal_map(T) for T in self.n3}),19)
    def test_06_n3_ambiguous(self):
        g={}
        for T in self.n3:g[diagonal_map(T)]=g.get(diagonal_map(T),0)+1
        self.assertEqual(sum(v>1 for v in g.values()),10)
    def test_07_n3_max_same_diagonal(self):
        g={}
        for T in self.n3:g[diagonal_map(T)]=g.get(diagonal_map(T),0)+1
        self.assertEqual(max(g.values()),9)
    def test_08_same_diagonal_diff_operation(self):
        groups={}
        for T in self.n3:groups.setdefault(diagonal_map(T),[]).append(T)
        self.assertTrue(any(off_diagonal_disagreement(a,b) for gs in groups.values() for a,b in itertools.combinations(gs,2)))
    def test_09_order2(self): self.assertEqual(group_squaring_signature(2),{'tail':1,'period':1})
    def test_10_order3(self): self.assertEqual(group_squaring_signature(3),{'tail':0,'period':2})
    def test_11_order5(self): self.assertEqual(group_squaring_signature(5),{'tail':0,'period':4})
    def test_12_order12(self): self.assertEqual(group_squaring_signature(12),{'tail':2,'period':2})
    def test_13_comm_probe_count(self): self.assertEqual(mixed_probe_requirement(5)['commutative_unknown_off_diagonal_entries'],10)
    def test_14_general_probe_count(self): self.assertEqual(mixed_probe_requirement(5)['general_unknown_off_diagonal_entries'],20)
    def test_15_add_linearizer(self):
        rng=random.Random(1);pairs=[(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(200)]
        self.assertEqual(search_linearizer(candidate_binary_ops()['ADD'],pairs)[0]['transform'],'IDENTITY')
    def test_16_mul_linearizer(self):
        rng=random.Random(2);pairs=[(rng.uniform(.1,2),rng.uniform(.1,2)) for _ in range(200)]
        self.assertEqual(search_linearizer(candidate_binary_ops()['MUL'],pairs)[0]['transform'],'LOG_POSITIVE')
    def test_17_prob_or_linearizer(self):
        rng=random.Random(3);pairs=[(rng.uniform(.01,.95),rng.uniform(.01,.95)) for _ in range(200)]
        self.assertEqual(search_linearizer(candidate_binary_ops()['PROB_OR'],pairs)[0]['transform'],'NEG_LOG1M')
    def test_18_lambda_linearizer(self):
        rng=random.Random(4);pairs=[(rng.uniform(-.6,.6),rng.uniform(-.6,.6)) for _ in range(200)]
        self.assertEqual(search_linearizer(add_mul_op(.37),pairs,.37)[0]['transform'],'LOG1P_LAMBDA')
    def test_19_lambda_associative(self):
        rng=random.Random(5);triples=[(rng.uniform(-.5,.5),rng.uniform(-.5,.5),rng.uniform(-.5,.5)) for _ in range(200)]
        self.assertLess(associativity_defect(add_mul_op(.37),triples)['max'],1e-12)
    def test_20_diagonal_ambiguity_continuous(self):
        x=.7
        vals=[candidate_binary_ops()[k](x,x) for k in ['MAX','MIN','MEAN','RMS']]
        self.assertTrue(all(abs(v-x)<1e-12 for v in vals))

if __name__=='__main__': unittest.main()
