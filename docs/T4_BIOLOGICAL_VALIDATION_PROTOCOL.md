# T4 directional response: preregistered biological validation protocol (v1)

Status: **PROTOCOL ONLY — NOT BIOLOGICALLY VALIDATED**. This document fixes criteria before evaluation. The FAFB v783 connectivity is anatomical evidence, not independent physiological ground truth.

## Hypothesis and external ground truth
In the Drosophila visual system, T4 subtypes a/b/c/d have distinct preferred motion directions in the retinotopic coordinate system. **Do not equate** raw FAFB column p/q signs with anatomical directions without an independently documented coordinate transform. Acquire published or independently measured T4 directional tuning data with stimulus speed, contrast, temporal sampling, cell type and coordinate orientation. Record source, DOI, extraction method, units, uncertainty and any license limitations. Separate calibration and held-out datasets by experiment/animal, not by random time points from the same recording.

## Locked gates (all required)
1. **Numerical stability:** every trace and integrated response finite; no discarded nonfinite states; baseline response near zero (absolute tolerance 1e-9 in simulator units); response magnitude under the documented model's normalization bound; compare with and without recurrent edges.
2. **Input controls:** same active L1 population, total stimulus drive and frame count for four directions; document any unavoidable mismatch; reverse temporal order and shuffled-frame controls with 20 deterministic seeds; compare moving and static stimuli.
3. **Anatomical alignment:** preregister the p/q-to-visual-axis transform from independent anatomy before scoring preferred directions. No post-hoc relabeling to improve agreement.
4. **Direction tuning:** report each subtype's four response amplitudes, preferred direction, direction-selectivity index DSI=(Rpref-Ropp)/(Rpref+Ropp+eps), with eps=1e-12, and circular tuning where meaningful. Predeclare opposite pairs p_positive/p_negative and q_positive/q_negative. Report if all subtypes share the same winner; this alone does not pass.
5. **Reproducibility:** run at least 20 independent perturbation/control seeds, quantify bootstrap 95% confidence intervals for DSI and preference stability, and report number of independent biological samples in held-out evidence.
6. **Held-out biological comparison:** only after alignment, at least 3 of 4 subtypes must match independently measured preferred directions; each matched subtype must have held-out DSI > 0.2 and bootstrap 95% CI lower bound > 0; held-out preference agreement must exceed a predeclared shuffled-label null (permutation p < 0.05). Report all failures and multiplicity correction when testing additional hypotheses.

## Reporting and decision
A green CI run confirms software execution, **not** biological validation. Biological validation requires all gates, a verifiable independent experimental reference and a frozen model before held-out evaluation. A negative result must remain negative; do not tune on the held-out set. Thresholds above are engineering preregistration criteria, not published physiological standards. The first defensible milestone is an independent, held-out *preliminary* validation; wider generalization requires more biological data and replications.

## Current blockers
- No independently verified p/q anatomical coordinate transform.
- No held-out published T4 tuning dataset integrated into the repository.
- Simplified graph has no signed inhibition or calibrated cell physiology.
- Numerical stability after outgoing normalization has not yet been independently reviewed in result artifacts.
