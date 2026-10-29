"""Strict parser and spatial coverage report for FlyWire FAFB v783 column assignments.

The table's x/y and p/q fields are retained separately: they are not interchangeable,
and this module does not infer physical units or a retinal transform.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

COLUMN_ASSIGNMENT_FILE = "column_assignment.csv.gz"
REQUIRED_COLUMNS = {
    "root_id", "hemisphere", "type", "column_id", "x", "y", "p", "q",
}
T4_TYPES = {"T4a", "T4b", "T4c", "T4d"}


@dataclass(frozen=True, slots=True)
class ColumnAssignment:
    root_id: str
    hemisphere: str
    cell_type: str
    column_id: str
    x: float
    y: float
    p: int
    q: int


@dataclass(frozen=True, slots=True)
class ColumnAssignmentReport:
    path: str
    size_bytes: int
    sha256: str
    rows: tuple[ColumnAssignment, ...]
    unmapped_root_ids: int

    def summary(self, primary_types: dict[str, str]) -> dict[str, object]:
        assigned_ids = {row.root_id for row in self.rows}
        pilot_ids = {
            root_id for root_id, cell_type in primary_types.items()
            if cell_type in {"L1", "Mi1", "Tm3"} | T4_TYPES
        }
        coverage_by_primary_type: dict[str, dict[str, int]] = {}
        for cell_type in ("L1", "Mi1", "Tm3", "T4a", "T4b", "T4c", "T4d"):
            ids = {root_id for root_id in pilot_ids
                   if primary_types[root_id] == cell_type}
            covered = ids & assigned_ids
            coverage_by_primary_type[cell_type] = {
                "pilot_ids": len(ids),
                "assigned_ids": len(covered),
                "unassigned_ids": len(ids - assigned_ids),
                "coverage_fraction": (len(covered) / len(ids)) if ids else None,
            }

        columns_by_hemisphere: dict[str, set[str]] = defaultdict(set)
        p_q_by_hemisphere: dict[str, set[tuple[int, int]]] = defaultdict(set)
        assigned_type_rows: Counter[str] = Counter()
        assigned_type_ids: dict[str, set[str]] = defaultdict(set)
        for row in self.rows:
            columns_by_hemisphere[row.hemisphere].add(row.column_id)
            p_q_by_hemisphere[row.hemisphere].add((row.p, row.q))
            assigned_type_rows[row.cell_type] += 1
            assigned_type_ids[row.cell_type].add(row.root_id)

        return {
            "dataset": "FlyWire FAFB v783",
            "source_file": {
                "name": Path(self.path).name,
                "size_bytes": self.size_bytes,
                "sha256": self.sha256,
            },
            "rows": len(self.rows),
            "unique_root_ids": len(assigned_ids),
            "rows_with_root_id_not_in_primary_type_table": self.unmapped_root_ids,
            "pilot_ids": len(pilot_ids),
            "pilot_ids_with_column_assignment": len(pilot_ids & assigned_ids),
            "pilot_ids_without_column_assignment": len(pilot_ids - assigned_ids),
            "coverage_by_primary_type": coverage_by_primary_type,
            "unique_columns_by_hemisphere": {
                hemisphere: len(columns)
                for hemisphere, columns in sorted(columns_by_hemisphere.items())
            },
            "unique_hemisphere_column_pairs": sum(
                len(columns) for columns in columns_by_hemisphere.values()
            ),
            "unique_p_q_pairs_by_hemisphere": {
                hemisphere: len(pairs)
                for hemisphere, pairs in sorted(p_q_by_hemisphere.items())
            },
            "assignment_rows_by_type": dict(sorted(assigned_type_rows.items())),
            "assignment_unique_ids_by_type": {
                cell_type: len(ids)
                for cell_type, ids in sorted(assigned_type_ids.items())
            },
            "coordinate_semantics": {
                "x_y": "preserved as supplied; units/meaning not inferred by this importer",
                "p_q": "preserved as integer lattice coordinates; transform not inferred",
                "column_identity": "pair (hemisphere, column_id), because column IDs may repeat between hemispheres",
            },
        }


def _finite_number(value: str, field: str, line_number: int) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field} at CSV line {line_number}: {value!r}") from exc
    if not math.isfinite(parsed):
        raise ValueError(f"invalid {field} at CSV line {line_number}: {value!r}")
    return parsed


def load_column_assignments(
    path: str | Path,
    primary_types: dict[str, str],
) -> ColumnAssignmentReport:
    """Read a Codex column-assignment CSV.GZ and validate its structure."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)

    digest = hashlib.sha256()
    with path.open("rb") as raw:
        for chunk in iter(lambda: raw.read(1024 * 1024), b""):
            digest.update(chunk)

    rows: list[ColumnAssignment] = []
    unmapped = 0
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(
                f"missing required columns {sorted(REQUIRED_COLUMNS)}; "
                f"got {reader.fieldnames}"
            )
        for line_number, row in enumerate(reader, start=2):
            root_id = (row.get("root_id") or "").strip()
            hemisphere = (row.get("hemisphere") or "").strip()
            cell_type = (row.get("type") or "").strip()
            column_id = (row.get("column_id") or "").strip()
            if not root_id or not hemisphere or not cell_type or not column_id:
                raise ValueError(f"empty required column-assignment field at CSV line {line_number}")
            try:
                p = int(row["p"])
                q = int(row["q"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid integer p/q at CSV line {line_number}") from exc
            x = _finite_number(row["x"], "x", line_number)
            y = _finite_number(row["y"], "y", line_number)
            rows.append(ColumnAssignment(
                root_id=root_id,
                hemisphere=hemisphere,
                cell_type=cell_type,
                column_id=column_id,
                x=x, y=y, p=p, q=q,
            ))
            if root_id not in primary_types:
                unmapped += 1

    return ColumnAssignmentReport(
        path=str(path),
        size_bytes=path.stat().st_size,
        sha256=digest.hexdigest(),
        rows=tuple(rows),
        unmapped_root_ids=unmapped,
    )
