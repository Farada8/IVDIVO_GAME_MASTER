import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from genesis_residual import *

class GenesisTests(unittest.TestCase):
    def test_peer_growth(self):
        r=peer_genesis([1,2,3,4],steps=4)
        self.assertEqual([x['created'] for x in r['history']],[10.0,20.0,40.0,80.0])
        self.assertEqual([x['next_sum'] for x in r['history']],[20.0,40.0,80.0,160.0])

    def test_symmetric_ladder(self):
        self.assertEqual(symmetric_ladder([1,2,3]),[6.0,11.0,6.0])

    def test_pair_order_symmetric(self):
        rows=residual_order_search(make_dataset('symmetric_pair',600,4,42),mode='symmetric',max_order=4)
        self.assertGreater(rows[0]['test_rmse'],0.5)
        self.assertLess(rows[1]['test_rmse'],1e-8)

    def test_triple_order_symmetric(self):
        rows=residual_order_search(make_dataset('symmetric_triple',600,4,42),mode='symmetric',max_order=4)
        self.assertGreater(rows[1]['test_rmse'],0.2)
        self.assertLess(rows[2]['test_rmse'],1e-8)

    def test_full_product_order4(self):
        rows=residual_order_search(make_dataset('full_product',600,4,42),mode='symmetric',max_order=4)
        self.assertGreater(rows[2]['test_rmse'],0.05)
        self.assertLess(rows[3]['test_rmse'],1e-8)

    def test_specific_pair_breaks_symmetric(self):
        data=make_dataset('specific_pair',600,4,42)
        sym=residual_order_search(data,mode='symmetric',max_order=4)
        sub=residual_order_search(data,mode='subset',max_order=4)
        self.assertGreater(sym[-1]['test_rmse'],0.2)
        self.assertLess(sub[1]['test_rmse'],1e-8)

    def test_mixed_requires_subset_order3(self):
        data=make_dataset('mixed',600,4,42)
        sym=residual_order_search(data,mode='symmetric',max_order=4)
        sub=residual_order_search(data,mode='subset',max_order=4)
        self.assertGreater(sym[-1]['test_rmse'],0.5)
        self.assertGreater(sub[1]['test_rmse'],0.05)
        self.assertLess(sub[2]['test_rmse'],1e-8)

    def test_genesis_status(self):
        self.assertEqual(genesis_status(new_element_in_old_closure=True),'REPRESENTATIONAL_GENESIS_ONLY')
        self.assertEqual(genesis_status(new_element_in_old_closure=True,expands_observable_structure=True),'STRUCTURAL_GENESIS_RELATIVE_TO_DECLARED_OBSERVABLES')

if __name__=='__main__':
    unittest.main()
