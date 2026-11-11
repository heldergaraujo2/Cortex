import unittest
from cortex.experiments.t4_validation_gates import assess


class T4ValidationGatesTest(unittest.TestCase):
    def test_identical_preference_is_not_biological_validation(self):
        conditions = {"p_positive": 1.0, "p_negative": 2.0,
                      "q_positive": 1.0, "q_negative": 4.0}
        data = {"metrics": {t: {"responses": conditions} for t in ("T4a","T4b","T4c","T4d")},
                "responses": {"normalize_outgoing": True,
                              "baseline": {"integrated": {t: 0 for t in ("T4a","T4b","T4c","T4d")}}}}
        result = assess(data)
        self.assertTrue(result["numerical_finite_integrated"])
        self.assertTrue(result["baseline_near_zero"])
        self.assertTrue(result["all_subtypes_share_winner"])
        self.assertFalse(result["biological_direction_selectivity_validated"])
        self.assertAlmostEqual(result["opposite_direction_dsi"]["T4a"], 0.6)

    def test_nonfinite_response_fails(self):
        conditions = {"p_positive": float("inf"), "p_negative": 2,
                      "q_positive": 1, "q_negative": 4}
        data = {"metrics": {t: {"responses": conditions} for t in ("T4a","T4b","T4c","T4d")},
                "responses": {"baseline": {"integrated": {t: 0 for t in ("T4a","T4b","T4c","T4d")}}}}
        self.assertFalse(assess(data)["numerical_finite_integrated"])
