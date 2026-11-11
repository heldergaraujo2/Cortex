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

    def test_rejects_invalid_weights(self):
        with self.assertRaises(ValueError):
            simulate({"x": [{"active_l1_root_ids": []}]},
                     [("l1", "a", float("nan"))], self.types)


if __name__ == "__main__":
    unittest.main()
