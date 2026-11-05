import pytest

from cortex.spatial import ColumnAssignment
from cortex.t4_inputs import T4InputEdge
from cortex.t4_profiles import summarize_t4_target_profiles


def _assignments():
    return (
        ColumnAssignment("10", "left", "T4a", "C1", 1.0, 2.0, 3, 4),
        ColumnAssignment("11", "right", "T4b", "C1", 5.0, 6.0, 3, 4),
    )


def _edges():
    return (
        T4InputEdge("1", "10", "Mi1", "T4a", "ME_L", 8, "ACH"),
        T4InputEdge("1", "10", "Mi1", "T4a", "ME_L", 4, "ACH"),
        T4InputEdge("2", "10", "Mi4", "T4a", "ME_L", 5, "GABA"),
        T4InputEdge("3", "11", "Mi9", "T4b", "ME_R", 7, "GLUT"),
        T4InputEdge("4", "11", "TmY15", "T4b", "ME_R", 6, "GABA"),
        T4InputEdge("5", "12", "C3", "T4c", "ME_R", 9, "GABA"),
    )


def test_profiles_join_targets_to_exact_column_assignment():
    report = summarize_t4_target_profiles(_edges(), _assignments())
    assert report["unique_t4_target_root_ids_with_candidate_inputs"] == 3
    assert report["unique_t4_target_root_ids_with_column_assignment"] == 2
    assert report["unique_t4_target_root_ids_without_column_assignment"] == 1
    assert report["edge_rows_with_assigned_t4_target"] == 5
    assert report["edge_rows_with_unassigned_t4_target"] == 1
    assert report["synaptic_sign_assigned"] is False


def test_same_column_id_in_two_hemispheres_remains_distinct():
    report = summarize_t4_target_profiles(_edges(), _assignments())
    profiles = {row["t4_root_id"]: row for row in report["profiles_by_t4_target"]}
    assert profiles["10"]["column_identity"] == ["left", "C1"]
    assert profiles["11"]["column_identity"] == ["right", "C1"]


def test_per_target_profile_preserves_rows_and_structural_synapse_sums():
    report = summarize_t4_target_profiles(_edges(), _assignments())
    profiles = {row["t4_root_id"]: row for row in report["profiles_by_t4_target"]}
    mi1 = next(row for row in profiles["10"]["inputs"] if row["presynaptic_primary_type"] == "Mi1")
    assert mi1["connection_table_rows"] == 2
    assert mi1["distinct_presynaptic_root_ids"] == 1
    assert mi1["syn_count_sum"] == 12


def test_aggregate_profiles_separate_hemisphere_and_t4_subtype():
    report = summarize_t4_target_profiles(_edges(), _assignments())
    keys = {
        (row["t4_type"], row["hemisphere"], row["presynaptic_primary_type"])
        for row in report["aggregate_by_t4_type_hemisphere_input_type_neuropil_nt"]
    }
    assert ("T4a", "left", "Mi1") in keys
    assert ("T4b", "right", "Mi9") in keys
    assert ("T4c", "(unassigned)", "C3") in keys


def test_neuropil_hemisphere_mismatch_is_reported_not_filtered():
    edges = (
        T4InputEdge("1", "10", "Mi1", "T4a", "ME_R", 8, "ACH"),
    )
    report = summarize_t4_target_profiles(edges, _assignments())
    assert report["edge_rows_with_neuropil_hemisphere_mismatch"] == 1
    assert report["candidate_input_edge_rows"] == 1


def test_assignment_type_mismatch_is_rejected():
    edges = (T4InputEdge("1", "10", "Mi1", "T4b", "ME_L", 8, "ACH"),)
    with pytest.raises(ValueError, match="type mismatch"):
        summarize_t4_target_profiles(edges, _assignments())


def test_duplicate_t4_assignment_is_rejected():
    assignments = _assignments() + (_assignments()[0],)
    with pytest.raises(ValueError, match="duplicate T4 column assignment"):
        summarize_t4_target_profiles(_edges(), assignments)
