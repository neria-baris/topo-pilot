# `tools/c2_nd/nd_decide.py`

- Source: [tools/c2_nd/nd_decide.py](../../../../../tools/c2_nd/nd_decide.py)
- Kind: python
- Lines: 396

## Module docstring

> C2ND decisions: guards, the per-model rules of N-R, D (through c2_decide.r_model) and N-M,
> the rule-6 statements, variant categories, known cases, the 2-of-3 rule, endpoint statuses,
> qualifiers, licences and the union display (API.md §8, §20; protocol §4.3, §5.2, §7, §8).
> `b` is one model's {stat: {"mean", "L", "U", "rank_L", "rank_U", "g"}}; a bound inside its
> guard is neither > 0 nor < 0 (c2_decide.sign).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 11, via same directory)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 14, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 15, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `re` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 25, import)
- [tests/c2_nd/test_a_family.py](../../tests/c2_nd/test_a_family.py.md) (line 26, import)
- [tests/c2_nd/test_a_identity.py](../../tests/c2_nd/test_a_identity.py.md) (line 26, import)
- [tests/c2_nd/test_a_inference.py](../../tests/c2_nd/test_a_inference.py.md) (line 26, import)
- [tests/c2_nd/test_a_known.py](../../tests/c2_nd/test_a_known.py.md) (line 27, import)
- [tests/c2_nd/test_b_layer2.py](../../tests/c2_nd/test_b_layer2.py.md) (line 27, import)
- [tests/c2_nd/test_b_policy.py](../../tests/c2_nd/test_b_policy.py.md) (line 19, import)
- [tools/c2_nd/nd_split.py](nd_split.py.md) (line 25, import)
- [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 26, import)
- [tools/c2_nd/nd_stage_post.py](nd_stage_post.py.md) (line 23, import)
- [tools/c2_nd/nd_stage_val.py](nd_stage_val.py.md) (line 18, import)

## Top-level constants

- `CLAIM`
- `D_CAT`
- `KNOWN`
- `KNOWN_R`
- `NM_CAT`
- `NON_EXCLUDING`
- `NR_CAT`
- `Q`
- `REASON_ORDER`
- `RESOLVED`
- `T`
- `UNION_DISPLAY`
- `_ENTRY`
- `_GEN`
- `_TEXT`

## Classes and functions

- **function `_sg`** [L34-35]: `def _sg(b, stat, side) -> int`
- **function `_nec`** [L38-50]: `def _nec(b, z1, z5, w, v, suffix='') -> str` - The §2.3 table: NECESSARY, COMPLEMENT_LOW_ALIGNED, CODE_DOMINANT, NOT_NECESSARY or INC.
- **function `nr_model`** [L53-70]: `def nr_model(b, y_active) -> dict` - RESP, SPEC, category, coarse, rule-6 (a), nested, NEGATIVE_COMPLEMENT (§20 A-6).
- **function `nr_variant_category`** [L73-87]: `def nr_variant_category(b, v, primary) -> str` - The variant category on v:Zc010, v:Zc050 (c2_decide.variant_category pattern).
- **function `d_model`** [L90-95]: `def d_model(b, y_active) -> dict` - c2_decide.r_model on the DNULL arrays, DECOY_ names, rule-6 (b); y_active = Y1' active.
- **function `dnullr_category`** [L98-101]: `def dnullr_category(b, primary) -> str` - The report-only D-NULL-R category on the DNULLR: arrays (feeds DECOY_LOCATION_DEPENDENT).
- **function `nm_model`** [L104-120]: `def nm_model(b) -> dict` - RESP, ROUTED first, the four _M categories on ZMc010, ZMc050, WMc, VMc, rule-6 (c).
- **function `kc_case`** [L132-143]: `def kc_case(case, b_case, y_active) -> str` - PASS, CONTRADICTED (wins) or UNRESOLVED (ND-C17); the case's own RESP/SPEC (ND-C31).
- **function `kc_gate`** [L146-152]: `def kc_gate(results) -> dict` - KC per model: PASS/FAIL per case only (§6.7 L5); CONTRADICTED wins over UNRESOLVED.
- **function `kcr_gate`** [L155-165]: `def kcr_gate(results) -> dict` - KC-R per model (report-only): MOVE_CASE_CONTRADICTED, NOT_COMPUTED, UNRESOLVED or PASS.
- **function `_cats`** [L169-184]: `def _cats(family, gen) -> str | None`
- **function `overall`** [L190-208]: `def overall(family, statuses, cnhs, kc_contradicted=False) -> str` - §4.3 / C2 §6.5 (fatal, D: KNOWN_CASE_CONTRADICTED, CNHS, exclusions, categories).
- **function `statement_count`** [L211-213]: `def statement_count(per_model, flag) -> dict`
- **function `_family_of`** [L216-219]: `def _family_of(rec) -> str | None`
- **function `endpoint_status`** [L222-238]: `def endpoint_status(model, family, gate_history) -> str` - C2's rule with the ND names: SCORED, NOT_RUN/<gate>, SEALED_UNSCORED/<gate> (ND-C40).
- **function `qualifiers`** [L247-273]: `def qualifiers(family, per_model, extra, y_active, p1) -> list` - The qualifiers in the API.md §2 order, models ascending within each kind (ND-C19, C29).
- **function `_fill`** [L361-365]: `def _fill(text, values) -> str`
- **function `_sentence`** [L368-374]: `def _sentence(family, outcome, values) -> str`
- **function `licence`** [L377-379]: `def licence(family, outcome, values) -> str` - The §7.2-§7.4 sentence, [name] filled ("[ ]" if absent), then the family's Q-CODE.
- **function `statement_licence`** [L382-384]: `def statement_licence(kind, values) -> str` - rule6a, rule6b, rule6c (with the C2-M caveats and KM3) or nested (§7.2-§7.4).
- **function `package_statement`** [L387-390]: `def package_statement(c2_outcome, nr, d) -> str | None` - §7.5, only if C2-R USED, N-R CODE_DOMINANT (or NECESSARY) and D DECOY_NOT_USED.
- **function `c2_caveat`** [L393-396]: `def c2_caveat(d_outcome) -> str | None` - Owner default (§7.3, Q4): every C2 statement carries this until the owner decides.

