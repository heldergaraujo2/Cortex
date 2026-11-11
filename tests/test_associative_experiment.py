"""Tests of a deterministic synthetic baseline, not biological validation."""
import pytest

from cortex.experiments.associative import (
    Trial, accuracy, predict, run_experiment, synthetic_trials, train_perceptron,
)


def test_synthetic_training_improves_accuracy():
    result = run_experiment()
    assert result["dataset"] == "synthetic_only"
    assert result["biological_validation"] is False
    assert result["baseline_accuracy"] == 0.5
    assert result["trained_accuracy"] == 1.0


def test_deterministic_training():
    trials = synthetic_trials()
    assert train_perceptron(trials, dimensions=2) == train_perceptron(trials, dimensions=2)


def test_invalid_dimensions_rejected():
    with pytest.raises(ValueError):
        train_perceptron((Trial((1.0,), 1),), dimensions=2)


def test_invalid_labels_rejected():
    with pytest.raises(ValueError):
        train_perceptron((Trial((1.0, 0.0), 2),), dimensions=2)


def test_empty_evaluation_rejected():
    with pytest.raises(ValueError):
        accuracy((0.0,), ())


def test_dimension_mismatch_rejected():
    with pytest.raises(ValueError):
        predict((0.0,), (1.0, 0.0))
