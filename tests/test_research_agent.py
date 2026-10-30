"""Independent checks for the Reality Loom agent utilities."""
import unittest

from tools.research_agent import rank_candidate, summarize_candidate


class ResearchAgentTests(unittest.TestCase):
    def test_license_metadata_improves_triage_score(self):
        base = {"stargazers_count": 100, "description": "simulation"}
        licensed = {**base, "license": {"spdx_id": "MIT"}}
        self.assertGreater(rank_candidate(licensed), rank_candidate(base))

    def test_archived_repository_is_penalized(self):
        active = {"stargazers_count": 1000, "license": {"spdx_id": "MIT"}}
        archived = {**active, "archived": True}
        self.assertLess(rank_candidate(archived), rank_candidate(active))

    def test_summary_marks_unknown_license(self):
        item = summarize_candidate({"full_name": "example/project"})
        self.assertEqual(item["license"], "Not identified")
        self.assertEqual(item["full_name"], "example/project")

    def test_summary_never_claims_verification(self):
        item = summarize_candidate({"full_name": "example/project"})
        self.assertIn("score", item)
        self.assertNotIn("verified", item)


if __name__ == "__main__":
    unittest.main()
