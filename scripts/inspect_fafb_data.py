from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path("data/raw/fafb_v783")
CELL_FILE = "consolidated_cell_types.csv.gz"
CONNECTION_FILE = "connections_princeton.csv.gz"
COORDINATE_FILE = "coordinates.csv.gz"
FILES = (CELL_FILE, CONNECTION_FILE, COORDINATE_FILE)
REPORT_PATH = Path("fafb_v783_validation_report.json")
PILOT_TYPES = {"L1", "Mi1", "Tm3"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_csv(path: Path) -> dict:
    result = {
        "file": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "columns": [],
        "data_rows": 0,
        "sample_rows": [],
        "gzip_csv_readable": False,
    }
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        result["columns"] = next(reader, [])
        for row in reader:
            result["data_rows"] += 1
            if len(result["sample_rows"]) < 2:
                result["sample_rows"].append([cell[:160] for cell in row[:12]])
    result["gzip_csv_readable"] = True
    return result


def load_primary_types(path: Path) -> tuple[dict[str, str], Counter]:
    root_to_type: dict[str, str] = {}
    counts: Counter = Counter()
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"root_id", "primary_type"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Expected columns {sorted(required)}; got {reader.fieldnames}")
        for row in reader:
            root_id = row["root_id"].strip()
            cell_type = row["primary_type"].strip()
            if root_id and cell_type:
                if root_id in root_to_type and root_to_type[root_id] != cell_type:
                    raise ValueError(f"Conflicting primary_type annotations for root_id {root_id}")
                root_to_type[root_id] = cell_type
                counts[cell_type] += 1
    return root_to_type, counts


def group_type(cell_type: str | None) -> str | None:
    if cell_type in PILOT_TYPES:
        return cell_type
    if cell_type and cell_type.startswith("T4"):
        return "T4"
    return None


def analyze_pilot_connections(path: Path, root_to_type: dict[str, str]) -> dict:
    row_counts: Counter = Counter()
    synapse_sums_by_neuropil: Counter = Counter()
    row_counts_by_neuropil: Counter = Counter()
    pairs_by_group: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    pairs_by_group_neuropil: dict[tuple[str, str, str], set[tuple[str, str]]] = defaultdict(set)
    exact_rows: Counter = Counter()
    exact_pairs: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    mapping_rows = Counter()
    all_rows = 0

    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"pre_root_id", "post_root_id", "syn_count", "neuropil"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"Expected columns {sorted(required)}; got {reader.fieldnames}")
        for row in reader:
            all_rows += 1
            pre_id = row["pre_root_id"].strip()
            post_id = row["post_root_id"].strip()
            pre_type = root_to_type.get(pre_id)
            post_type = root_to_type.get(post_id)
            mapping_rows["pre_id_mapped"] += bool(pre_type)
            mapping_rows["post_id_mapped"] += bool(post_type)
            mapping_rows["both_ids_mapped"] += bool(pre_type and post_type)

            pre_group = group_type(pre_type)
            post_group = group_type(post_type)
            if not (pre_group and post_group):
                continue

            neuropil = row["neuropil"].strip() or "(empty)"
            group_key = (pre_group, post_group)
            pair_key = (pre_id, post_id)
            group_neuropil_key = (pre_group, post_group, neuropil)
            pairs_by_group[group_key].add(pair_key)
            pairs_by_group_neuropil[group_neuropil_key].add(pair_key)
            row_counts[group_key] += 1
            row_counts_by_neuropil[group_neuropil_key] += 1
            try:
                synapse_sums_by_neuropil[group_neuropil_key] += int(row["syn_count"])
            except (TypeError, ValueError):
                pass

            exact_key = (pre_type or "(untyped)", post_type or "(untyped)")
            exact_rows[exact_key] += 1
            exact_pairs[exact_key].add(pair_key)

    grouped_summary = []
    for (pre, post), count in sorted(row_counts.items()):
        neuropils = []
        matching_keys = sorted(
            key for key in row_counts_by_neuropil
            if key[0] == pre and key[1] == post
        )
        for key in matching_keys:
            neuropils.append({
                "neuropil": key[2],
                "table_rows": row_counts_by_neuropil[key],
                "distinct_pre_post_root_id_pairs": len(pairs_by_group_neuropil[key]),
                "syn_count_sum_within_neuropil": synapse_sums_by_neuropil[key],
            })
        grouped_summary.append({
            "pre_type": pre,
            "post_type": post,
            "table_rows_across_neuropils": count,
            "distinct_pre_post_root_id_pairs_across_table": len(pairs_by_group[(pre, post)]),
            "neuropils": neuropils,
        })

    exact_summary = [
        {
            "pre_type": pre,
            "post_type": post,
            "table_rows_across_neuropils": exact_rows[(pre, post)],
            "distinct_pre_post_root_id_pairs_across_table": len(exact_pairs[(pre, post)]),
        }
        for pre, post in sorted(exact_rows)
    ]

    return {
        "connection_table_rows_total": all_rows,
        "rows_with_pre_id_in_cell_type_table": mapping_rows["pre_id_mapped"],
        "rows_with_post_id_in_cell_type_table": mapping_rows["post_id_mapped"],
        "rows_with_both_ids_in_cell_type_table": mapping_rows["both_ids_mapped"],
        "pair_counting_note": (
            "table_rows count records in connections_princeton; a pre/post root-ID pair may appear "
            "in multiple neuropils. Distinct pair counts deduplicate (pre_root_id, post_root_id) "
            "across the whole table. syn_count sums are reported only within each neuropil and are "
            "not added across neuropils."
        ),
        "pilot_group_pairs": grouped_summary,
        "exact_primary_type_pairs": exact_summary,
    }


