# T4 physiology data review gate

## Confirmed provenance
- Figshare article 5576101, DOI 10.25378/janelia.5576101.
- Acquisition workflow run 43648509472 completed successfully and uploaded artifact `gruntman-t4-physiology` (ID 14134961190, 2,839,999,011 bytes), expiring 2026-11-21.
- Successful download and archive upload do **not** demonstrate that the dataset includes held-out T4a–d response traces, stimulus directions or per-animal labels.

## Automated inventory
- `scripts/inventory_t4_gruntman.py` inventories manifest-listed files, archive entries and small text headers without extracting potentially unsafe archive paths.
- Workflow `synthetic-learning-smoke.yml` runs inventory after acquisition, publishing `data/t4/gruntman_inventory.json` in the artifact.
- The inventory is descriptive only. It does not estimate tuning curves, calibrate anatomical axes or claim biological validation.

## Required decisions after inspecting inventory
1. Confirm actual experimental modality, license, data dictionary, and per-file provenance.
2. Identify per-animal recordings, stimulus orientation/direction/time, ON-edge condition, and T4a/b/c/d subtype labels; record absent fields explicitly.
3. If those fields exist, implement a separately tested reader for the **actual** file format and produce a per-animal, per-direction held-out response table with traceable source IDs.
4. Freeze the independent FAFB p/q-to-visual-axis calibration **before** examining agreement; no post-hoc matching.
5. Run the preregistered validation protocol with uncertainty and controls; otherwise retain status `NOT BIOLOGICALLY VALIDATED`.

## Current decision
**DATA ACQUIRED; EXPERIMENTAL CONTENT UNDER REVIEW; BIOLOGICAL VALIDATION NOT ESTABLISHED.**
