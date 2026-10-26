# `tools/c2_readout/c2_model.py`

- Source: [tools/c2_readout/c2_model.py](../../../../../tools/c2_readout/c2_model.py)
- Kind: python
- Lines: 282

## Module docstring

> C2 model evaluation: model loading, the three-hook pass, the readout basis Q0/M (Lemma R),
> the closed-form logits, the M0 checks, the SYMBOL-ORDER checks, X1 (ephemeral) and its
> attainability, and the site-parameterised patch wrappers (API.md §7; C2-FROZEN-v1 §2.1, §2.3,
> §2.7, §5.7, §7 rows 9, 17, 23).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 14, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../c1prime/c1_fit.py.md) (line 17, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 18, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 19, via unique basename)
- `import c1_registry_sources` -> [tools/c1prime_registry/c1_registry_sources.py](../c1prime_registry/c1_registry_sources.py.md) (line 20, via unique basename)
- `from topo_pilot.learner import forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 24, via package root)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 38, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 39, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 21)
- `torch` (lines 22)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 25, import)
- [tests/c2_readout/test_a_readout.py](../../tests/c2_readout/test_a_readout.py.md) (line 30, import)
- [tests/c2_readout/test_b_patch.py](../../tests/c2_readout/test_b_patch.py.md) (line 26, import)
- [tools/c2_nd/nd_decoy.py](../c2_nd/nd_decoy.py.md) (line 23, import)
- [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 64, import)
- [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 267, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 25, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 18, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 22, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 18, import)

## Top-level constants

- `PROTOCOL_IDS`

## Classes and functions

- **function `load_models`** [L35-48]: `def load_models() -> dict` - {model: (model64, float32 state_sha)} through c1_model.load_model64 (exact float64 cast,
- **function `_batches`** [L51-53]: `def _batches(n, batch)`
- **function `_tokens`** [L56-61]: `def _tokens(inputs) -> torch.Tensor`
- **function `_pass`** [L64-77]: `def _pass(model64, inputs, keep_logits, batch)`
- **function `activations3`** [L80-82]: `def activations3(model64, inputs, batch=1024) -> dict` - resid_post_2, resid_post_3 and ln_final_out at position 32 (float64 [n, 128]).
- **function `natural_pass`** [L85-87]: `def natural_pass(model64, inputs, policy, kind, batch=1024) -> tuple`
- **function `patched_logits`** [L90-99]: `def patched_logits(model64, inputs, site, rep, policy, kind, batch=1024) -> np.ndarray` - forward_with_patch at (site, 32) with rep [n, 128]; logits at position 32.
- **function `helmert`** [L103-111]: `def helmert(n=128) -> np.ndarray` - Orthonormal Helmert basis of 1-perp: column k has 1/sqrt(k(k+1)) in rows 1..k and
- **function `readout_basis`** [L114-136]: `def readout_basis(model64) -> dict`
- **function `readout_coords`** [L139-140]: `def readout_coords(u, basis) -> np.ndarray`
- **function `closed_logits`** [L143-145]: `def closed_logits(y, basis) -> np.ndarray` - W_U beta + M y (the stored WUbeta, so a defective beta or Q0 shows in X1).
- **function `placed`** [L148-151]: `def placed(y_hat, basis) -> np.ndarray`
- **function `identity_patch`** [L155-162]: `def identity_patch(model64, inputs, acts, policy) -> dict` - {site: patched logits bitwise equal to the natural logits} at the three sites.
- **function `_row_check`** [L165-171]: `def _row_check(z, z_closed) -> tuple`
- **function `readout_identity`** [L174-177]: `def readout_identity(z_net, y, basis) -> dict`
- **function `kappa_x1`** [L180-184]: `def kappa_x1(u, y, basis, z) -> float` - max_{i,v} S_iv / max(1, |z_i|_inf), S_iv the head-arithmetic sum of §2.7.
- **function `x1_attainable`** [L187-189]: `def x1_attainable(kappa) -> bool` - 4 * 128 * 2**-53 * kappa_X1 <= 1e-10 in exact rationals (API.md C-6).
- **function `two_route`** [L192-204]: `def two_route(d_canon, d_named, z_named, perm) -> dict` - M0 SYMBOL-ORDER two-route rule per row (T18, NEW-7).
- **function `symbol_order_a`** [L207-212]: `def symbol_order_a(named_inputs, canon32, perm) -> bool` - (a): the named input tokens are perm[w], by the independent inverse route canonical32.
- **function `symbol_order_b`** [L215-218]: `def symbol_order_b(perm) -> bool` - (b): named_from_canonical(e_c, perm) = e_{perm[c]} for every canonical c (bitwise).
- **function `symbol_order_c`** [L221-225]: `def symbol_order_c(d_canon, perm) -> bool` - (c): canonical_from_named_cols(named_from_canonical(d, perm), perm) = d (bitwise).
- **function `m0`** [L228-257]: `def m0(model64, sha, contract_j, inputs, acts, z_net, basis, d_canon, perm, policy) -> dict` - §7 row 9 in order: ids, state_sha, round trip, identity patches, rank, readout identity,
- **function `x1`** [L261-282]: `def x1(model64, arms, basis, policy) -> dict` - Closed form vs the network on every arm; arms[name] = (inputs, y_hat, z_ref, seq_ids),

