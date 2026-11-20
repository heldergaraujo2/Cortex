from cortex.t4_biological_reference import evaluate, validate_reference


def reference():
    return {
        "doi": "10.0000/example-not-a-real-reference",
        "figure": "Figure 1", "license": "test fixture",
        "axis_transform_source": "synthetic test only",
        "axis_transform": "p_positive -> p_positive (synthetic)",
        "calibration_sample_ids": ["cal-1"],
        "held_out_sample_ids": ["hold-1"],
        "observations": {
            subtype: {
                "preferred_direction": "p_positive",
                "dsi": 0.4,
                "dsi_ci95": [0.2, 0.6],
            }
            for subtype in ("T4a", "T4b", "T4c", "T4d")
        },
    }


def test_valid_structure_does_not_claim_biological_validation():
    sample = reference()
    assert validate_reference(sample)["valid"]
    result = evaluate(sample, {})
    assert not result["biological_direction_selectivity_validated"]
    assert not result["held_out_physiological_reference_verified"]
    assert not result["independent_anatomical_alignment_verified"]


def test_missing_reference_fails_closed():
    assert not validate_reference({})["valid"]
    assert not evaluate({}, {})["biological_direction_selectivity_validated"]


def test_rejects_data_leakage():
    sample = reference()
    sample["held_out_sample_ids"] = ["cal-1"]
    assert not validate_reference(sample)["valid"]


def test_rejects_invalid_dsi():
    sample = reference()
    sample["observations"]["T4a"]["dsi"] = float("nan")
    assert not validate_reference(sample)["valid"]


def test_rejects_missing_subtype():
    sample = reference()
    del sample["observations"]["T4d"]
    assert not validate_reference(sample)["valid"]
