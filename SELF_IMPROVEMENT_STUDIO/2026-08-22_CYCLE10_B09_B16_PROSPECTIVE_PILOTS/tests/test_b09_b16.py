import importlib.util, pathlib, unittest

HERE = pathlib.Path(__file__).resolve()
spec = importlib.util.spec_from_file_location("b09b16", HERE.parents[1] / "tools/run_b09_b16.py")
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class ProspectivePilotTests(unittest.TestCase):
    def test_real_batch_passes(self):
        self.assertEqual(module.evaluate()["status"], "PASS")

    def test_all_three_have_meaningful_delta(self):
        self.assertTrue(all(x["meaningful_delta"] for x in module.evaluate()["results"]))

    def test_smallest_selected_all_three(self):
        self.assertTrue(all(x["voi_route"]["selected"] == "SMALLEST" for x in module.evaluate()["results"]))

    def test_no_external_evidence_fabricated(self):
        self.assertTrue(all(x["external_evidence_claimed"] is False for x in module.evaluate()["results"]))

    def test_real_three_do_not_trigger_two_no_delta_stop(self):
        self.assertFalse(module.evaluate()["b15_triggered_on_real_three"])

    def test_two_no_delta_trigger_stop(self):
        z = {"gate_changed": False, "selected_test_changed": False, "artifact_changed": False, "next_action_changed": False, "decision_changed": False}
        self.assertTrue(module.stop_after_two_no_delta([z, z]))

    def test_one_no_delta_does_not_stop(self):
        z = {"gate_changed": False, "selected_test_changed": False, "artifact_changed": False, "next_action_changed": False, "decision_changed": False}
        self.assertFalse(module.stop_after_two_no_delta([z]))

    def test_delta_resets_streak(self):
        z = {"gate_changed": False, "selected_test_changed": False, "artifact_changed": False, "next_action_changed": False, "decision_changed": False}
        y = dict(z, artifact_changed=True)
        self.assertFalse(module.stop_after_two_no_delta([z, y, z]))

    def test_b16_no_numbered_si(self):
        self.assertEqual(module.evaluate()["b16"]["numbered_si_candidate"], "NO")


if __name__ == "__main__":
    unittest.main(verbosity=2)
