import unittest
from cortex.experiments.t4_response_diagnostics import diagnose


class ResponseDiagnosticsTest(unittest.TestCase):
    def test_shared_winner_is_not_selectivity(self):
        metrics = {t: {"responses": {"p_positive": 2.0, "p_negative": 1.0,
                                     "q_positive": 3.0, "q_negative": 9.0}}
                   for t in ("T4a", "T4b", "T4c", "T4d")}
        result = diagnose({"metrics": metrics,
                           "responses": {"baseline": {"integrated": {t: 0 for t in metrics}}}})
        self.assertTrue(result["all_subtypes_share_winner"])
        self.assertFalse(result["biological_direction_selectivity_validated"])
        self.assertTrue(all(abs(v) < 1e-12 for row in
                            result["subtype_residuals_after_common_mode"].values()
                            for v in row.values()))

    def test_rejects_overflow(self):
        metrics = {t: {"responses": {"x": float("inf")}} for t in
                   ("T4a", "T4b", "T4c", "T4d")}
        with self.assertRaises(ValueError):
            diagnose({"metrics": metrics})
