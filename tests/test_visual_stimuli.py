import pytest
from cortex.dynamics import RateEdge, RateNetwork, run_rate_simulation_schedule
from cortex.spatial import ColumnAssignment
from cortex.visual_stimuli import build_lattice_schedule, lattice_progress

def rows():
    return (
        ColumnAssignment("a","left","L1","1",0,0,0,0),
        ColumnAssignment("b","left","L1","2",1,0,1,0),
        ColumnAssignment("c","left","L1","3",0,1,0,1),
        ColumnAssignment("d","left","L1","4",1,1,1,1),
        ColumnAssignment("m","left","Mi1","1",0,0,0,0),
        ColumnAssignment("r","right","L1","1",0,0,0,0),
    )

@pytest.mark.parametrize("axis,p,q,value",[("p",2,1,3),("q",2,1,0),("v",2,1,3)])
def test_projection(axis,p,q,value):
    assert lattice_progress(p,q,axis)==value

def test_opposite_directions_reverse_exact_frames_and_match_energy():
    ids={"a","b","c","d"}
    plus=build_lattice_schedule(rows(),ids,"left","p",1)
    minus=build_lattice_schedule(rows(),ids,"left","p",-1)
    assert minus.frames==tuple(reversed(plus.frames))
    assert plus.total_input_events==minus.total_input_events==4
    assert plus.active_root_ids==minus.active_root_ids==ids

def test_only_l1_from_requested_hemisphere_are_scheduled():
    result=build_lattice_schedule(rows(),{"a","b","c","d","r"},"left","v")
    assert result.active_root_ids=={"a","b","c","d"}

def test_duplicate_l1_assignment_is_rejected():
    with pytest.raises(ValueError,match="duplicate L1"):
        build_lattice_schedule(rows()+(rows()[0],),{"a","b","c","d"},"left","p")

@pytest.mark.parametrize("axis,direction",[("x",1),("p",0),("p",-2)])
def test_invalid_axis_and_direction_are_rejected(axis,direction):
    with pytest.raises(ValueError):
        build_lattice_schedule(rows(),{"a","b","c","d"},"left",axis,direction)

def test_empty_hemisphere_is_rejected():
    with pytest.raises(ValueError,match="no assigned L1"):
        build_lattice_schedule(rows(),{"a","b","c","d"},"right","p")


def test_scheduled_input_propagates_through_rate_network():
    network = RateNetwork(
        "ME_L",
        {"l1": "L1", "mi": "Mi1", "t4": "T4a"},
        (
            RateEdge("l1", "mi", 1.0, 5, "L1", "Mi1"),
            RateEdge("mi", "t4", 1.0, 5, "Mi1", "T4a"),
        ),
        ("l1",), ("t4",),
        {"T4a": ("t4",), "T4b": (), "T4c": (), "T4d": ()},
    )
    result = run_rate_simulation_schedule(
        network, (frozenset({"l1"}), frozenset(), frozenset()), leak=1.0
    )
    assert result["metrics"]["t4_rate_trace"] == [0.0, 0.0, 1.0]


def test_scheduled_input_control_stays_zero():
    network = RateNetwork(
        "ME_L", {"l1": "L1", "t4": "T4a"}, (), ("l1",), ("t4",),
        {"T4a": ("t4",), "T4b": (), "T4c": (), "T4d": ()},
    )
    result = run_rate_simulation_schedule(
        network, (frozenset(), frozenset(), frozenset())
    )
    assert result["metrics"]["peak_mean_t4_rate"] == 0.0



def test_missing_projection_bins_remain_empty_frames():
    sparse = (
        ColumnAssignment("a", "left", "L1", "1", 0, 0, 0, 0),
        ColumnAssignment("b", "left", "L1", "2", 0, 0, 2, 0),
    )
    schedule = build_lattice_schedule(sparse, {"a", "b"}, "left", "p", 1)
    assert schedule.progress_values == (0, 2, 4)
    assert schedule.frames == (frozenset({"a"}), frozenset(), frozenset({"b"}))
