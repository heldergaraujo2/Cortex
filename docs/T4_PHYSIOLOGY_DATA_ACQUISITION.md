# T4 independent physiology: verified acquisition lead (2026-11-14)

## Newly identified downloadable experimental source

Gruntman et al., **Simple integration of fast excitation and offset, delayed inhibition computes directional selectivity in Drosophila** (2018), primary paper https://pmc.ncbi.nlm.nih.gov/articles/PMC5967973/ . The paper's Data Availability section explicitly points to **https://doi.org/10.25378/janelia.5576101** as data used for primary results, and to **https://figshare.com/projects/Gruntman_et_al_2017_Data/26347** for essential analysis/simulation code.

This is a **real research-data acquisition candidate**, not a validated import. The paper includes experimentally measured T4 physiology, receptive-field and directional responses. Before use, inspect the deposited files individually for neuron subtype, animal/recording identifiers, ON-edge stimulus speed and contrast, directions, response units, license, and whether responses can be held out independently. A single subtype or pooled response cannot be extrapolated to all four T4 subtypes.

A second experimental reference: *Voltage to Calcium Transformation Enhances Direction Selectivity in Drosophila T4 Neurons*, https://pmc.ncbi.nlm.nih.gov/articles/PMC10082464/ . It explicitly records **T4c** calcium/voltage responses to gratings in 12 directions and ON edges at speeds 15, 30, 60, 120 degrees/second and contrasts 10%, 20%, 50%, 100%. This is useful for stimulus-matched **T4c** validation but cannot validate T4a/b/d alone.

## Acquisition and leakage prevention checklist

1. Fetch the deposit metadata, file manifest, per-file license, DOI and checksums. Do not assume all deposited files are unrestricted or subtype-resolved.
2. Download the smallest relevant raw response/summary files; record SHA-256 and provenance. Never invent measurements or enter paper figure labels as independent samples.
3. Confirm biological sample/animal grouping. Partition by animal or experiment **before** model calibration; freeze split and axes in a versioned manifest.
4. Check the raw data contains directional tuning for the requested subtype, motion direction, speed/contrast, and calcium/voltage units. If not, record **not evaluable**.
5. Independently determine FAFB column p/q → retinal coordinates. Anatomical subtype labels alone do not establish this transformation.
6. Only after these gates, compute 20-seed uncertainty, bootstrap CIs and held-out permutation comparison under T4_BIOLOGICAL_VALIDATION_PROTOCOL.md.

## Current evidence status

- Independent published experimental data **repository located**: YES.
- Repository dataset metadata and raw bytes downloaded/verified: NO.
- Independent FAFB p/q transform: NO.
- Per-animal held-out four-subtype quantitative evaluation: NO.
- Biological validation: **NOT ESTABLISHED**.

This document records an acquisition lead and its evidence boundary, not a biological pass.
