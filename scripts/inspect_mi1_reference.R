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
write.csv(inventory, file.path(out_dir, "object_inventory.csv"), row.names = FALSE)

required <- c("Mi1_M10_xyz", "Mi1_neu_ind", "anno_Mi1", "anno_Mi1_DRA")
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
  anno_rows <- match(skids, as.character(anno$skid))
  m10_rows <- rep(NA_integer_, length(anno_rows))
  can_index <- !is.na(anno_rows) & anno_rows >= 1L & anno_rows <= length(idx)
  m10_rows[can_index] <- idx[anno_rows[can_index]]
  in_range <- !is.na(m10_rows) & m10_rows >= 1L & m10_rows <= nrow(xyz)
  x <- y <- z <- rep(NA_real_, length(m10_rows))
  if (any(in_range)) {
    x[in_range] <- xyz[m10_rows[in_range], 1]
    y[in_range] <- xyz[m10_rows[in_range], 2]
    z[in_range] <- xyz[m10_rows[in_range], 3]
  }
  finite_xyz <- in_range & is.finite(x) & is.finite(y) & is.finite(z)
  status <- ifelse(
    is.na(anno_rows), "skid_not_found_in_anno_Mi1",
    ifelse(!can_index, "annotation_index_out_of_range",
      ifelse(is.na(m10_rows), "missing_Mi1_neu_ind",
        ifelse(!in_range, "M10_row_out_of_range",
          ifelse(!finite_xyz, "non_finite_M10_coordinate", "mapped")))))
  data.frame(
    subset = label,
    source_row = seq_along(skids),
    skid = skids,
    anno_Mi1_row = anno_rows,
    Mi1_neu_ind_value = m10_rows,
    m10_x = x, m10_y = y, m10_z = z,
    mapping_status = status,
    stringsAsFactors = FALSE
  )
}

full_map <- build_mapping(anno, "all_anno_Mi1")
dra_map <- build_mapping(dra, "anno_Mi1_DRA")
mapping <- rbind(full_map, dra_map)
write.csv(mapping, file.path(out_dir, "mi1_skid_to_m10_mapping.csv"), row.names = FALSE)

summarize_map <- function(x) {
  data.frame(
    subset = unique(x$subset),
    records = nrow(x),
    unique_skids = length(unique(x$skid[!is.na(x$skid)])),
    duplicate_skid_records = sum(duplicated(x$skid) & !is.na(x$skid)),
    matched_annotation_rows = sum(!is.na(x$anno_Mi1_row)),
    valid_m10_rows = sum(!is.na(x$Mi1_neu_ind_value) &
                         x$Mi1_neu_ind_value >= 1L &
                         x$Mi1_neu_ind_value <= nrow(xyz)),
    finite_m10_coordinates = sum(x$mapping_status == "mapped"),
    stringsAsFactors = FALSE
  )
}
summary <- rbind(summarize_map(full_map), summarize_map(dra_map))
write.csv(summary, file.path(out_dir, "mapping_summary.csv"), row.names = FALSE)

status_lines <- c(
  "Read-only Mi1 reference inventory completed.",
  paste("neu_Mi1.RData:", neu_path),
  paste("Mi1_ind.RData:", ind_path),
  paste("Mi1_M10_xyz dimensions:", paste(dim(xyz), collapse = " x ")),
  paste("Mi1_neu_ind length:", length(idx)),
  paste("anno_Mi1 rows:", nrow(anno)),
  paste("anno_Mi1_DRA rows:", nrow(dra)),
  "",
  "Mapping summary:",
  capture.output(print(summary, row.names = FALSE)),
  "",
  "Important: this checks the authors' local index chain only. It does NOT",
  "establish a CATMAID-to-FAFB-v783 crosswalk or biological validity of every row."
)
writeLines(status_lines, file.path(out_dir, "mapping_status.txt"))
cat(paste(status_lines, collapse = "\n"), "\n")
