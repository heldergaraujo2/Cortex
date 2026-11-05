#!/usr/bin/env Rscript

# Read-only inventory for the Mi1 CATMAID -> local index -> M10 coordinate chain.
# This script does not source the authors' plotting pipeline and does not modify
# any input RData. Run it against copies of the original files.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2L) {
  stop(
    "Usage: Rscript scripts/inspect_mi1_reference.R <neu_Mi1.RData> <Mi1_ind.RData> [output_dir]",
    call. = FALSE
  )
}
neu_path <- normalizePath(args[[1]], mustWork = TRUE)
ind_path <- normalizePath(args[[2]], mustWork = TRUE)
out_dir <- if (length(args) >= 3L) args[[3]] else "phase8_mi1_inventory"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

env <- new.env(parent = baseenv())
neu_objects <- load(neu_path, envir = env)
ind_objects <- load(ind_path, envir = env)
all_objects <- unique(c(neu_objects, ind_objects))

describe_object <- function(nm) {
  x <- get(nm, envir = env, inherits = FALSE)
  d <- dim(x)
  data.frame(
    object = nm,
    class = paste(class(x), collapse = "|"),
    typeof = typeof(x),
    length = length(x),
    dimensions = if (is.null(d)) NA_character_ else paste(d, collapse = "x"),
    rownames_present = !is.null(rownames(x)),
    stringsAsFactors = FALSE
  )
}
inventory <- do.call(rbind, lapply(all_objects, describe_object))
utils::write.csv(inventory, file.path(out_dir, "object_inventory.csv"), row.names = FALSE)

required <- c("Mi1_M10_xyz", "Mi1_neu_ind", "anno_Mi1", "anno_Mi1_DRA", "Mi1_ind_DRA")
missing <- required[!vapply(required, exists, logical(1), envir = env, inherits = FALSE)]
if (length(missing)) {
  writeLines(
    c(
      "INCOMPLETE: required objects are missing.",
      paste("Missing:", paste(missing, collapse = ", ")),
      paste("Objects loaded:", paste(all_objects, collapse = ", "))
    ),
    file.path(out_dir, "mapping_status.txt")
  )
  stop(
    paste("Missing required objects:", paste(missing, collapse = ", "),
          "- inspect object_inventory.csv and load the correct source files."),
    call. = FALSE
  )
}

xyz <- as.matrix(get("Mi1_M10_xyz", envir = env))
idx <- get("Mi1_neu_ind", envir = env)
anno <- get("anno_Mi1", envir = env)
dra <- get("anno_Mi1_DRA", envir = env)
dra_reference_rows <- as.integer(get("Mi1_ind_DRA", envir = env))

if (ncol(xyz) != 3L || !is.numeric(xyz)) {
  stop("Mi1_M10_xyz is not a numeric matrix with exactly 3 columns.", call. = FALSE)
}
if (!is.data.frame(anno) || !("skid" %in% names(anno)) ||
    !is.data.frame(dra) || !("skid" %in% names(dra))) {
  stop("anno_Mi1 and anno_Mi1_DRA must be data.frames with a skid column.", call. = FALSE)
}
if (!is.atomic(idx) || is.list(idx)) {
  stop("Mi1_neu_ind is not an atomic index vector; inspect its structure manually.", call. = FALSE)
}
idx <- suppressWarnings(as.integer(idx))
if (length(idx) != nrow(anno)) {
  warning("Length of Mi1_neu_ind differs from nrow(anno_Mi1); mapping will be marked where possible.")
}

build_mapping <- function(source, label) {
  skids <- as.character(source$skid)
  anno_skids <- as.character(anno$skid)
  anno_counts <- table(anno_skids, useNA = "no")
  match_count <- as.integer(anno_counts[skids])
  match_count[is.na(match_count)] <- 0L
  anno_rows <- match(skids, anno_skids)

  # Mi1_neu_ind is NOT an anno-row -> M10-row lookup. It lists the
  # original anno_Mi1 row index represented by each row of Mi1_M10_xyz.
  # Therefore invert it: M10 row = match(anno_Mi1 row, Mi1_neu_ind).
  m10_rows <- rep(NA_integer_, length(anno_rows))
  can_match <- match_count == 1L & !is.na(anno_rows)
  m10_rows[can_match] <- match(anno_rows[can_match], idx)

  in_range <- !is.na(m10_rows) & m10_rows >= 1L & m10_rows <= nrow(xyz)
  x <- y <- z <- rep(NA_real_, length(m10_rows))
  if (any(in_range)) {
    x[in_range] <- xyz[m10_rows[in_range], 1]
    y[in_range] <- xyz[m10_rows[in_range], 2]
    z[in_range] <- xyz[m10_rows[in_range], 3]
  }
  finite_xyz <- in_range & is.finite(x) & is.finite(y) & is.finite(z)
  source_index_value <- rep(NA_integer_, length(anno_rows))
  source_index_value[can_match] <- anno_rows[can_match]
  status <- ifelse(
    match_count == 0L, "skid_not_found_in_anno_Mi1",
    ifelse(match_count > 1L, "duplicate_skid_in_anno_Mi1",
      ifelse(is.na(anno_rows), "missing_annotation_row",
        ifelse(is.na(m10_rows), "annotation_row_absent_from_Mi1_neu_ind",
          ifelse(!in_range, "M10_row_out_of_range",
            ifelse(!finite_xyz, "non_finite_M10_coordinate", "mapped"))))))
  data.frame(
    subset = label,
    source_row = seq_along(skids),
    skid = skids,
    anno_Mi1_row = anno_rows,
    anno_Mi1_skid_match_count = match_count,
    Mi1_source_index_value = source_index_value,
    Mi1_M10_row = m10_rows,
    m10_x = x, m10_y = y, m10_z = z,
    mapping_status = status,
    stringsAsFactors = FALSE
  )
}

