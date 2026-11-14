import csv
import gzip
import tempfile
import unittest
from pathlib import Path

from cortex.experiments.t4_spatial_stimuli import generate, balance_schedules


class FourDirectionInputsTest(unittest.TestCase):
    def test_realistic_column_schema_and_reverse_directions(self):
        with tempfile.TemporaryDirectory() as temp:
            annotations = Path(temp) / "types.csv.gz"
            columns = Path(temp) / "columns.csv.gz"
            with gzip.open(annotations, "wt", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["root_id", "primary_type"])
                writer.writeheader()
                writer.writerows([
                    {"root_id": "1", "primary_type": "L1"},
                    {"root_id": "2", "primary_type": "L1"},
                    {"root_id": "3", "primary_type": "L1"},
                    {"root_id": "4", "primary_type": "T4a"},
                ])
            with gzip.open(columns, "wt", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["root_id", "p", "q"])
                writer.writeheader()
                writer.writerows([
                    {"root_id": "1", "p": "0", "q": "0"},
                    {"root_id": "2", "p": "2", "q": "0"},
                    {"root_id": "3", "p": "0", "q": "2"},
                    {"root_id": "4", "p": "3", "q": "3"},
                ])
            data = generate(annotations, columns, steps=3, stripe_width=0.5)
            self.assertEqual(data["mapped_l1_neurons"], 3)
            self.assertEqual(set(data["directions"]), {"p_positive", "p_negative", "q_positive", "q_negative"})
            self.assertEqual(data["directions"]["p_positive"][0]["active_l1_root_ids"], ["1", "3"])
            self.assertEqual(data["directions"]["p_negative"][0]["active_l1_root_ids"], ["2"])
            self.assertEqual(data["directions"]["q_positive"][0]["active_l1_root_ids"], ["1", "2"])
            self.assertEqual(data["directions"]["q_negative"][0]["active_l1_root_ids"], ["3"])
            self.assertFalse(data["direction_selectivity_validated"])
            self.assertFalse(data["neural_simulation_executed"])

    def test_balancing_is_deterministic_and_preserves_original(self):
        schedules = {
            "p_positive": [{"step": 0, "active_l1_root_ids": ["1", "2", "3"]},
                           {"step": 1, "active_l1_root_ids": ["4", "5"]}],
            "q_positive": [{"step": 0, "active_l1_root_ids": ["1", "2"]},
                           {"step": 1, "active_l1_root_ids": ["3", "4"]}],
        }
        balanced = balance_schedules(schedules)
        self.assertEqual(balanced, balance_schedules(schedules))
        self.assertEqual([sum(len(f["active_l1_root_ids"]) for f in frames)
                          for frames in balanced.values()], [4, 4])
        self.assertEqual(len(schedules["p_positive"][0]["active_l1_root_ids"]), 3)
        self.assertEqual([f["step"] for f in balanced["p_positive"]], [0, 1])

    def test_balancing_rejects_empty_drive(self):
        with self.assertRaises(ValueError):
            balance_schedules({"p_positive": [{"step": 0, "active_l1_root_ids": []}]})

    def test_invalid_steps(self):
        with self.assertRaises(ValueError):
            generate(None, None, steps=1)


if __name__ == "__main__":
    unittest.main()
