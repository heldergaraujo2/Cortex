"""Strict, dependency-free importer for the reduced FAFB v783 pilot.

Raw files are read-only inputs. Connection rows remain separated by neuropil;
the importer never silently sums rows or synapse counts across neuropils.
Coordinate units and biological meaning are intentionally not inferred.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

CELL_TYPES_FILE = "consolidated_cell_types.csv.gz"
CONNECTIONS_FILE = "connections_princeton.csv.gz"
COORDINATES_FILE = "coordinates.csv.gz"
REQUIRED_FILES = (CELL_TYPES_FILE, CONNECTIONS_FILE, COORDINATES_FILE)


@dataclass(frozen=True, slots=True)
class CoordinateRecord:
    root_id: str
    position: tuple[int, int, int]
    supervoxel_id: str


@dataclass(frozen=True, slots=True)
class PilotConnection:
    pre_root_id: str
    post_root_id: str
    pre_type: str
    post_type: str
    neuropil: str
    syn_count: int
    nt_type: str


@dataclass(frozen=True, slots=True)
class PilotConnectome:
    dataset: str
    cell_types: dict[str, str]
    coordinates_by_root_id: dict[str, tuple[CoordinateRecord, ...]]
    connections: tuple[PilotConnection, ...]
    file_manifest: tuple[dict[str, object], ...]
    total_connection_rows: int
    total_coordinate_rows: int
    coordinate_root_ids: int

    def summary(self) -> dict[str, object]:
        pilot_counts = Counter(
            cell_type for cell_type in self.cell_types.values()
            if is_pilot_type(cell_type)
        )
        pairs: dict[tuple[str, str], set[tuple[str, str]]] = {}
        rows_by_pair: Counter = Counter()
        rows_by_pair_neuropil: Counter = Counter()
        synapses_by_pair_neuropil: Counter = Counter()

        for edge in self.connections:
            group = (group_type(edge.pre_type), group_type(edge.post_type))
            pair = (edge.pre_root_id, edge.post_root_id)
            pairs.setdefault(group, set()).add(pair)
            rows_by_pair[group] += 1
            group_roi = (*group, edge.neuropil)
            rows_by_pair_neuropil[group_roi] += 1
            synapses_by_pair_neuropil[group_roi] += edge.syn_count

        pair_summary = []
        for (pre_type, post_type), unique_pairs in sorted(pairs.items()):
            neuropils = []
            for key in sorted(k for k in rows_by_pair_neuropil
                              if k[0] == pre_type and k[1] == post_type):
                neuropils.append({
                    "neuropil": key[2],
                    "table_rows": rows_by_pair_neuropil[key],
                    "syn_count_sum_within_neuropil": synapses_by_pair_neuropil[key],
                })
            pair_summary.append({
                "pre_type": pre_type,
                "post_type": post_type,
                "table_rows_across_neuropils": rows_by_pair[(pre_type, post_type)],
                "distinct_pre_post_root_id_pairs": len(unique_pairs),
                "neuropils": neuropils,
            })

        pilot_ids = {root_id for root_id, cell_type in self.cell_types.items()
                     if is_pilot_type(cell_type)}
        coordinate_ids = set(self.coordinates_by_root_id)
        return {
            "dataset": self.dataset,
            "cell_type_counts": dict(sorted(pilot_counts.items())),
            "pilot_neuron_ids": len(pilot_ids),
            "coordinate_rows_total": self.total_coordinate_rows,
            "coordinate_root_ids_total": self.coordinate_root_ids,
            "pilot_neuron_ids_with_coordinates": len(pilot_ids & coordinate_ids),
            "pilot_neuron_ids_without_coordinates": len(pilot_ids - coordinate_ids),
            "coordinate_rows_for_pilot_neurons": sum(
                len(rows) for rows in self.coordinates_by_root_id.values()
            ),
            "connection_table_rows_total": self.total_connection_rows,
            "pilot_connection_rows": len(self.connections),
            "pilot_type_pairs": pair_summary,
            "aggregation_rule": (
                "Rows are retained per neuropil. Distinct directed neuron pairs are counted by "
                "(pre_root_id, post_root_id) across neuropils; syn_count is summed only within "
                "each neuropil. Coordinate position units are not inferred."
            ),
            "file_manifest": list(self.file_manifest),
        }


def is_pilot_type(cell_type: str) -> bool:
    return cell_type in {"L1", "Mi1", "Tm3"} or cell_type.startswith("T4")


def group_type(cell_type: str) -> str:
    return "T4" if cell_type.startswith("T4") else cell_type


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require_columns(reader: csv.DictReader, required: set[str], path: Path) -> None:
    actual = set(reader.fieldnames or ())
    missing = required - actual
    if missing:
        raise ValueError(f"{path.name}: missing required columns {sorted(missing)}; got {reader.fieldnames}")


def _parse_position(raw: str, path: Path, line_number: int) -> tuple[int, int, int]:
    values = re.findall(r"-?\d+", raw)
    if len(values) != 3:
        raise ValueError(
            f"{path.name}:{line_number}: expected three integer coordinates, got {raw!r}"
        )
    return int(values[0]), int(values[1]), int(values[2])


def load_pilot_connectome(data_dir: str | Path) -> PilotConnectome:
    """Read the three FAFB v783 products and retain the reduced pilot graph.

    The source connection file is expected to be the Codex Princeton table,
    whose records are separated by neuropil. No rows are merged or deduplicated.
    """
    root = Path(data_dir)
    paths = {name: root / name for name in REQUIRED_FILES}
    missing = [path.name for path in paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing required FAFB v783 files: {', '.join(missing)}")

    manifest: list[dict[str, object]] = []
    for name in REQUIRED_FILES:
        path = paths[name]
        manifest.append({
            "file": name,
            "size_bytes": path.stat().st_size,
            "sha256": _sha256(path),
        })

    cell_types: dict[str, str] = {}
    with gzip.open(paths[CELL_TYPES_FILE], "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        _require_columns(reader, {"root_id", "primary_type"}, paths[CELL_TYPES_FILE])
        for line_number, row in enumerate(reader, start=2):
            root_id = (row.get("root_id") or "").strip()
            cell_type = (row.get("primary_type") or "").strip()
            if not root_id:
                raise ValueError(f"{CELL_TYPES_FILE}:{line_number}: empty root_id")
            if root_id in cell_types:
                raise ValueError(f"{CELL_TYPES_FILE}:{line_number}: duplicate root_id {root_id}")
            if cell_type:
                cell_types[root_id] = cell_type

    target_ids = {
        root_id for root_id, cell_type in cell_types.items() if is_pilot_type(cell_type)
    }
    coordinate_records: dict[str, list[CoordinateRecord]] = {}
    total_coordinate_rows = 0
    coordinate_root_ids: set[str] = set()
    with gzip.open(paths[COORDINATES_FILE], "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        _require_columns(reader, {"root_id", "position", "supervoxel_id"}, paths[COORDINATES_FILE])
        for line_number, row in enumerate(reader, start=2):
            total_coordinate_rows += 1
            root_id = (row.get("root_id") or "").strip()
            if not root_id:
                raise ValueError(f"{COORDINATES_FILE}:{line_number}: empty root_id")
            coordinate_root_ids.add(root_id)
            if root_id in target_ids:
                record = CoordinateRecord(
                    root_id=root_id,
                    position=_parse_position(row.get("position") or "", paths[COORDINATES_FILE], line_number),
                    supervoxel_id=(row.get("supervoxel_id") or "").strip(),
                )
                coordinate_records.setdefault(root_id, []).append(record)

    connections: list[PilotConnection] = []
    total_connection_rows = 0
    with gzip.open(paths[CONNECTIONS_FILE], "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        _require_columns(
            reader,
            {"pre_root_id", "post_root_id", "neuropil", "syn_count", "nt_type"},
            paths[CONNECTIONS_FILE],
        )
        for line_number, row in enumerate(reader, start=2):
            total_connection_rows += 1
            pre_id = (row.get("pre_root_id") or "").strip()
            post_id = (row.get("post_root_id") or "").strip()
            if not pre_id or not post_id:
                raise ValueError(f"{CONNECTIONS_FILE}:{line_number}: empty pre/post root_id")
            pre_type = cell_types.get(pre_id)
            post_type = cell_types.get(post_id)
            if not pre_type or not post_type or not (
                is_pilot_type(pre_type) and is_pilot_type(post_type)
            ):
                continue
            try:
                syn_count = int(row["syn_count"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{CONNECTIONS_FILE}:{line_number}: invalid syn_count {row.get('syn_count')!r}"
                ) from exc
            if syn_count < 0:
                raise ValueError(f"{CONNECTIONS_FILE}:{line_number}: negative syn_count")
            connections.append(PilotConnection(
                pre_root_id=pre_id,
                post_root_id=post_id,
                pre_type=pre_type,
                post_type=post_type,
                neuropil=(row.get("neuropil") or "").strip(),
                syn_count=syn_count,
                nt_type=(row.get("nt_type") or "").strip(),
            ))

    return PilotConnectome(
        dataset="FlyWire FAFB v783",
        cell_types=cell_types,
        coordinates_by_root_id={
            root_id: tuple(records) for root_id, records in coordinate_records.items()
        },
        connections=tuple(connections),
        file_manifest=tuple(manifest),
        total_connection_rows=total_connection_rows,
        total_coordinate_rows=total_coordinate_rows,
        coordinate_root_ids=len(coordinate_root_ids),
    )
