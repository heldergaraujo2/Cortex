"""Experimental temporal propagation from spatial L1 schedules to T4 subtypes.

A simplified directed, weighted, delayed graph model. NOT a validated biological
neural simulator or evidence of direction selectivity until real data and
appropriate controls are evaluated.
"""
from __future__ import annotations
from collections import defaultdict
from math import isfinite


T4_TYPES = ("T4a", "T4b", "T4c", "T4d")


def simulate(schedules, edges, cell_types, *, decay=0.25, threshold=0.0, normalize_outgoing=False):
    """Run four stimulus conditions through the same graph.

    edges: iterable of (presynaptic_root_id, postsynaptic_root_id, weight).
    Each directed edge takes one simulation step. No recurrent instant updates.
    Returns subtype activity traces, integrated responses and a baseline.
    """
    if not 0 <= decay < 1 or threshold < 0:
        raise ValueError("Invalid decay or threshold")
    graph = defaultdict(list)
    for pre, post, weight in edges:
        weight = float(weight)
        if not isfinite(weight) or weight < 0:
            raise ValueError("Weights must be finite and nonnegative")
        graph[str(pre)].append((str(post), weight))
    if normalize_outgoing:
        # Bound outgoing propagation by the remaining budget after decay.
        # Each source then contributes at most its previous total activity,
        # preventing recurrent amplification from the propagation operator.
        for root, outgoing in graph.items():
            total = sum(weight for _, weight in outgoing)
            if not isfinite(total):
                raise ValueError('Outgoing synapse weight sum overflow')
            budget = 1.0 - decay
            if total > budget:
                graph[root] = [(post, weight * (budget / total)) for post, weight in outgoing]
    cells = {str(k): v for k, v in cell_types.items()}
    if not all(any(t == subtype for t in cells.values()) for subtype in T4_TYPES):
        raise ValueError("All four T4 subtypes must be annotated")
    if not schedules or any(not frames for frames in schedules.values()):
        raise ValueError("Nonempty stimulus schedules required")

    def run(frames):
        state = {}
        traces = {subtype: [] for subtype in T4_TYPES}
        for frame in frames:
            next_state = defaultdict(float)
            for root, value in state.items():
                next_state[root] += decay * value
                for post, weight in graph.get(root, ()):
                    next_state[post] += value * weight
            for root in frame:
                next_state[str(root)] += 1.0
            if any(not isfinite(value) for value in next_state.values()):
                raise FloatingPointError('Nonfinite neural activity during propagation')
            state = {root: value for root, value in next_state.items()
                     if value > threshold}
            for subtype in T4_TYPES:
                subtype_total = sum(value for root, value in state.items()
                                    if cells.get(root) == subtype)
                if not isfinite(subtype_total):
                    raise FloatingPointError("Nonfinite aggregated T4 activity")
                traces[subtype].append(subtype_total)
        integrated = {subtype: sum(trace) for subtype, trace in traces.items()}
        if any(not isfinite(value) for value in integrated.values()):
            raise FloatingPointError("Nonfinite integrated T4 response")
        return {"traces": traces, "integrated": integrated}
    results = {direction: run([frame["active_l1_root_ids"] for frame in frames])
               for direction, frames in schedules.items()}
    steps = max(map(len, schedules.values()))
    baseline = run([[] for _ in range(steps)])
    return {"model": "simplified_delayed_weighted_graph_v2" if normalize_outgoing else "simplified_delayed_weighted_graph_v1",
            "normalize_outgoing": normalize_outgoing,
            "conditions": results, "baseline": baseline,
            "real_fafb_experiment_executed": False,
            "biological_direction_selectivity_validated": False}


def direction_metrics(result):
    """Descriptive directional contrasts; not biological validation.

    DSI is only defined when both members of a preregistered opposite pair
    are present. A zero response in both directions has undefined DSI.
    """
    conditions = result["conditions"]
    opposite = {"p_positive": "p_negative", "p_negative": "p_positive",
                "q_positive": "q_negative", "q_negative": "q_positive"}
    metrics = {}
    for subtype in T4_TYPES:
        responses = {name: values["integrated"][subtype]
                     for name, values in conditions.items()}
        if not responses or any(not isfinite(v) for v in responses.values()):
            raise ValueError("Directional responses must be finite and nonempty")
        preferred = max(responses, key=responses.get)
        rival = opposite.get(preferred)
        dsi = None
        if rival in responses:
            pref_value, opp_value = responses[preferred], responses[rival]
            denominator = pref_value + opp_value + 1e-12
            dsi = (pref_value - opp_value) / denominator
        metrics[subtype] = {"preferred_condition": preferred,
                            "responses": responses,
                            "opposite_condition": rival if rival in responses else None,
                            "direction_selectivity_index": dsi}
    return metrics
