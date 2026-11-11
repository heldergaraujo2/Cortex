"""Structural input profiles for assigned T4 target neurons.

The module joins T4 input edges to the existing T4 column assignments. It does
not assign synaptic signs or infer source-cell columns/visual directions.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean, median
from typing import Iterable

from cortex.spatial import ColumnAssignment
from cortex.t4_inputs import T4InputEdge, T4_TYPES


def summarize_t4_target_profiles(
    edges: tuple[T4InputEdge, ...],
    assignments: Iterable[ColumnAssignment],
) -> dict[str, object]:
    assignment_by_id: dict[str, ColumnAssignment] = {}
    for assignment in assignments:
        if assignment.cell_type not in T4_TYPES:
            continue
        if assignment.root_id in assignment_by_id:
            raise ValueError(f"duplicate T4 column assignment for root_id {assignment.root_id}")
        assignment_by_id[assignment.root_id] = assignment

    target_ids = {edge.post_root_id for edge in edges}
    for edge in edges:
        assignment = assignment_by_id.get(edge.post_root_id)
        if assignment is not None and assignment.cell_type != edge.post_type:
            raise ValueError(
                f"T4 assignment type mismatch for {edge.post_root_id}: "
                f"{assignment.cell_type!r} != {edge.post_type!r}"
            )

    target_group_rows: Counter[tuple[str, str, str, str]] = Counter()
    target_group_synapses: Counter[tuple[str, str, str, str]] = Counter()
    target_group_pre_ids: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    target_group_info: dict[str, dict[str, object]] = {}
    target_group_keys: dict[str, set[tuple[str, str, str, str]]] = defaultdict(set)
    hemisphere_mismatch_rows = 0
    unassigned_edge_rows = 0

    for edge in edges:
        assignment = assignment_by_id.get(edge.post_root_id)
        if assignment is None:
            unassigned_edge_rows += 1
            hemisphere = "(unassigned)"
        else:
            hemisphere = assignment.hemisphere
            expected = (
                "left" if edge.neuropil.endswith("_L")
                else "right" if edge.neuropil.endswith("_R")
                else None
            )
            if expected is not None and expected != hemisphere:
                hemisphere_mismatch_rows += 1
            target_group_info[edge.post_root_id] = {
                "t4_root_id": edge.post_root_id,
                "t4_type": edge.post_type,
                "hemisphere": assignment.hemisphere,
                "column_id": assignment.column_id,
                "column_identity": [assignment.hemisphere, assignment.column_id],
                "p": assignment.p,
                "q": assignment.q,
                "x": assignment.x,
                "y": assignment.y,
                "spatial_semantics": (
                    "p/q and x/y preserved as supplied; no transform or visual direction inferred"
                ),
            }
        if edge.post_root_id not in target_group_info:
            target_group_info[edge.post_root_id] = {
                "t4_root_id": edge.post_root_id,
                "t4_type": edge.post_type,
                "hemisphere": None,
                "column_id": None,
                "column_identity": None,
                "p": None,
                "q": None,
                "x": None,
                "y": None,
                "spatial_semantics": "no column assignment available for this T4 target",
            }
        key = (edge.pre_type, edge.neuropil, edge.nt_type, edge.post_type)
        target_key = (edge.post_root_id, *key[:3])
        target_group_rows[target_key] += 1
        target_group_synapses[target_key] += edge.syn_count
        target_group_pre_ids[target_key].add(edge.pre_root_id)
        target_group_keys[edge.post_root_id].add(key)

    target_profiles: list[dict[str, object]] = []
    aggregate_totals: dict[tuple[str, str, str, str, str], list[int]] = defaultdict(list)
    aggregate_rows: Counter[tuple[str, str, str, str, str]] = Counter()
    aggregate_synapses: Counter[tuple[str, str, str, str, str]] = Counter()
    aggregate_pre_ids: dict[tuple[str, str, str, str, str], set[str]] = defaultdict(set)

    for target_id in sorted(target_ids):
        info = target_group_info[target_id]
        target_inputs = []
        for key in sorted(target_group_keys[target_id]):
            pre_type, neuropil, nt_type, post_type = key
            target_key = (target_id, pre_type, neuropil, nt_type)
            row_count = target_group_rows[target_key]
            syn_sum = target_group_synapses[target_key]
            distinct_pre = len(target_group_pre_ids[target_key])
            target_inputs.append({
                "presynaptic_primary_type": pre_type,
                "neuropil": neuropil,
                "nt_type_as_supplied": nt_type,
                "connection_table_rows": row_count,
                "distinct_presynaptic_root_ids": distinct_pre,
                "syn_count_sum": syn_sum,
            })
            hemisphere = info["hemisphere"] or "(unassigned)"
            aggregate_key = (post_type, hemisphere, pre_type, neuropil, nt_type)
            aggregate_totals[aggregate_key].append(syn_sum)
            aggregate_rows[aggregate_key] += row_count
            aggregate_synapses[aggregate_key] += syn_sum
            aggregate_pre_ids[aggregate_key].update(target_group_pre_ids[target_key])
        target_profiles.append({**info, "inputs": target_inputs})

    aggregate_summary = []
    for key in sorted(aggregate_totals):
        post_type, hemisphere, pre_type, neuropil, nt_type = key
        values = aggregate_totals[key]
        aggregate_summary.append({
            "t4_type": post_type,
            "hemisphere": hemisphere,
            "presynaptic_primary_type": pre_type,
            "neuropil": neuropil,
            "nt_type_as_supplied": nt_type,
            "t4_target_count": len(values),
            "connection_table_rows": aggregate_rows[key],
            "distinct_presynaptic_root_ids": len(aggregate_pre_ids[key]),
            "syn_count_sum": aggregate_synapses[key],
            "mean_syn_count_per_t4_target": mean(values),
            "median_syn_count_per_t4_target": median(values),
            "min_syn_count_per_t4_target": min(values),
            "max_syn_count_per_t4_target": max(values),
        })

    assigned_target_ids = target_ids & set(assignment_by_id)
    target_counts_by_type: Counter[str] = Counter(
        assignment_by_id[target_id].cell_type for target_id in assigned_target_ids
    )
    target_counts_total_by_type: Counter[str] = Counter(
        edge.post_type for edge in edges
    )
    return {
        "dataset": "FlyWire FAFB v783",
        "candidate_input_edge_rows": len(edges),
        "unique_t4_target_root_ids_with_candidate_inputs": len(target_ids),
        "unique_t4_target_root_ids_with_column_assignment": len(assigned_target_ids),
        "unique_t4_target_root_ids_without_column_assignment": len(target_ids - assigned_target_ids),
        "edge_rows_with_assigned_t4_target": len(edges) - unassigned_edge_rows,
        "edge_rows_with_unassigned_t4_target": unassigned_edge_rows,
        "edge_rows_with_neuropil_hemisphere_mismatch": hemisphere_mismatch_rows,
        "assigned_t4_targets_by_subtype": dict(sorted(target_counts_by_type.items())),
        "candidate_input_edges_by_t4_subtype": dict(sorted(target_counts_total_by_type.items())),
        "profiles_by_t4_target": target_profiles,
        "aggregate_by_t4_type_hemisphere_input_type_neuropil_nt": aggregate_summary,
        "synaptic_sign_assigned": False,
        "interpretation_limits": [
            "T4 target assignments are joined by exact root_id and primary type",
            "column identity is the pair (hemisphere, column_id); IDs may repeat across hemispheres",
            "p/q and x/y are preserved as supplied; no transform or visual direction is inferred",
            "presynaptic candidate cells do not have column assignments in the current assignment table",
            "nt_type is a prediction label, not a verified physiological sign",
            "syn_count is structural and is not treated as synaptic efficacy",
        ],
    }
