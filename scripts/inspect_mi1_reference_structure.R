#!/usr/bin/env Rscript

# Read-only structural diagnostics for the authors' Mi1 reference objects.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2L) stop("Usage: Rscript scripts/inspect_mi1_reference_structure.R <neu_Mi1.RData> <Mi1_ind.RData> [output]", call.=FALSE)
neu_path <- normalizePath(args[[1]], mustWork=TRUE)
ind_path <- normalizePath(args[[2]], mustWork=TRUE)
out_dir <- if (length(args) >= 3L) args[[3]] else "phase8_mi1_structure"
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)

env <- new.env(parent=baseenv())
load(neu_path, envir=env)
load(ind_path, envir=env)
required <- c("Mi1", "anno_Mi1", "Mi1_M10_xyz", "Mi1_neu_ind",
              "Mi1_ind_PR", "Mi1_ind_noPR", "Mi1_ind_DRA", "anno_Mi1_DRA")
missing <- required[!vapply(required, exists, logical(1), envir=env, inherits=FALSE)]
if (length(missing)) stop(paste("Missing:", paste(missing, collapse=", ")), call.=FALSE)

Mi1 <- get("Mi1", env)
anno <- get("anno_Mi1", env)
xyz <- get("Mi1_M10_xyz", env)
idx <- get("Mi1_neu_ind", env)
pr <- get("Mi1_ind_PR", env)
no_pr <- get("Mi1_ind_noPR", env)
dra_ind <- get("Mi1_ind_DRA", env)
dra <- get("anno_Mi1_DRA", env)

lines <- c(
  "Mi1 reference object structure (read-only)",
  paste("Mi1 class:", paste(class(Mi1), collapse="|")),
  paste("Mi1 length:", length(Mi1)),
  paste("Mi1 names present:", !is.null(names(Mi1))),
  paste("Mi1 names first:", paste(utils::head(names(Mi1), 12), collapse=", ")),
  paste("Mi1 names last:", paste(utils::tail(names(Mi1), 12), collapse=", ")),
  paste("anno_Mi1 dimensions:", paste(dim(anno), collapse="x")),
  paste("anno_Mi1 columns:", paste(names(anno), collapse=", ")),
  paste("anno_Mi1 rownames first:", paste(utils::head(rownames(anno), 12), collapse=", ")),
  paste("anno_Mi1 rownames last:", paste(utils::tail(rownames(anno), 12), collapse=", ")),
  paste("anno_Mi1 skid first:", paste(utils::head(anno$skid, 12), collapse=", ")),
  paste("anno_Mi1 skid last:", paste(utils::tail(anno$skid, 12), collapse=", ")),
  paste("M10 dimensions:", paste(dim(xyz), collapse="x")),
  paste("M10 rownames present:", !is.null(rownames(xyz))),
  paste("Mi1_neu_ind length:", length(idx)),
  paste("Mi1_neu_ind class/type:", paste(class(idx), collapse="|"), "/", typeof(idx)),
  paste("Mi1_neu_ind range:", paste(range(idx, na.rm=TRUE), collapse="..")),
  paste("Mi1_neu_ind unique count:", length(unique(idx))),
  paste("Mi1_neu_ind duplicated values:", sum(duplicated(idx))),
  paste("Mi1_neu_ind NA count:", sum(is.na(idx))),
  paste("Mi1_neu_ind values > nrow(M10):", paste(which(!is.na(idx) & idx > nrow(xyz)), collapse=", ")),
  paste("Mi1_neu_ind tail:", paste(utils::tail(idx, 20), collapse=", ")),
  paste("Mi1_ind_PR class/length:", paste(class(pr), collapse="|"), "/", length(pr)),
  paste("Mi1_ind_PR names:", paste(names(pr), collapse=", ")),
  paste("Mi1_ind_PR element lengths:", paste(lengths(pr), collapse=", ")),
  paste("Mi1_ind_PR elements 7-8:", paste(capture.output(str(pr[7:8])), collapse=" | ")),
  paste("Mi1_ind_noPR length/range:", length(no_pr), "/", paste(range(no_pr), collapse="..")),
  paste("Mi1_ind_DRA length/range:", length(dra_ind), "/", paste(range(dra_ind), collapse="..")),
  paste("anno_Mi1_DRA rows:", nrow(dra)),
  "",
  "Last 5 anno_Mi1 rows:",
  paste(capture.output(print(utils::tail(anno, 5))), collapse="\n"),
  "",
  "All Mi1_neu_ind values:",
  paste(idx, collapse=", ")
)
writeLines(lines, file.path(out_dir, "mi1_object_structure.txt"))
cat(paste(lines, collapse="\n"), "\n")