full_map <- build_mapping(anno, "all_anno_Mi1")
dra_map <- build_mapping(dra, "anno_Mi1_DRA")
mapping <- rbind(full_map, dra_map)
utils::write.csv(mapping, file.path(out_dir, "mi1_skid_to_m10_mapping.csv"), row.names = FALSE)

# Export only rows with a verified local M10 coordinate for the later
# CATMAID -> FlyWire v783 crosswalk. The missing annotation row stays excluded.
crosswalk_input <- full_map[full_map$mapping_status == "mapped",
                            c("skid", "anno_Mi1_row", "Mi1_M10_row")]
utils::write.csv(crosswalk_input,
                 file.path(out_dir, "mi1_catmaid_skids_for_crosswalk.csv"),
                 row.names = FALSE)

summarize_map <- function(x) {
  data.frame(
    subset = unique(x$subset),
    records = nrow(x),
    unique_skids = length(unique(x$skid[!is.na(x$skid)])),
    duplicate_skid_records = sum(duplicated(x$skid) & !is.na(x$skid)),
    ambiguous_annotation_skids = sum(x$anno_Mi1_skid_match_count > 1L),
    matched_annotation_rows = sum(x$anno_Mi1_skid_match_count == 1L),
    valid_m10_rows = sum(!is.na(x$Mi1_M10_row) &
                         x$Mi1_M10_row >= 1L &
                         x$Mi1_M10_row <= nrow(xyz)),
    finite_m10_coordinates = sum(x$mapping_status == "mapped"),
    stringsAsFactors = FALSE
  )
}
summary <- rbind(summarize_map(full_map), summarize_map(dra_map))
utils::write.csv(summary, file.path(out_dir, "mapping_summary.csv"), row.names = FALSE)

dra_derived_rows <- as.integer(dra_map$Mi1_M10_row)
dra_reference_match <- identical(dra_derived_rows, dra_reference_rows)
dra_check <- data.frame(
  check = "inverse_annotation_to_M10_rows_equals_Mi1_ind_DRA",
  derived_count = length(dra_derived_rows),
  reference_count = length(dra_reference_rows),
  exact_ordered_match = dra_reference_match,
  stringsAsFactors = FALSE
)
utils::write.csv(dra_check, file.path(out_dir, "dra_index_crosscheck.csv"), row.names = FALSE)
if (!dra_reference_match) {
  warning("Inverse Mi1 annotation-to-M10 mapping does not exactly match Mi1_ind_DRA; inspect dra_index_crosscheck.csv.")
}

status_lines <- c(
  "Read-only Mi1 reference inventory completed.",
  paste("neu_Mi1.RData:", neu_path),
  paste("Mi1_ind.RData:", ind_path),
  paste("Mi1_M10_xyz dimensions:", paste(dim(xyz), collapse = " x ")),
  paste("Mi1_neu_ind length:", length(idx)),
  "Index semantics: Mi1_neu_ind lists anno_Mi1 row indices in Mi1_M10_xyz row order.",
  "Mapping uses match(anno_Mi1 row, Mi1_neu_ind), not Mi1_neu_ind[anno_Mi1 row].",
  paste("Source annotation rows without M10 coordinate:", paste(which(!(seq_len(nrow(anno)) %in% idx)), collapse=", ")),
  paste("anno_Mi1 rows:", nrow(anno)),
  paste("anno_Mi1_DRA rows:", nrow(dra)),
  paste("Mi1_ind_DRA exact ordered cross-check:", dra_reference_match),
  "",
  "Mapping summary:",
  utils::capture.output(print(summary, row.names = FALSE)),
  "",
  "The inverse mapping is cross-checked against Mi1_ind_DRA; it does not silently shift or impute indices.",
  paste("Rows in anno_Mi1 absent from Mi1_neu_ind:", paste(which(!(seq_len(nrow(anno)) %in% idx)), collapse=", ")),
  "Important: this checks the authors' local index chain only. It does NOT",
  "establish a CATMAID-to-FAFB-v783 crosswalk or biological validity of every row."
)
writeLines(status_lines, file.path(out_dir, "mapping_status.txt"))
cat(paste(status_lines, collapse = "\n"), "\n")
