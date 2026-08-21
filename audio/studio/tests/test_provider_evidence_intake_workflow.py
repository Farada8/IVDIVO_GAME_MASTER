import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github" / "workflows" / "elevenlabs-provider-evidence-intake.yml"


class ProviderEvidenceIntakeWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_trigger_is_exact_upstream_workflow_run(self):
        self.assertIn("workflow_run:", self.text)
        self.assertIn('workflows: ["ElevenLabs Provider Snapshot Evidence"]', self.text)
        self.assertIn("types: [completed]", self.text)

    def test_permissions_are_read_only(self):
        self.assertIn("contents: read", self.text)
        self.assertIn("actions: read", self.text)
        self.assertNotIn("contents: write", self.text)
        self.assertNotIn("actions: write", self.text)

    def test_cross_run_download_is_bound_to_triggering_run(self):
        self.assertIn("github.event.workflow_run.id", self.text)
        self.assertIn("github.event.workflow_run.run_attempt", self.text)
        self.assertIn("run-id: ${{ github.event.workflow_run.id }}", self.text)
        self.assertIn("github-token: ${{ github.token }}", self.text)

    def test_intake_workflow_never_receives_provider_secret_or_runs_synthesis(self):
        self.assertNotIn("ELEVENLABS_API_KEY", self.text)
        self.assertNotIn("elevenlabs_snapshot_acquirer.py", self.text)
        self.assertNotIn("controlled_provider_dispatch", self.text)
        self.assertNotIn("text_to_speech", self.text.lower())

    def test_checkout_uses_trusted_default_branch_and_drops_credentials(self):
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", self.text)
        self.assertIn("persist-credentials: false", self.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
