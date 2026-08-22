import json, unittest
from pathlib import Path
from tools.si0015_project_slice_freshness_canary import ProjectSlice, classify_slice
ROOT=Path(__file__).resolve().parent

class SI0015Real20(unittest.TestCase):
    def test_all_source_grounded_slices(self):
        data=json.loads((ROOT/'REAL20_FIXTURES.json').read_text())
        self.assertGreaterEqual(len(data['fixtures']),20)
        for x in data['fixtures']:
            f=ProjectSlice(
                slice_kind=x['slice_kind'],
                embedded_frontier=x['embedded_frontier'],
                controlling_frontiers=tuple(x['controlling_frontiers']),
                pointer_resolved=x['pointer_resolved'],
                required_approval_event=x['required_approval_event'],
                observed_events=tuple(x['observed_events']),
            )
            self.assertEqual(classify_slice(f),x['expected'],x['id'])

if __name__=='__main__': unittest.main()
