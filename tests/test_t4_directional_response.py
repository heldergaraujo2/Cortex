import unittest

from cortex.experiments.t4_directional_response import simulate, direction_metrics


class DirectionalResponseTest(unittest.TestCase):
    def setUp(self):
        self.types = {"a": "T4a", "b": "T4b", "c": "T4c", "d": "T4d"}
        self.edges = [("l1", "relay", 1), ("relay", "a", 2),
                      ("relay", "b", 1), ("relay", "c", 1),
                      ("relay", "d", 1)]

    def test_delayed_signal_and_zero_baseline(self):
        schedules = {"forward": [{"active_l1_root_ids": ["l1"]}] +
                     [{"active_l1_root_ids": []} for _ in range(3)],
                     "reverse": [{"active_l1_root_ids": []} for _ in range(4)]}
        output = simulate(schedules, self.edges, self.types, decay=0)
        trace = output["conditions"]["forward"]["traces"]["T4a"]
        self.assertEqual(trace[:3], [0, 0, 2])
        self.assertEqual(output["baseline"]["integrated"]["T4a"], 0)
        self.assertEqual(output["conditions"]["reverse"]["integrated"]["T4a"], 0)
        self.assertEqual(direction_metrics(output)["T4a"]["preferred_condition"], "forward")
        self.assertFalse(output["biological_direction_selectivity_validated"])
        self.assertFalse(output["real_fafb_experiment_executed"])

    def test_normalization_bounds_recurrent_amplification(self):
        schedules = {"x": [{"active_l1_root_ids": ["l1"]}] +
                     [{"active_l1_root_ids": []} for _ in range(15)]}
        edges = [("l1", "relay", 1000), ("relay", "relay", 1000),
                 ("relay", "a", 1000), ("relay", "b", 1000),
                 ("relay", "c", 1000), ("relay", "d", 1000)]
        result = simulate(schedules, edges, self.types,
                          decay=0.25, normalize_outgoing=True)
        self.assertTrue(result["normalize_outgoing"])
        for subtype in ("T4a", "T4b", "T4c", "T4d"):
            self.assertLess(result["conditions"]["x"]["integrated"][subtype], 100)
        self.assertEqual(result["baseline"]["integrated"]["T4a"], 0)

    def test_overflow_is_not_silently_discarded(self):
        schedules = {"x": [{"active_l1_root_ids": ["l1"]}] +
                     [{"active_l1_root_ids": []} for _ in range(5)]}
        edges = [("l1", "relay", 1e308), ("relay", "relay", 1e308),
                 ("relay", "a", 1), ("relay", "b", 1),
                 ("relay", "c", 1), ("relay", "d", 1)]
        with self.assertRaises(FloatingPointError):
            simulate(schedules, edges, self.types, decay=0)

    def test_rejects_invalid_weights(self):
        with self.assertRaises(ValueError):
            simulate({"x": [{"active_l1_root_ids": []}]},
                     [("l1", "a", float("nan"))], self.types)


if __name__ == "__main__":
    unittest.main()