def coordinate_coverage(path: Path, target_ids: set[str]) -> dict:
    coordinate_ids: set[str] = set()
    with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        if "root_id" not in columns:
            raise ValueError(f"coordinates file has no root_id column: {columns}")
        for row in reader:
            root_id = (row.get("root_id") or "").strip()
            if root_id:
                coordinate_ids.add(root_id)
    covered = target_ids & coordinate_ids
    return {
        "columns": columns,
        "unique_root_ids": len(coordinate_ids),
        "pilot_target_ids": len(target_ids),
        "pilot_target_ids_with_coordinates": len(covered),
        "pilot_target_ids_without_coordinates": len(target_ids - coordinate_ids),
    }


def main() -> int:
    report = {
        "dataset": "FlyWire FAFB v783",
        "purpose": "Structural evidence check for the L1/Mi1/Tm3/T4 pilot",
        "files": [],
        "cell_type_summary": {},
        "pilot_connection_analysis": {},
        "coordinate_coverage": {},
        "errors": [],
        "scientific_limit": (
            "Observed structural connectivity does not by itself establish functional direction "
            "selectivity, causal influence, or a complete biological circuit."
        ),
    }

    for filename in FILES:
        path = DATA_DIR / filename
        if not path.is_file():
            report["errors"].append(f"Missing file: {path.as_posix()}")
            continue
        try:
            item = inspect_csv(path)
            report["files"].append(item)
            print(f"\nFILE: {item['file']}")
            print(f"SIZE_BYTES: {item['size_bytes']}")
            print(f"SHA256: {item['sha256']}")
            print("COLUMNS: " + json.dumps(item["columns"], ensure_ascii=False))
            print(f"DATA_ROWS: {item['data_rows']}")
            print("SAMPLE_ROWS: " + json.dumps(item["sample_rows"], ensure_ascii=False))
            print("GZIP_CSV_READABLE: true")
        except Exception as exc:
            report["errors"].append(f"{filename}: {type(exc).__name__}: {exc}")
            print(f"ERROR: {report['errors'][-1]}")

    try:
        root_to_type, type_counts = load_primary_types(DATA_DIR / CELL_FILE)
        relevant_counts = {
            cell_type: type_counts[cell_type]
            for cell_type in sorted(type_counts)
            if cell_type in PILOT_TYPES or cell_type.startswith("T4")
        }
        target_ids = {
            root_id for root_id, cell_type in root_to_type.items()
            if cell_type in PILOT_TYPES or cell_type.startswith("T4")
        }
        report["cell_type_summary"] = {
            "unique_root_ids_with_primary_type": len(root_to_type),
            "counts_for_pilot_types": relevant_counts,
            "pilot_target_ids": len(target_ids),
        }
        print("\nPILOT_PRIMARY_TYPE_COUNTS: " + json.dumps(relevant_counts, ensure_ascii=False))

        connections = analyze_pilot_connections(DATA_DIR / CONNECTION_FILE, root_to_type)
        report["pilot_connection_analysis"] = connections
        print("PILOT_GROUP_PAIRS: " + json.dumps(connections["pilot_group_pairs"], ensure_ascii=False))
        print("PILOT_EXACT_TYPE_PAIRS: " + json.dumps(connections["exact_primary_type_pairs"], ensure_ascii=False))
        print("CONNECTION_ID_MAPPING: " + json.dumps({
            "rows_total": connections["connection_table_rows_total"],
            "rows_with_pre_type": connections["rows_with_pre_id_in_cell_type_table"],
            "rows_with_post_type": connections["rows_with_post_id_in_cell_type_table"],
            "rows_with_both_types": connections["rows_with_both_ids_in_cell_type_table"],
        }, ensure_ascii=False))

        coords = coordinate_coverage(DATA_DIR / COORDINATE_FILE, target_ids)
        report["coordinate_coverage"] = coords
        print("PILOT_COORDINATE_COVERAGE: " + json.dumps(coords, ensure_ascii=False))
    except Exception as exc:
        report["errors"].append(f"Pilot analysis: {type(exc).__name__}: {exc}")
        print(f"ERROR: {report['errors'][-1]}")

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nREPORT_PATH: {REPORT_PATH.as_posix()}")
    print(f"FILES_OK: {len(report['files'])}/{len(FILES)}")
    print(f"ERRORS: {len(report['errors'])}")
    return 1 if report["errors"] or len(report["files"]) != len(FILES) else 0


if __name__ == "__main__":
    raise SystemExit(main())
