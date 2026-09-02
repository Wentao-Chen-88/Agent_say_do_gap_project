# BDI: The Say-Do Gap Is a Function of Deployment Conditions

A criterion-construction framework for measuring the say-do gap of tool-using agents — the divergence between what an agent says it does and what it actually does.

Paper: ICLR 2027 submission.

## Repository Contents

- `data/promise_type_v2.jsonl` — Clean dataset: 1,799 trajectories, 7 models, 3 insurance-domain scenarios
- `codebook.md` — Human annotation codebook for the L2 caliber
- `fig_gen_v8_all.py` — Figure generation script (5 figures)

## Data Format

Each line in `promise_type_v2.jsonl` is a JSON object:

| Field | Type | Description |
|-------|------|-------------|
| model | string | Model identifier |
| scenario | string | D1 (Policy Renewal), D3 (Contract Amendment), D4 (Refund Processing) |
| posture | string | CON (conservative), STD (standard), AGG (aggressive) |
| explicitness | string | L1 (core rule), L4 (full regulation chapter) |
| seed | int | Random seed |
| code | string | Tool-layer code: BV (modification), AE (escalation), AR (refusal), CS (query) |
| promise_type | string | Text-layer: direct-execution, deflect, refuse, empty |

## Key Results

- L1 deterministic upper bound: 70.8% of direct-execution texts flagged as unanchored
- L2 human-adjudicated over-promise rate: 4.65% [3.1%, 7.0%] (21/452)
- 66pp L1-L2 gap = instrument resolution
- Unverifiable layer: 27.9% — commitments that single-channel evaluation cannot name

## Running Figures

```bash
pip install matplotlib numpy
python fig_gen_v8_all.py
# Output: figures/fig1_framework.pdf through fig5_controlled_experiment.pdf
```

## Protocol Summary

The criterion-construction framework derives a say-do-gap criterion from a deployment's tool registry and business processes. It has a scenario-agnostic skeleton (traceability) and a domain-specific skin (four-step derivation procedure):

1. **Tool Registry Enumeration** — Parse the tool registry to construct action vocabulary T
2. **Business Process Extraction** — Extract SOPs to build commitment semantics
3. **Mapping Rule Instantiation** — Establish statement→action mapping (vocabulary-level + semantic-level)
4. **Alignment Window & Exemption Table** — Define turn-alignment rules and exemptions

Steps 1, 3, and 4 are fixed across scenarios. Only Step 2 requires domain knowledge.

## Citation

```bibtex
@article{chen2026saydogap,
  title={The Say-Do Gap Is a Function of Deployment Conditions:
         A Criterion-Construction Framework and a Paired, Layered Instrument},
  author={Chen, Wentao},
  year={2026},
  note={ICLR 2027 submission}
}
```