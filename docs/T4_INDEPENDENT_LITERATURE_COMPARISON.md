# T4: independent physiological literature check (2026-11-14)

**Decision: NOT BIOLOGICALLY VALIDATED.** This is an executed *qualitative literature comparison*, not a held-out quantitative validation. No calcium traces, per-animal data, preregistered anatomical p/q transform, or independently measured confidence intervals were available in this repository.

## Independent physiological reference

- Maisak et al. (2013), *A directional tuning map of Drosophila elementary motion detectors*, Nature, DOI **10.1038/nature12320**, https://www.nature.com/articles/nature12320 . In vivo GCaMP5 optical recordings establish four cardinal direction preferences and T4 selectivity for moving ON edges.
- Takemura et al. (2017), *The comprehensive connectome of a neural substrate for ‘ON’ motion detection in Drosophila*, eLife, https://elifesciences.org/articles/24394 . Summarizes T4a front-to-back, T4b back-to-front, T4c upward, T4d downward, citing Maisak et al. This is a literature-backed categorical mapping, **not** a digitized held-out physiological response dataset.
- Shinomiya et al. (2019), *Comparisons between the ON- and OFF-edge motion pathways in the Drosophila brain*, eLife, DOI **10.7554/eLife.40025**, https://doi.org/10.7554/eLife.40025 . Independently describes subtype labels and cardinal directions; this corroborates nomenclature but is not an independent physiological replicate of Maisak.

## Categorical comparison (NOT a pass)

| Subtype | Literature cardinal direction | Latest simulation preferred raw FAFB axis | Comparison |
| --- | --- | --- | --- |
| T4a | front-to-back | p_positive | UNRESOLVED: no independent coordinate transform |
| T4b | back-to-front | q_positive | UNRESOLVED: no independent coordinate transform |
| T4c | upward | p_positive | UNRESOLVED: no independent coordinate transform |
| T4d | downward | p_positive | UNRESOLVED: no independent coordinate transform |

Simulation values are from run [#43645122830](https://github.com/heldergaraujo2/Cortex/actions/runs/43645122830), commit c4660cce6230. Descriptive DSI: T4a 0.062691; T4b 0.059942; T4c 0.146457; T4d 0.047260. **These are simulated values, not measured biological DSIs.**

## Explicit gate verdicts

- Independent published *qualitative* physiological finding: **FOUND** (Maisak 2013).
- Verified FAFB p/q → visual-axis calibration: **FAIL / MISSING**. No post-hoc axis assignment permitted.
- Per-animal held-out calcium tuning curves and provenance: **FAIL / MISSING**.
- 20-seed confidence intervals and preregistered permutation test against held-out physiology: **FAIL / NOT RUN**.
- Matched subtype preferences ≥3/4 and held-out DSI >0.2 with positive 95% CI lower bound: **NOT EVALUABLE**.
- Preliminary biological validation: **FAIL / NOT ESTABLISHED**.

## Next reproducible action

Obtain independently licensed physiological data with stimulus metadata and per-animal grouping, document acquisition and checksums, freeze the coordinate transform from anatomical evidence before scoring, and only then run the protocol in [T4_BIOLOGICAL_VALIDATION_PROTOCOL.md](T4_BIOLOGICAL_VALIDATION_PROTOCOL.md). Do not enter literature categories as fake numeric response traces. Software CI success is not a biological pass.
