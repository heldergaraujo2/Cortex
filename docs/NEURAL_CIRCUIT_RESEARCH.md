# Cortex — neural-circuit research and first executable model

## Evidence base (consulted 2026-11-10)

- FlyWire whole-brain wiring and limitations: https://www.nature.com/articles/s41586-024-07558-y
- Network statistics, neurotransmitter prediction limits, missing gap junction/neuropeptide data: https://www.nature.com/articles/s41586-024-07968-y
- Connectome-derived weighted/sign matrix, modelling assumptions: https://www.nature.com/articles/s41586-024-07982-0
- L1 → Mi1/Tm3 → T4 ON motion pathway: https://pmc.ncbi.nlm.nih.gov/articles/PMC5435463/
- T4 computation also involves Mi4/Mi9 inhibition: https://www.sciencedirect.com/science/article/pii/S0896627317301939
- Conductance-based T4 motion model: https://www.nature.com/articles/s41593-017-0046-4
- Brian2 reference implementation of STDP: https://github.com/brian-team/brian2/blob/master/examples/synapses/STDP.py

## Implemented in this branch

`cortex/experiments/spiking_circuit.py` provides a small discrete-time
leaky-integrate-and-fire neuron network with one-step synaptic transmission
delay, explicit stimulation, bounded excitatory weights, and pair-trace
spike-timing-dependent plasticity (STDP). It demonstrates the sign of weight
changes under causal vs anti-causal spike timing. The model uses **synthetic**
neurons and connectivity; the timing rule is an engineering approximation,
not a fitted fly synapse model.

Run: `python -m pytest -q tests/test_spiking_circuit.py`

## What must happen before calling this a biological circuit

1. Select a reproducible subset of FAFB v783 neurons and edges, with explicit
   root IDs, synapse counts, cell types and provenance.
2. Determine which connections are excitatory/inhibitory using supported
   neurotransmitter annotations; preserve uncertainty and missing metadata.
3. Map actual connectivity to simulator indices, keeping source edges immutable.
4. Specify time constants, neuron/synapse dynamics, stimulus encoding and
   plasticity assumptions; do not infer these from wiring alone.
5. Compare simulated motion-direction responses with published T4 data,
   including negative controls, ablations, and reproducibility.
6. Only after biological validation, investigate inter-module communication
   and long-term learning across four separate circuit instances.

**Scientific boundary:** an electron-microscopy connectome does not encode
all dynamics, neuromodulation, synaptic plasticity or developmental history.
A passing software test proves the code's defined behavior, not that the
model reproduces a fly brain or constitutes general intelligence.
