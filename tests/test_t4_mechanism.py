import pytest

from cortex.t4_mechanism import (
    T4InputArm,
    T4MechanismConfig,
    compare_opposite_sweeps,
    default_t4_input_arms,
    run_t4_mechanism,
)


def test_no_stimulus_has_zero_response():
    result = run_t4_mechanism((9, 9, 9))
    assert result["metrics"]["integrated_rate"] == 0


def test_inhibitory_arm_reduces_direct_excitation():
    arms = default_t4_input_arms()
    direct = run_t4_mechanism((-2, -1, 0, 1, 2), (arms[0],))
    combined = run_t4_mechanism((-2, -1, 0, 1, 2), arms[:2])
    assert combined["metrics"]["integrated_rate"] < direct["metrics"]["integrated_rate"]


def test_mi9_off_response_and_inhibitory_synapse_form_disinhibitory_drive():
    arm = default_t4_input_arms()[2]
    result = run_t4_mechanism((-2, -1, 0, 1, 2), (arm,))
    assert max(result["metrics"]["arm_drive_traces"][arm.name]) > 0


def test_opposite_sweeps_are_equal_energy_but_asymmetric_in_synthetic_model():
    result = compare_opposite_sweeps()
    assert result["comparison"]["same_stimulus_event_count"] is True
    assert result["comparison"]["synthetic_directional_asymmetry_index"] != 0
    assert result["comparison"]["biological_dsi_claimed"] is False


def test_symmetric_direct_arm_has_no_directional_asymmetry():
    direct = T4InputArm(
        "direct", ("Mi1",), "ACH", 1, 1, 0, 1.0, 0, 1.0
    )
    result = compare_opposite_sweeps(arms=(direct,))
    assert result["comparison"]["synthetic_directional_asymmetry_index"] == pytest.approx(0)


def test_invalid_arm_parameters_are_rejected():
    arm = T4InputArm("bad", ("Mi1",), "ACH", 0, 1, 0, 1, 0, 1)
    with pytest.raises(ValueError, match="synaptic_sign"):
        run_t4_mechanism((0,), (arm,))


def test_invalid_config_is_rejected():
    with pytest.raises(ValueError, match="leak"):
        run_t4_mechanism((0,), config=T4MechanismConfig(leak=2))


def test_delay_is_an_explicit_parameter():
    immediate = T4InputArm("fast", ("Mi1",), "ACH", 1, 1, 0, 1, 0, 1)
    delayed = T4InputArm("delayed", ("Mi1",), "ACH", 1, 1, 0, 1, 2, 1)
    first = run_t4_mechanism((0, 1, 1), (immediate,))["metrics"]["rate_trace"]
    second = run_t4_mechanism((0, 1, 1), (delayed,))["metrics"]["rate_trace"]
    assert first != second
