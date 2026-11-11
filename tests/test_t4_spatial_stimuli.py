import csv
import gzip
import tempfile
import unittest
from pathlib import Path

from cortex.experiments.t4_spatial_stimuli import generate


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

    def test_invalid_steps(self):
        with self.assertRaises(ValueError):
            generate(None, None, steps=1)


if __name__ == "__main__":
    unittest.main()
