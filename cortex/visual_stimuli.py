"""Spatially ordered ON-front schedules on the FAFB medulla column lattice.

The p/q coordinates are used as medulla-lattice indices, not as retinal or
world-space coordinates. x/y are deliberately not used here.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Literal

from cortex.spatial import ColumnAssignment

Axis = Literal["p", "q", "v"]


@dataclass(frozen=True, slots=True)
class LatticeSchedule:
    axis: Axis
    direction: int
    hemisphere: str
    progress_values: tuple[int, ...]
    frames: tuple[frozenset[str], ...]

    @property
    def active_root_ids(self) -> frozenset[str]:
        return frozenset(root_id for frame in self.frames for root_id in frame)

    @property
    def total_input_events(self) -> int:
        return sum(len(frame) for frame in self.frames)


def lattice_progress(p: int, q: int, axis: Axis) -> int:
    """Integer projection along one of the three cardinal medulla-lattice axes.

    The projections follow the hexagonal-lattice definitions in Seung (2024):
    p: 2p-q; q: 2q-p; v: p+q. Positive p/q/v point anterodorsal,
    posterodorsal and dorsal, respectively, in medulla coordinates.
    """
    if axis == "p":
        return 2 * p - q
    if axis == "q":
        return 2 * q - p
    if axis == "v":
        return p + q
    raise ValueError("axis must be one of 'p', 'q', or 'v'")


def build_lattice_schedule(
    assignments: Iterable[ColumnAssignment],
    input_ids: Iterable[str],
    hemisphere: str,
    axis: Axis,
    direction: int = 1,
) -> LatticeSchedule:
    """Build a moving one-column-wide ON front; reverse direction reverses frames.

    Each assigned L1 neuron is activated exactly once. Opposite directions use
    the same frames in reverse order, making total input events identical.
    """
    if axis not in {"p", "q", "v"}:
        raise ValueError("axis must be one of 'p', 'q', or 'v'")
    if direction not in {-1, 1}:
        raise ValueError("direction must be -1 or +1")
    if not hemisphere.strip():
        raise ValueError("hemisphere must be non-empty")

    allowed = set(input_ids)
    by_progress: dict[int, set[str]] = defaultdict(set)
    seen: set[str] = set()
    for row in assignments:
        if row.hemisphere != hemisphere or row.cell_type != "L1":
            continue
        if row.root_id not in allowed:
            continue
        if row.root_id in seen:
            raise ValueError(f"duplicate L1 column assignment for root_id {row.root_id}")
        seen.add(row.root_id)
        by_progress[lattice_progress(row.p, row.q, axis)].add(row.root_id)

    if not by_progress:
        raise ValueError(f"no assigned L1 input neurons for hemisphere {hemisphere!r}")

    # Keep empty projection bins: dropping them would silently accelerate the
    # front wherever the lattice has a missing slice.
    progress_values = tuple(range(min(by_progress), max(by_progress) + 1))
    frames = tuple(frozenset(by_progress.get(value, set())) for value in progress_values)
    if direction == -1:
        progress_values = tuple(reversed(progress_values))
        frames = tuple(reversed(frames))

    scheduled = frozenset(root_id for frame in frames for root_id in frame)
    if scheduled != seen:
        raise AssertionError("schedule did not include each assigned L1 exactly once")

    return LatticeSchedule(
        axis=axis,
        direction=direction,
        hemisphere=hemisphere,
        progress_values=progress_values,
        frames=frames,
    )
