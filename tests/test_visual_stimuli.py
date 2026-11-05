import pytest
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
