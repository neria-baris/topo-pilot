STATUS: C2ND design freeze candidate (C2ND-DESIGN-v1; MERGED v2 plus RC-13 and NEW-1 to NEW-3). Next: owner AUTH-IMPL (implementation, tests, synthetic-only dry run; ≈ 0.4 CPU-h central, 3× pause at 1.20), implementation and dry run, final freeze (`FREEZE.json` binding the C2ND-FROZEN-v1 sha256, H and the dry-run report sha256), then owner AUTH-RUN for S1–S5. Nothing here authorises a run.

# C2ND-MERGED-v2 (supersedes v1; see "Change log v1 → v2" at the end): is the circle code necessary, and can the method say "not used"? Necessity by the complement interchange (N-R at `ln_final_out`/32; N-M at `resid_post_2`/32, secondary) and an exact readout decoy (D) on the three C2 models, no training

| Field | Value |
|---|---|
| Plan id | C2ND-MERGED-v2 (writer's merge of track L and track X under the coordinator's MERGE decisions; v2 applies the result-blind review RC-1 to RC-12 and closes OPEN-1 to OPEN-3 under the coordinator's rulings) |
| Supersedes | `responses/C2ND-MERGED-v1.md`, sha256 `749760feb80a3a58a8e50fffb3e637f2df0f874cc9b796791051da0770bb2c71` |
| Review applied | `responses/coord-c2nd-review-20261026.claude-reviewer.md` (clean-context Claude reviewer; Codex frozen by owner, addendum 28), sha256 `e0fc9b608cce89023f71289d8e4f192613cbfdea53fd291bae41602865f79318`; rulings `responses/coord-c2nd-review-20261026.rulings.md`, sha256 `5a41daf0d299cb0a9b55b8736ac4b1d10cac636d8bb5d7f6a529dbb129449c2f` (every RC accepted) |
| Request | `agent-handoff/planning/requests/coord-c2-necessity-decoy-20261026.md`, sha256 `0e9c9d714636237d60f3fc50b63eb58d993e93eeb34cf803f745b8efad046b9c` |
| Base text | track L `responses/coord-c2-necessity-decoy-20261026.claude.md`, sha256 `1f30a5449ce6f7b548da649833cfabb3944b9f55b59a74d5868446494026551b` |
| Imported from | track X `responses/coord-c2-necessity-decoy-20261026.codex.md`, sha256 `aaa4d544f642ebeacf141071c849bbd00f74b3ffaf87e53f7a5fc646e731b2ca` (only what the decisions adopt) |
| Decisions applied | comparison `….COMPARISON.md` (MD-1 to MD-15, adopted as written), sha256 `20e7489284e954724deb3d57fe4eb5d140743a57d959dcfed31ce4efa6450299`; coordinator rulings R-C2ND-1 to R-C2ND-7 in `….MERGE.md`, sha256 `b3c6b91b7853c1627f98b6b17ea78e2e37713f453a31306ffe605d24037736a3` (binding; they override everything else) |
| Code base | topo-pilot main **b67f332** (`b67f3327e9220a0a17f665eec888f39859cc4096`). `tools/c2_readout/` and `src/topo_pilot/learner/` are byte-identical to C2's frozen H″ `3e234b3` (every git blob equals C2 `FREEZE.json`, §2.1). All file:line citations are at b67f332 |
| Protocol inherited | `C2-FROZEN-v2.md`, sha256 `51f78976a6d035b3e01dc2155ad66bb80cb870a4ae155cad17b6665d37f24583`; `C2-FROZEN-v2.coordinator-addendum-4.md`, sha256 `b0ea1eb2cfdd3d18abb6e81ebe7e3e8a8230c4881acb9a6d18b3c39445a23e18`. Cited below as "C2 §x" |
| Owner rules | addenda 25 (sha256 `22f130227deb091e36696a880cac6789d8b4040d2ba7aac07a7e829700cf37f4`), 26 (`23ab23f951bb4bf728c8087d1fa1340f8fe34dcc73d6b501eeb97db892edf602`), 27 (`5bbbd9ee76f537755e3dbf20fe0a459c845021a6013341d85d3e7bcd270cc948`), 28 (`650d8b6b2508280a32cadb6c512632d4103b2ac241550e7055bfa45c3377666c`; Codex frozen, reviews by clean-context Claude) |
| Arithmetic marks | **[W]** worked from recorded numbers or exact algebra; **[H]** heuristic, measured by the run before anything is decided. No [W] or [H] value is a gate |
| Authorises | Nothing. §13 gives the two owner steps (AUTH-IMPL for implementation, tests and the synthetic-only dry run on C2ND-DESIGN-v1; AUTH-RUN after the final freeze C2ND-FROZEN-v1) |

---

## Summary (≤ 300 words)

**Questions.** (N) Is the registered 6-d circle code *necessary* for the final readout's response to the ±2-cell x-history change: does the complement interchange (everything except the code taken from the other history) move little? (D) Can the frozen C2 method return NOT_USED on a model whose code is present but provably unread?

**Necessity.** At `ln_final_out`/32 the head is exactly linear, so the complement interchange carries exactly A_full − A_S: **ψ_comp ≡ 1 − ψ = ψ_Γ + ψ_rest** (Lemma N1). It is a mirror of sufficiency, not independent evidence. With ψ̂ ≈ 0.85, ψ_comp ≈ 0.15 is expected, so "necessary" (−0.10 < ψ_comp < 0.10) is not reachable for the registered complement (C2's variants: 6–9%, report-only). The expected outcome is CODE_DOMINANT: "the code is the main carrier, not the only one". A secondary family tests necessity at `resid_post_2`/32 (N-M), where the remaining computation is non-linear.

**Decoy.** Removing the code from the readout leaves θ_full ≈ 0.14 < 0.30, so a naive decoy fails the response gate in all three models [W]. The primary decoy D-NULL edits only `unembed`: W′_U = 6·W_U(I − Q₀P_SQ₀ᵀ). The code stays bitwise in the activations, its readout is exactly zero, and the remaining readout carries the response (θ′ ≈ 0.83–0.85). The gain 6 is fixed now; the measured share does not depend on it. The method re-estimates the code on a fresh split and must return NOT_USED. Constructed known cases check the method on real activations.

**Data.** New scope `c2nd-v1`; splits DFIT/DFEAS/DVAL/DTEST; a registry covering every C2 block, C2's dry-run histories and the stores of the two parallel rounds.

**Error control.** N-R and D at α = 1/300 (5 events per model), N-M at 1/360; nominal 0.05, 0.05, 0.0417; union 0.15 with C2-R, 0.29 with all six families.

**Cost.** Central ≈ 0.8 CPU-h (one test block) plus ≈ 0.4 for the synthetic dry run; pause at 3×.

---

## 1. Questions, claims, competing explanations, prior expectation, scope

### 1.1 Questions
- **Q-N (necessity).** For each model j and the C2 natural counterfactual pairs (H⁺, H⁻) (±2-cell x-history rotation, w32 kept), what fraction of the model's signed oracle-aligned response does the **complement interchange** carry? The complement interchange sets every readout coordinate except the registered code to the counterfactual's value and holds the code. Secondary (N-M): the same question at `resid_post_2`/32, where the remaining computation is non-linear.
- **Q-D (discrimination).** Take a model built so that the registered code is present at the readout site (identical activations, so every activation-only gate passes), the readout provably does not read it, and the model still responds to the counterfactual. Does the frozen C2 recipe, re-estimating the code on fresh data, return NOT_USED?

### 1.2 Claims sought
- N-R: a per-model category on ψ_comp against the owner's 0.10 and 0.50 lines, 2 of 3 models, with Q-CODE; a registered "positive but below margin" statement (rule 6).
- D: DECOY_NOT_USED in 2 of 3 models with Q-CODE-D, with the constructed known cases passing at validation; a registered "positive but below margin" statement for the decoy (rule 6).
- N-M (secondary, owner Q2): a per-model category on ψ_M,comp at layer 2; a registered "positive but below margin" statement for the layer-2 complement (rule 6 (c)).

### 1.3 Competing explanations and what separates them

| Explanation | Observation that separates it | What it cannot separate |
|---|---|---|
| E-sole: the code is the only carrier of the readout's aligned response | NECESSARY: −0.10 < ψ_comp < 0.10 and complement energy < 0.10 | redundancy outside the linear code (Q-CODE) |
| E-dominant: the code carries most, other directions the rest | CODE_DOMINANT: 0.10 < ψ_comp < 0.50 | what carries the rest (`STRONGER_EVIDENCE_OPTIONS_HE.md` §2.2, out of scope) |
| E-proj: the size of the remainder depends on how "everything except the code" is defined (C2 §1.3) | the report-only variant categories on the R_E, R_K1, R_K2 complements and the qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR (§2.3) | which complement definition is "right" (none is chosen) |
| E-redundant: other directions alone carry most | NOT_NECESSARY: ψ_comp > 0.50. At the readout this contradicts C2's ψ > 0.5 (Lemma N1) | — |
| E-opposed: the complement acts against the response | NEGATIVE_COMPLEMENT qualifier; a large negative complement is never "little" (the lower bound in NECESSARY) | — |
| E-interact (layer 2 only): code and complement act jointly through block 3 | ι_M = 1 − ψ_M − ψ_M,comp reported; categories on ψ_M,comp | block-3 processing versus the residual skip (C2 RC-6) |
| E-method-yes: the recipe returns USED whenever a history-sensitive code is present and the model responds | D-NULL returns USED or PARTIAL (false positive) | — |
| E-method-ok: the recipe follows what the readout reads | D-NULL NOT_USED; D0 USED; D-ONLY USED and NECESSARY; D-DOSE PARTIAL | every non-use not represented by a decoy (Q-CODE-D) |
| E-estimation: a re-estimated projector leaks a spurious share | the leak share of D-NULL (§2.8; magnified by ψ/(1 − ψ)), the blind S2 diagnostic κ_leak and DECOY_POSITIVE_BELOW_MARGIN | — |
| E-LN: the code acts through LayerNorm statistics | at the readout the interchange is post-LN (no channel, Lemma N1); at layer 2 the LN-scale ratios and fixture KM3 (§5.1); the decoy's upstream LN channel is stated in Q-CODE-D (§7.1) | LN-scale use of the upstream code at `resid_post_3` (not a C2 estimand) |

### 1.4 Prior expectation (stated now; the planners have read C2's opened values)
The C2 TEST and VAL values are opened (job 0115). Hence: ψ_comp ≈ 0.149 / 0.146 / 0.144 (1 − ψ̂, C2 TEST) [W]; ψ_M,C ≈ 0.141 / 0.144 / 0.140 and ι_M ≈ 0.020 / 0.012 / 0.013 (C2 descriptive, TEST) [W]. **Expected:** N-R CODE_DOMINANT, N-M CODE_DOMINANT_M, D DECOY_NOT_USED, every known case as constructed. A confirmation is reported as confirming the expectation, not as a discovery. The thresholds 0.10 / 0.50 / 0.30 are C2's owner-approved values, unchanged. Only the decoy design constants g_D = 6 and ρ = 0.92 were set with the opened values. They are disclosed (§2.6, R-C2ND-1), they are construction constants, and they are fixed before any C2ND data exist. C2's registered variants give, on C2 TEST, 1 − ψ = 0.093/0.077/0.072 (R_E, Euclidean complement), 0.062/0.059/0.057 (R_K1), 0.156/0.150/0.158 (R_K2) [W]. The ≈ 0.15 remainder is a property of the registered K = 3 GLS complement, not of the code alone. Expected: PROJECTOR_DEPENDENT_NR and HARMONIC_DEPENDENT_NR(K = 1) in all three models.

### 1.5 What the package can and cannot add (honest scope)
- **Necessity at the readout is a mirror of sufficiency.** Under exact linearity the two directions of the interchange are one number. A fresh N-R run replicates ψ on new rows, tests it against the thresholds 0.90 and 0.50 (Lemma N1(iii)), and adds an energy conjunct and a lower bound. It cannot turn "sufficient" into "sufficient and necessary". The 0.145 remainder decides the expected outcome.
- **The decoy is a specificity check of the recipe under real activations and real estimation noise.** Its answer is known by construction, so NOT_USED is expected; its sampling margin is large, but the refit leak is not bounded in advance (§2.8, §4.6). It shows the method *can* say no and does not manufacture a share from an unread code. It does not show that C2's USED excludes every alternative mechanism, or that NOT_USED on a natural model would be right.
- **Layer 2 is where necessity is non-trivial.** N-M measures a non-linear complement effect. Its known cases are synthetic only (§5.1): no exact real-model construction with a known layer-2 answer exists.

### 1.6 Scope
The three C2 models (cylinder-O 1729, 2718, 3141, step 5000; C2 §0, §4); position 32; the C2 donors (x pair H⁺/H⁻; y placebo H^Y); the C2 frozen FIT projectors (R at `ln_final_out`, M at `resid_post_2`) and frozen eligibility constants; the natural cylinder-O process (overlap, σ = 1.25). No training, no site search, no new chart. Not in scope: C2-S* on the decoys, other positions, other donors, the decomposition of the 0.145 remainder, the w31 separation (C2 MD 9). C2's verdicts are never reopened by any C2ND outcome (§12).

---

## 2. Design

### 2.1 Models, sites and reused frozen artefacts (R-C2ND-5: full values from manifests, stage records and writer code; no array opened)
Every value below is copied into the C2ND `CONTRACT.json` and checked by G0 (§3 row 1) before and after every job. The C2 store `X:/Downloads/projects/topo-pilot/c2-readout-store` is read-only for C2ND.

**Models** (C2 `CONTRACT.json` "models"; float32 `c1_model.state_sha`, not file hashes):

| Model | checkpoint id | EmissionSpec | state_sha_f32 |
|---|---|---|---|
| 1729 | `c3358e3cb9c352fb` | `3633ac27dab50cf4` | `062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8` |
| 2718 | `98b0e703a337d513` | `97838b9e13a26f74` | `501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c` |
| 3141 | `036b670743ffbbaf` | `8c29c329c197c79e` | `197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8` |

**C2 store artefacts** (sha256 from `manifests/0115.json`, the accepted final manifest; the FIT/DEC/ORACLE_FROZEN values are identical in `manifests/0112.json`):

| Path (under `c2-readout-store/`) | sha256 | Use in C2ND |
|---|---|---|
| `fits/FIT_1729.npz` | `0ae758e84c41b6b9cd157b8e699674fe07996c7f60fa310e1aa878a4286c7326` | frozen projectors and readout basis |
| `fits/FIT_2718.npz` | `ca44b5ad681fe927d045afedf8efd8facd8e0efc312e04aff060160b172840f2` | same |
| `fits/FIT_3141.npz` | `51ac9332982f6123dda7a5e7eb1c7bddc6ba902094b3ad5505bbbe8f66fc408a` | same |
| `fits/FIT_1729.json` | `989a97c810411364ca9e7ccf670a86c2ecee6c0dbd88cf26afa2b481fa289784` | status, δ_P |
| `fits/FIT_2718.json` | `8a3b94af7335599ef85a6aa0ccc42a54710bb7a66c5dc38309ee0164e2585d3d` | same |
| `fits/FIT_3141.json` | `08395b4904d53efaa6ecf27b17d913e132b6a5162f1a7dd5a20f1758ffacd21a` | same |
| `fits/DEC_1729.npz` | `531d3d9c4d6f110900a26b35fb368c002c34f562d69644bd919aa6588b1ab6ee` | frozen C2 decoders (N-R and N-M validity on new rows) |
| `fits/DEC_2718.npz` | `9606a0e1e8de929eabd104e709a00993276d8f75baa065b83f0c5154051fcd36` | same |
| `fits/DEC_3141.npz` | `3392295e6e3bca6d5c4458816a3ebd00a77858c6bc415ebdb85a1fcf9d129b68` | same |
| `oracle/ORACLE_FROZEN.json` | `8ce019086884bb9812d2705415b41c8a0fcf15b749c1cf2c9e133d285336045e` | s_max = 7.34032133381897, κ_m = 4.7527e-4, κ_ν = 8.6243e-3, y_active = true |
| `hist/HIST_fit_b0.npz` | `c9f6567371d9ff65a668224597edc1c6be687fac9b5cb943b41d6eee8c243873` | registry only (digest columns, R-C2ND-6) |
| `hist/HIST_fit_b1.npz` | `740513e7ed528d5202531d0de1df80651d27ea2da06d3b998de11936d6e28592` | same |
| `hist/HIST_feas_b0.npz` | `7162e158a264c7966b7074f66c05a5b580fe2307918873c3d3f595446ba6c943` | same |
| `hist/HIST_val_b0.npz` | `0282719ad6bc87a7fc1a5c491a768d4c6923bba59936bce0bb494ef28dc077dd` | same |
| `hist/HIST_test_b0.npz` | `3c776f58f267da281672a00c5027253d36803d9a3a5f8db16afd6ab0ea68d0f0` | same (the opened C2 TEST block) |
| `stages/S5/report.json` | `2daeb7bb340856955c502163a69666e861cb746ebcf38d3486a31cdf2e139ff2` | the bound C2 outcome (for §7.5 and S13) |
| `manifests/0115.json` | `0ca8148bd0c781613694ab0825e929de90469be31b48f61cbbd41e5c58592d43` | final C2 manifest (equals `manifest_sha256` in `0115.accepted.json`) |
| `manifests/0115.accepted.json` | `e0ee1039978eaf921cbd13aebd82799c555163da6eda64073e676ecba3f88410` | C2 ACCEPT record (review `jobs/0115/review.md`, sha256 `9425b0a7da620680d679ddb80eb422a0c677a5d4aceb22757574fd6397f90327`) |
| `FREEZE.json` | `31df0efa430c7b8b77aed145cb5759ed2f463fe3e1eadee4c9d2a96ce2e11684` | C2 freeze record (H″, blobs) |
| `CHART_CONSTRUCTIONS.json` | `e5be845ebaae6cc6e4005e8c2dc43fcd46d211bfad46aca548f5ee8d33d7a98a` | lineage only |

**Other inherited bindings** (C2 `CONTRACT.json` "hashes", sha256 `3d4b9f6257b886a0edc40feb499513fe0d0cae0af5c031f76b0988750fe7445a`): the C1′ production charts `c1prime-store/CHART_1729_production.npz` `6154af0ee1a5ad01d378b507272365d1f0e797b4a843835d7dc09525d5c9cc71`, `CHART_2718_production.npz` `6a5d8c1cbe4aea9909b85aff258a31d2dfdfb8d12c1f93f33a79b245d69370da`, `CHART_3141_production.npz` `ce0c0192d243ff9e8fa4ddc6b07750db31a637ff059a4e8cc55535b8dd21cf2d`; the K4 FREEZE `x4-circle-history-feas-store-0015/FREEZE.json` `e3049feedf0fadfb004c9422effe560af031addb846a7b8d1c1bffd52ce3c94a`; `tools/c1prime/CONTRACT.json` `f8df2e43bc24a3e992ce4323a8577ec4a7e2657a4e00bdf3ff0323b909a7a379`; the c1prime registry v1 `ebcebe186103d7a4ed01d8f011c05742419f9f418af03775549a80d0d5c77d9e`; every entry of C2 `CONTRACT.json` "reused_blobs" and "reused_extra" (copied into the C2ND CONTRACT unchanged; e.g. `src/topo_pilot/learner/model.py` `ee1c124ce83da147ccc2a4b4c0be167de902d61ecd00ead5748b8566f62ae039`, `patch.py` `64d742e85ddba3d121a5c72af0abaef910c9b986a03a7b87caa26c4c20dd0ad4`).

**Frozen C2 code** (`tools/c2_readout/` at H″ `3e234b38077f84ddebfa380120938b8847f40e03`; git blob = sha1 of the blob, sha256 from C2 `FREEZE.json` "modules"; the C2ND code head must hold the same blobs, "never retrofit a frozen implementation"):

| File | git blob (b67f332 = H″) | sha256 |
|---|---|---|
| `c2_attrib.py` | `bb7c297b221fcd8e7f2f3a8dab97fa326de5615e` | `882bf534c4898f16e595552edb7cde6db4a9f7682bed537917df206b64861ca8` |
| `c2_code.py` | `a488d3858b19824903adb9c0e32f94dfadeaeadd` | `fa5b42a4e0187bc24990a368319fa22cde9a777339a75dcaa5aef34022ff5f0a` |
| `c2_config.py` | `4e3cc56fcc0af1f29fa27a3147488540804e41a1` | `d721d0f36d6bd46cdbf337fbf26f60aab11b4c11524d9e2d3e2b83ff7731a2b4` |
| `c2_data.py` | `fb94311d89fc14c2041e3c88981d68e22a9f787c` | `5b97f8b8112cf7587c0be12eecacf259730c9c904f53f810ad111a5c4612c2a0` |
| `c2_decide.py` | `1b0422fa3c1b78f920852843bc70d304509ec5ec` | `bb1b3652015d77c553afedafd984dfd00c97da37832a2efe5e659271521d9906` |
| `c2_driver.py` | `a90ae40575df8ef001fdecfc68cebb9186a8a746` | `1a092c67181b388e173b2ff8e499cbe3fe2d9415c64bca15119b192c56bb8908` |
| `c2_model.py` | `9f77f5ea7e066a430cdb71a4a4a44c32d5f6e5f9` | `6cbfb0cab730a5b8411a95a5e656fec953550f3962feede0be948b90f5f1e91d` |
| `c2_oracle.py` | `87bebc9634216d547da3a4a28ef0103b0a7bca6e` | `b22496b4bbbcf5595eebce95604f63532d991556717e13e2a2875a2f8fa631f7` |
| `c2_registry.py` | `6dea71249acbefdfcadaf41408b7a125f3d650d5` | `14f221d0484b61c0ebc76d910ade5c6e377cc864ccf3ab1973fbc450e1bafd56` |
| `c2_stage_base.py` | `cedefb9b75af62766e4e4543647d96f55ef8eea3` | `0dee985930dc08faf55d4b3842b7e1ac0db49e808e2251742c62dcc8e47f951b` |
| `c2_stage_post.py` | `3c5358004f6536a62274922d7e7355ee7894a3e9` | `a7f267b0868e32c23334f86565b587ef9774abf23a9ded98b6473cbdb1d4fd9e` |
| `c2_stage_pre.py` | `9f9d37e22de95fa40b2c9c1d86613a1ff41432c2` | `e89e210d6165f0ca3f8f522c808b338562084e72d90749522a8f2909772893ae` |
| `c2_stage_val.py` | `468e8292457fc6ce18044c30b6d68532287e3122` | `a5a73dae7998367ae74adf60210e2ceb5ef138a3b0e70a34212a57ac98ecae69` |
| `c2_stats.py` | `449992ec54fdfff2f66400cee1bab1ff7930bb8a` | `1090bf1899f34fd2a04c0f6d0c33e92ee20ac49024899a2cf1cde38fc8c1fcf7` |
| `API.md` | `43fc92e6700481775df7c4c323ade7be813a3887` | `cabd745d12e7ceb75ad1b3ac7ed20aee85c99960af4f928217c2a109c1ba3f58` |
| `CONTRACT.json` | `81651f897501ba51ef0c51003b54bbf2e6bcf1a0` | `3d4b9f6257b886a0edc40feb499513fe0d0cae0af5c031f76b0988750fe7445a` |
| `PROTOCOL_C2_v2.md` | `4990e5650e916f2eb91f6777829ec2b815dbddcf` | `51f78976a6d035b3e01dc2155ad66bb80cb870a4ae155cad17b6665d37f24583` |
| `TEST_PLAN.md` | `3cdace9da696a813712e211e5bbe5a1b9ea04ecb` | `8cf2572c6132fe7fef19a7f840af60971b6cc9b7f1c7f8fa80877ce285ab1afe` |

**Fit-file key names (from the writer code, not from the arrays).** `c2_stage_pre.f1_model` (lines 162–204) writes `fits/FIT_{j}.npz` with:
- the readout basis `Q0`, `M`, `beta`, `gamma`, `WU`, `WUbeta` (`BASIS`, `c2_stage_base.py` line 36; values from `c2_model.readout_basis`, lines 114–136);
- `zt_mu`, `zt_sd` (nuisance standardisation), `J` (`c2_attrib.null_projector(M)`), `aff_w`, `aff_nu`, `n2_mu`, `n2_W`, `n2_q99` (lines 170–172);
- for each problem p ∈ (`R`, `R_K1`, `R_K2`, `R_E`, `M`, `S*`) (`c2_config.PROBLEMS`, line 113): `{p}_alpha`, `{p}_Gamma`, `{p}_B` (`FP`, line 36), `{p}_L`, `{p}_P_S`, `{p}_P_G` (line 189), `{p}_Sigma` for p ≠ `R_E` (line 190), `{p}_mtilde` (line 192).

C2ND uses `R_P_S`, `R_P_G`, `R_L`, `R_B`, `R_Gamma`, `R_alpha`, `R_Sigma`, `R_mtilde` and the basis keys (N-R, D), the variant keys `{v}_P_S`, `{v}_L`, `{v}_B` for v ∈ {`R_E`, `R_K1`, `R_K2`} (the report-only N-R variant arrays, §4.2; their δ_P(v) from `FIT_j.json` "delta"), and `M_P_S`, `M_L`, `M_B`, `M_mtilde` (N-M). L_B is `R_L[5:]` (`c2_stage_base.prob`, lines 216–222; 5 nuisance rows first). `fits/FIT_{j}.json` holds `status`, `values`, `delta` (δ_P per problem) and `n2`. All six problems have status PASS and `n2` PASS in all three models. The recorded δ_P(R) is 3.3214e-12 / 2.7962e-12 / 3.0949e-12, and δ_P(M) is 8.2892e-12 / 6.9914e-12 / 7.7924e-12. `fits/DEC_{j}.npz` keys are `{F}_{k}_{x}` with F ∈ (`R`, `M`, `Sstar`) (`c2_config.FILE_FAMILY`, line 115), k ∈ (`D0`, `Dcode`, `Dlin`) (`c2_stats.KINDS`, line 382) and x ∈ (`mu_F`, `s_F`, `W`, `b`, `lam`, `eq`, `tol`, `kappa`) (`c2_stats.FIELDS`, line 231). The presence of these keys follows from the writer code and the PASS statuses; G0 confirms it structurally at execution (§3 row 1).

**Sites.** N-R and D at `ln_final_out`, position index 32 (127 readout coordinates). N-M at `resid_post_2`, position 32 (128 coordinates), secondary (R-C2ND-7; owner Q2).

### 2.2 Notation (C2 §0 unchanged)
y ∈ ℝ¹²⁷: readout coordinates at `ln_final_out`/32, y = Q₀ᵀ(u − β). M = W_UQ₀ (36 × 127, named output order). C = I₃₆ − 11ᵀ/36. d = d_named = q̄(H⁺) − q̄(H⁻). Δy = y(H⁺) − y(H⁻). P_S = BL_B, P_Γ = ΓL_Γ, P_rest = I − P_S − P_Γ (the frozen oblique GLS projectors of model j). A_full = ½dᵀMΔy, A_S = ½dᵀMP_SΔy, A_Γ, A_rest as C2 §2.6; e_full = ‖CMΔy‖², e_S = ‖CMP_SΔy‖² (C2 §2.9); G = ½Σ_v d_v(log q̄¹_v − log q̄²_v), the oracle contrast. a₂ = `resid_post_2`[:, 32]; P₂ the frozen C2 M projector (`M_P_S`). E_x, E_y the C2 eligibility with frozen s_max; 1_E the indicator form (C2 §6.1). K := ker(CM) ⊂ ℝ¹²⁷ (readout-null coordinates; dim K = 127 − rank(CM) ≥ 92), J the Euclidean projector onto K (`c2_attrib.null_projector`, lines 96–101). ker(M) ⊂ K, dim ker(M) ≥ 91. Π_S := Q₀P_SQ₀ᵀ (128 × 128). **g_D = 6** is the decoy gain (R-C2ND-1's g). The numerical guard is g_s (§4.4). Bounds: L(s), U(s) are the lower and upper family bounds of mean(s); "L(s) > 0" means L(s) > g_s, and "U(s) < 0" means U(s) < −g_s (C2 §6.4 rule 3).

### 2.3 Intervention 1: necessity at the readout (family N-R, primary of C2ND)
**Complement interchange.** For a pair (1, 2) = (H⁺, H⁻):

  y_C^{2←1} := y² + (I − P_S)Δy  (arm 2 receives arm 1's complement, i.e. its Γ-coordinates and P_rest part; the code is held at arm 2's value),

  A_comp := ½dᵀ(z(y_C^{2←1}) − z(y²)),  e_comp := ‖C(z(y_C^{2←1}) − z(y²))‖² = ‖CM(I − P_S)Δy‖².

The complement includes the nuisance directions Γ: it is everything except the code, not only P_rest. It is placed at `ln_final_out`/32 through `forward_with_patch` with the replacement β + Q₀y_C (C2 Lemma R(iv)). The frozen C2 projector P_S is used (no refit for N-R; R-C2ND-2 applies to the decoys only), so the C2 code definition is unchanged.

**Lemma N1 (the readout identity).** (i) y_C^{2←1} = y¹ − P_SΔy = y_S^{1←2}, the reverse C2 interchange (C2 Lemma D1(ii)). (ii) A_comp = ½dᵀM(I − P_S)Δy = A_Γ + A_rest = A_full − A_S exactly, for every row and any oblique P_S (only P_S² = P_S is used). (iii) Hence ψ_comp := E[A_comp | E_x]/E[A_full | E_x] = 1 − ψ = ψ_Γ + ψ_rest. For every c, Zc^c := (A_comp − c·A_full)1_E = −(A_S − (1 − c)A_full)1_E = −Z^{1−c}, a sign flip of a C2 contrast. (iv) With symmetric percentile ranks (67 and 19,934 of 20,000 at α = 1/300: 67 + 19,934 = 20,001), L(−X) = −U(X) on the same index stream, so every N-R bound is a C2-type bound at the mirrored threshold.
*Proof.* (i) y² + Δy − P_SΔy = y¹ − P_SΔy. (ii) C2 Lemma R(iii)–(iv): z(ŷ) − z(y²) = M(ŷ − y²) for any ŷ; the patched normalised vector need not lie on the LayerNorm image, because only the bias-free linear head reads it (`model.py` lines 92–93, 122–126; `patch.py` lines 111–117, no second LayerNorm). Then P_S + P_Γ + P_rest = I. (iii) Linearity of expectation. (iv) The k-th smallest of −X over the draws is −(the (n + 1 − k)-th smallest of X). ∎

**Consequences, stated plainly.**
- "Necessary" at the 0.10 line (ψ_comp < 0.10) is the statement ψ > 0.90. "The complement carries less than half" (ψ_comp < 0.50) is ψ > 0.50, which C2 already licensed (USED).
- **What the 0.145 remainder implies.** ψ_comp ≈ ψ_Γ + ψ_rest = 0.0018 + 0.1475 = 0.1494 (1729), 0.1461 (2718), 0.1443 (3141) on C2 TEST [W]. NECESSARY needs the fresh ψ to exceed 0.90. C2's bounds make that implausible (its TEST Z050 and Z010 intervals give ψ ∈ ≈ [0.84, 0.86], descriptively). The expected and only plausible positive licence is CODE_DOMINANT. This holds for the registered K = 3 GLS complement only: C2's registered variants put 1 − ψ at 0.06–0.09 (R_E, R_K1; §1.4), so the remainder's size depends on the complement definition (report-only variant categories below).
- **Energy is not additive.** e_full = e_S + e_comp + 2⟨CMP_SΔy, CM(I − P_S)Δy⟩, so η_comp := E[e_comp]/E[e_full] is not 1 − η_S. The cross term is reported. Only the Minkowski bound (1 − √η_S)² ≤ η_comp follows; with η_S ≈ 0.905, η_comp ≥ 0.0024 [W]. Its value is unknown [H]; it enters NECESSARY as a conjunct.
- **No LayerNorm channel.** The interchange acts after `ln_final`; σ(a) is that of the natural arm. The complement coordinates do contain the LN rescaling caused by the upstream history change, including the code's own contribution to σ. §2.9 reports that part descriptively. It is part of "everything except the code at the readout", the registered estimand.
- **Negative complement.** ψ_comp can be negative (if ψ > 1). A large negative complement is not "little response". So NECESSARY carries a two-sided condition (track X): ψ_comp > −0.10, through Wc := (A_comp + 0.10·A_full)1_E with L(Wc) > 0. Qualifier NEGATIVE_COMPLEMENT(j) iff U(NEGc) < 0, NEGc := A_comp·1_E (outside the error allocation, as C2's NEGATIVE_ALIGNED_CONTRIBUTION).
- **Direct and by subtraction.** A_comp is computed both directly (the patched complement arm, gate X1) and as A_full − A_S (closed form). They must agree within the X1 tolerance (§3 row 19).

**Per-model N-R categories** (declared only with RESP_j and (SPEC_j or Y1 inactive), as C2 §6.3; Vc := (e_comp − 0.10·e_full)1_E):

| Category | Declared iff | Truth claimed |
|---|---|---|
| NECESSARY_j | U(Zc010) < 0, U(Zc050) < 0, L(Wc) > 0, U(Vc) < 0 | −0.10 < ψ_comp < 0.10 and η_comp < 0.10 |
| COMPLEMENT_LOW_ALIGNED_j | U(Zc010) < 0, U(Zc050) < 0, and NECESSARY_j not declared | ψ_comp < 0.10 (it may be negative; energy not bounded or lower bound not shown) |
| CODE_DOMINANT_j | L(Zc010) > 0 and U(Zc050) < 0 | 0.10 < ψ_comp < 0.50 |
| NOT_NECESSARY_j | L(Zc050) > 0 and L(Zc010) > 0 | ψ_comp > 0.50 |
| INC_j (INC_j/NUMERICAL if a guard hit left it undeclared) | otherwise | — |

The four categories are mutually exclusive. **Coarse statements** (as C2 §3.1, same prerequisites): "ψ_comp > 0.10" iff L(Zc010) > 0; "ψ_comp < 0.50" iff U(Zc050) < 0.

**Variant categories (report-only):** the CODE_DOMINANT / NOT_NECESSARY / COMPLEMENT_LOW_ALIGNED rule on v:Zc010, v:Zc050 with the primary RESP/SPEC prerequisites (`c2_decide.variant_category` pattern). Qualifiers PROJECTOR_DEPENDENT_NR(j) iff the R_E category ≠ the primary; HARMONIC_DEPENDENT_NR(j, K) iff the R_K{K} category ≠ the primary. (The variant arrays are defined in §4.2; they are outside Lemma FW-ND, as C2 §6.3 remark 6.)

**Rule-6 statement (a), COMPLEMENT_POSITIVE_BELOW_MARGIN_j** (owner addendum 25 rule 6; R-C2ND-4): declared iff L(NEGc) > 0, U(Zc010) < 0 and U(Zc050) < 0, with the same prerequisites. Truth claimed: 0 < ψ_comp < 0.10. It is reported beside NECESSARY or COMPLEMENT_LOW_ALIGNED. **CODE_DOMINANT is not the rule-6 licence**: it is an intermediate category above the margin (track L's label corrected).

**Unexpected-case entry (track X's native rule-6 statement), CODE_SHARE_POSITIVE_BELOW_MARGIN_j:** declared iff NOT_NECESSARY_j is declared, L(Zc090) > 0 and U(Zc100) < 0, where Zc090 := (A_comp − 0.90·A_full)1_E = −Z^{0.10} and Zc100 := (A_comp − A_full)1_E = −A_S·1_E. Truth claimed: 0 < ψ < 0.10, i.e. the native code share is certified positive but below the margin. Nesting it inside NOT_NECESSARY makes it cost no error event (§8.1).

**No random-reference energy conjunct.** The matched reference for a 121-dimensional complement is a random 121-plane, whose expected share 121/127 makes such a bound vacuous. The single absolute conjunct 0.10 is the owner's "little in any direction" level (C2 §2.9 item 3).

### 2.4 Intervention 2: necessity at layer 2 (family N-M; `resid_post_2`/32 included as a secondary family, R-C2ND-7, pending owner Q2)
The C2-M interventions are reused verbatim (C2 §2.10; `c2_attrib.cm_replacements`, lines 191–194). In the source context H, with donor states a₂(H±):
- F: r± = a₂(H±); S: r± = a₂(H) + P₂(a₂(H±) − a₂(H)); **C (complement): r± = a₂(H) + (I − P₂)(a₂(H±) − a₂(H))**.

Per row (`c2_attrib.cm_quantities`, lines 197–205): A_M,X = ½dᵀ(z_X⁺ − z_X⁻), e_M,X = ‖C(z_X⁺ − z_X⁻)‖², X ∈ {F, S, C}; I_M = A_M,F − A_M,S − A_M,C.

**Estimands.** τ_M = E[A_M,F]/E[A_full] (transmission; prerequisite). **ψ_M,comp := E[A_M,C | E_x]/E[A_M,F | E_x]** (primary N-M share). η_M,C := E[e_M,C]/E[e_M,F]. ι_M := E[I_M]/E[A_M,F] = 1 − ψ_M − ψ_M,comp (reported, descriptive).

**Why it is not a mirror.** Block 3 evaluates the patched state. ln1 and ln2 normalise it (the complement changes the row norm and mean). Attention at position 32 reads the patched query, key and value against H's unpatched prefix. The MLP is GELU, followed by the residual skip, `ln_final` and the head. So A_M,S + A_M,C ≠ A_M,F in general, and ψ_M,comp is a separate measurement. There is no identity ψ_M,comp = 1 − ψ_M. **LayerNorm statistics:** a complement that changes ‖a₂ − ā₂1‖ rescales every coordinate, the code's included, inside block 3 and at `ln_final`. This is the "code read through LN statistics" channel at this site. It is part of the registered intervention and is not removed. The per-row scale ratios √(Var(r) + ε)/√(Var(a₂(H)) + ε) for the S and C states (`c2_attrib.ln_scale_ratio`, lines 215–217) are reported, and fixture KM3 (§5.1) shows the channel on a known case. Every C2-M caveat carries over (C2 §3.2: the skip is part of every effect; the interchanged state is not natural; N2 is a radial support screen only; position 32 only; self-repair can lower τ_M).

**Per-model N-M rules** (C2 §6.4 M order): RESP_j (V3x in the N-M stream). ROUTED_j iff U(Ztau) < 0, Ztau := (A_M,F − 0.10·A_full)1_E; no share is then attributed. Else, if L(Ztau) > 0, the categories of §2.3 with ZMc^c := (A_M,C − c·A_M,F)1_E, WMc := (A_M,C + 0.10·A_M,F)1_E and VMc := (e_M,C − 0.10·e_M,F)1_E: NECESSARY_M_j (U(ZMc010) < 0, U(ZMc050) < 0, L(WMc) > 0, U(VMc) < 0), COMPLEMENT_LOW_ALIGNED_M_j, CODE_DOMINANT_M_j, NOT_NECESSARY_M_j. Else INC_j. There is no placebo statement: the C2 Y2 placebo tests y-information in the code, which is not a necessity question. **Rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN_j:** declared iff L(Ztau) > 0, L(NEGMc) > 0, U(ZMc010) < 0 and U(ZMc050) < 0, with RESP. Truth claimed: 0 < ψ_M,comp < 0.10. Reported beside NECESSARY_M or COMPLEMENT_LOW_ALIGNED_M; it uses the existing NEGMc array.

**If the owner declines N-M (Q2),** this section is replaced by track X's text, unchanged in substance: "`resid_post_2`/32 is not included in the new confirmatory endpoint. Its construction would be r_C^± = a₂(H) + (I − P₂){a₂(H^±) − a₂(H)}, with both arms evaluated in source context H alongside the full and code arms, and interaction I_M = A_M,F − A_M,S − A_M,C. There is no general identity ψ_M,C = 1 − ψ_M: block 3, LayerNorm and context effects intervene. This study makes no upstream necessity claim; that is a separate extension." The N-M rows of §3, §4 and §9 are then dropped, and the forecast falls by ≈ 0.25 CPU-h.

### 2.5 The decoy: requirements, and why the obvious constructions fail
A decoy for model j must satisfy:
- (R1) **code present:** the C2 activation-only gates (Sup, L1, R1) pass on it with unchanged thresholds. C0v is not rerun: charts frozen and validated by C2 S3; SUP covers new rows (§3 row 14);
- (R2) **code unread:** the registered code interchange has zero effect on the decoy's logits, exactly;
- (R3) **responsive:** RESP (θ′_full > 0.30) and SPEC pass;
- (R4) **a real model** where possible, so the network's own forward and patch path (X1) run on it.

**Failure 1: a copy.** Adding a copy, y′ = y + UL_By with col(U) ⊂ K, leaves the original code read: USED, as the request says. Moving the code *and* adding a visible copy is not a decoy either. The FWL regression of y on f(φ) absorbs every linear harmonic covariation into col(B̂), the copy included, so the method rightly calls the copy part of the code (fixture T-COPY, §5.1). A response that keeps its size without the code must therefore run through directions the registered code excludes: Γ, P_rest, higher harmonics, interactions (exactly the Q-CODE exclusions).

**Failure 2: removal without compensation fails the response gate.** If the readout of the code is removed and nothing else changes, A′_full = A_Γ + A_rest and

  θ′_full = (1 − ψ)·θ_full = 0.1494 × 0.9469 = **0.1415**, 0.1461 × 0.9588 = **0.1401**, 0.1443 × 0.9556 = **0.1380** [W, C2 TEST],

all below 0.30. V3x fails, the model is EXCLUDED/MODEL_HEADROOM in all three, and the test stops before it can say NOT_USED. This settles the request's planning point by desk arithmetic from exact identities. **The unamplified decoy's gate result is still computed and reported** (gate V3x′-g1, §3 row 23; R-C2ND-1; PASS/FAIL only before the TEST outcome, its value unsealed at REPORT, §6.7 L5). It is never called NOT_USED.

**The fix: a fixed gain (R-C2ND-1).** Amplify the readout that remains: the decoy reads (I − P_S)y with gain g_D. Then θ′_full = g_D(1 − ψ)θ_full. For a response at least 2× the gate margin (addendum 25 rule 1: θ′ ≥ 0.60), g_D ≥ 0.60/0.1380 = 4.35 [W] (c_min 4.24 / 4.28 / 4.35). **g_D = 6 is fixed now and disclosed as chosen with knowledge of the opened C2 values** (θ′ ≈ 0.849 / 0.841 / 0.828 [W]; 2.8× the margin). There is no pilot split and no gain menu. **The measured share does not depend on g_D** (Lemma DG, §2.8), so fixing it from opened values cannot bias the endpoint; amplification makes the response gate satisfiable by construction (owner Q3). If the frozen-gain decoy nevertheless fails an entry gate, the outcome is recorded as such (EXCLUDED_j/<gate> or INCONCLUSIVE) and no redesign, larger gain or new carrier is introduced within this study. The decoy's predictive becomes sharper (temperature 1/6 on the non-code readout). That is irrelevant to every C2-R statistic, which uses logit differences, and is reported.

### 2.6 The constructions (per model j; inputs are the frozen C2 artefacts of §2.1)
All head-edit decoys are genuine `TransformerLM` instances: a deep copy of `model64` with **only `unembed.weight` replaced** by a float64 matrix, and `ln_final`, every block and every embedding bitwise unchanged. `forward_with_patch` computes `normed = model.ln_final(x)` and `model.unembed(normed)` (`patch.py` lines 111–117), so it applies unchanged; its argument checks (`patch.py` lines 34–63) read only `training`, `cfg`, `hook_names`.

| Decoy | Role | Weight change | Centred readout CM′ | Truth under the construction subspace: ψ′ (code), ψ′_comp |
|---|---|---|---|---|
| **D-NULL** | **primary (family D)** | W′_U := g_D·W_U(I₁₂₈ − Π_S), g_D = 6 | g_D·CM(I − P_S) | **0**, 1 |
| D-ONLY | known case: code necessary | W′_U := W_UΠ_S | CMP_S | 1, 0 |
| D-DOSE | known case: intermediate | W′_U := g_D·W_U(I₁₂₈ − ρΠ_S), ρ = 0.92 | g_D·CM(I − ρP_S) | (1 − ρ)ψ/(1 − ρψ) ≈ 0.313 / 0.319 / 0.322 [W], ≈ 0.68 |
| D0 | positive control of the refit pipeline | none (the base model) | CM | ψ ≈ 0.85 (C2), ≈ 0.15 |
| D-NULL-R | report-only known case (R-C2ND-3): the code literally moved | coordinate map T after `ln_final`; head g_D·W_U | g_D·CM(I − P_S) on y | 0, 1 |
| D-ID | report-only known case (R-C2ND-3): the move compensated | coordinate map T; head W_UQ₀T⁻¹Q₀ᵀ | CM on y (same function as the base) | ψ ≈ 0.85, ≈ 0.15 |
| D-NULL₁ | report-only: the unamplified decoy (R-C2ND-1) | W′_U := W_U(I₁₂₈ − Π_S) | CM(I − P_S) | 0, 1 (its V3x′ is reported) |

"Truth under the construction subspace" means: exact for the frozen C2 projector P_S used to build the decoy. The method re-estimates the projector (§2.8), so under the refit these known answers hold by margin, not exactly (R-C2ND-2; track L's "exact" corrected).

**Lemma DC1 (head-edit readout).** For u = β + Q₀y (C2 Lemma R(ii)): W′_Uu = W′_Uβ + M′y with M′ = W′_UQ₀. For D-NULL, M′ = g_D(M − MP_S) (Q₀ᵀQ₀ = I), and W′_Uβ = g_D(W_Uβ − MP_SQ₀ᵀβ) is a fixed vector that cancels in every difference. `c2_model.readout_basis` (lines 114–136) computes M′ and W′_Uβ from the decoy's own `unembed.weight` unchanged (it reads `ln_final.weight`, `ln_final.bias`, `unembed.weight`). ∎

**Lemma DC2 (exact non-use; R2).** For D-NULL, CM′B = g_DCM(I − P_S)B = 0, since P_SB = B. So for any displacement v, the frozen code interchange gives A′_S = ½dᵀM′P_Sv = 0 and e′_S = 0 exactly. More strongly, any interchange whose range lies in col(B) has zero effect, whatever its oblique kernel. Meanwhile A′_full = g_D(A_Γ + A_rest) and A′_Γ = g_DA_Γ (P_SΓ = 0). In floating point both hold to rounding; gate DX measures it (§3 row 20). ∎

**Lemma DC3 (truth values of D-ONLY and D-DOSE, construction subspace).** D-ONLY: A′_full = ½dᵀMP_SΔy = A_S, and the frozen-projector interchange gives A′_S = A_S, so ψ′ = 1 and A′_comp = ½dᵀMP_S(I − P_S)Δy = 0. D-DOSE: A′_full = g_D[(1 − ρ)A_S + A_Γ + A_rest] and A′_S = g_D(1 − ρ)A_S, so ψ′ = (1 − ρ)ψ/(1 − ρψ). For ψ ∈ [0.80, 0.90], ψ′ ∈ [0.242, 0.419] ⊂ (0.10, 0.50) [W]: PARTIAL whatever the fresh ψ is in that range. ψ′_comp = 1 − ψ′ ∈ [0.58, 0.76]: NOT_NECESSARY. ∎

**Response of every decoy [W, C2 TEST values]:** θ′(D-NULL) 0.849 / 0.841 / 0.828; θ′(D-DOSE) = g_D(1 − ρψ)θ_full = 1.235 / 1.234 / 1.220; θ′(D-ONLY) = θ_S = 0.805 / 0.819 / 0.818; θ′(D-NULL₁) 0.141 / 0.140 / 0.138 (fails, reported). All decision-bearing decoys pass 0.30 by ≥ 2.6×. The y-placebo response of the decoys stays: the y pair's response runs mainly through Γ (C2 y-partition: A_Γ ≈ 0.93 of A^Y_full, A_S ≈ 0.0075 for 1729 [W]), so V3y′ ≈ g_D·V3y.

**The coordinate variants (report-only; R-C2ND-3; MD-6).** They close the "it only switched off the head" objection by moving the code itself into the original head's null space.
- **Null directions (MD-6: full-logit nullity).** V₀ (127 × k₀) is an orthonormal basis of **ker(M)** (k₀ = 127 − rank(M) ≥ 91), from the right singular vectors of M whose singular values are ≤ 1e-12·σ_max. U := V₀(L_BV₀)⁺ (127 × 6) is the minimum-norm solution of L_BU = I₆ with col(U) ⊂ ker(M). It does not depend on which orthonormal basis of ker(M) is used, so no sign or order convention affects it. Construction gates: rank(L_BV₀) = 6 with σ_min/σ_max ≥ 1e-6; cond₂(T) ≤ 1e8.
- **The map.** T := I₁₂₇ + (U − B)L_B, T⁻¹ = I₁₂₇ + (B − U)L_B.

**Lemma DC4.** (i) TB = U ⊂ ker(M) (the code is moved into full-logit-null directions); TΓ = Γ (L_BΓ = 0); T is the identity on ker(L_B), so Γ and the rest stay where they are; L_BTy = L_By (the code coordinates are kept). (ii) T⁻¹ is as stated (direct multiplication, using L_BU = L_BB = I₆). (iii) The decoy coordinates y′ := Ty are realised by a model wrapper whose `ln_final` is the module sequence (the frozen LayerNorm, then the fixed affine map u ↦ β + Q₀TQ₀ᵀ(u − β)). u′ − β ∈ col(Q₀), so C2 Lemma R holds with the same Q₀ and β, and `forward_with_patch` applies unchanged (it calls only `model.ln_final` and `model.unembed`).
- **D-NULL-R:** the head is `unembed.weight` = g_D·W_U. Then M′y′ = g_DM(y + (U − B)L_By) = g_DM(I − P_S)y, since MU = 0: **the same logit differences as D-NULL**, with the code sitting at U. (With U ⊂ ker(M) the logits agree up to the fixed vector g_DMP_SQ₀ᵀβ, not merely after centring.)
- **D-ID:** the head is W_UQ₀T⁻¹Q₀ᵀ. Then z″ = W_UQ₀T⁻¹Q₀ᵀβ + My: **the same function as the base model**, up to a constant logit vector.
(iv) **Equivariance.** OLS is exactly equivariant under y ↦ Ty (B̂ ↦ TB̂, Γ̂ ↦ TΓ̂, residuals ↦ Tε̂). GLS given Σ is equivariant (Σ ↦ TΣTᵀ gives L ↦ LT⁻¹ and P ↦ TPT⁻¹). Ledoit–Wolf is not equivariant under a non-orthogonal T (its target μI is not mapped to TμITᵀ). So the method's ψ on D-ID and D-NULL-R differs from D0 and D-NULL only through the Ledoit–Wolf shrinkage and rounding; that is what these two report-only cases show. ∎

The coordinate variants are not `TransformerLM` instances. LayerNorm with non-uniform γ does not commute with a general T, so the move cannot be folded into upstream weights exactly; it runs through the wrapper. ‖U‖_F/‖B‖_F and cond₂(T) are reported. `c2_model.readout_basis` needs `ln_final.weight`, so the wrapper uses an ND basis adapter (§11.2).

**Rejected variant: an upstream move at `resid_post_3`.** Moving the code before `ln_final` changes σ(a) row by row: ‖r + Nc‖² ≠ ‖r + c‖², because the cross terms ⟨r, Nc⟩ ≠ ⟨r, c⟩. The moved code would still be read through the LN scale, so its truth value at the readout is not known. The readout-site constructions have no such channel: upstream activations and σ are bitwise those of the base model, and the move acts on normalised coordinates. Track X's orthogonal swap (D-MOVE with head gM(I − P)Tᵀ) is not used: it needs a modified head, so it does not leave the code in the original readout's null space, and under the refit it is equivalent to D-NULL up to rounding (comparison MD-6).

### 2.7 What each decoy preserves and what it does not

| | D-NULL / D-DOSE / D-ONLY / D-NULL₁ | D-NULL-R / D-ID |
|---|---|---|
| Embeddings, blocks 0–3, `ln_final` | bitwise identical | bitwise identical; the fixed map follows `ln_final` |
| Activations at `resid_post_2`, `resid_post_3`, `ln_final_out` | bitwise identical (so Sup, chart phase, L1, R1 and N2 are literally the base model's) | `ln_final_out` coordinates are y′ = Ty (code at U); upstream identical |
| Readout of the code | removed (D-NULL, D-NULL₁), scaled by (1 − ρ)g_D (D-DOSE), sole readout (D-ONLY) | removed (D-NULL-R); unchanged function (D-ID) |
| Readout of Γ and P_rest | ×g_D (D-NULL, D-DOSE); ×1 (D-NULL₁); removed (D-ONLY) | ×g_D (D-NULL-R); unchanged (D-ID) |
| Model predictive p | sharper or changed; not a plausible language model | the same remarks |
| Known answer for C2-M, C2-S* | **none** (the layer-2 code feeds non-code readout directions through block 3; the S* plane differs from P_S) | none |

Every decoy is built **per model**, from that model's own frozen P_S, M, Q₀ and β. The decoy identity is `decoy_sha64`: sha256 over the float64 bytes of the decoy state dict (sorted keys) plus the construction record (base `state_sha`, the C2 FIT sha256, g_D, ρ, the construction version). The float32 `c1_model.state_sha` cannot identify a float64 construction.

### 2.8 How the method is run on a decoy: the fresh refit, the leak, and gain invariance (R-C2ND-2)
The registered C2 recipe (FWL K = 3 on the 36 classes, the 5 covariates and the harmonics of the frozen chart phase; Ledoit–Wolf; GLS; identities; GLS-REF; decoders) is **re-estimated on the fresh DFIT split**. This is problem `R@D` on the base coordinates, shared by D0, D-ONLY, D-DOSE, D-NULL and D-NULL₁, whose activations are identical. Problem `R@T` on Ty serves D-NULL-R and D-ID. The code fit sees activations and oracle quantities only, never the head. The method's statistics use the refit projector P̂_S. **They never use the construction projector P_S**; that would make A′_S ≡ 0 a tautology (track X's design flaw, comparison MD-5). P_S appears only in the exactness gate DX and in the blind S2 diagnostic κ_leak below (reported, never decision-bearing). Using it in a method statistic is a stop-rule S12 violation (§12).

For D-NULL: A′_S = ½dᵀg_DM(I − P_S)P̂_SΔy = ½dᵀg_DM(I − P_S)(P̂_S − P_S)Δy. **The leak is driven only by the estimation difference** between two 8,192-row fits (C2 FIT and DFIT) and their Ledoit–Wolf matrices. Reported (the "estimation leak", R-C2ND-2): the leak share λ_D := E[A′_S]/E[A′_full] and its energy analogue; the canonical angles between col(B̂) and col(B); the operator decomposition of A′_S into readout-visible and readout-null source parts (`c2_attrib.decomposition`, lines 104–112). Scale [H]: λ_D ≈ ε_vis·ψ/(1 − ψ) ≈ 5.7·ε_vis, ε_vis the relative readout-visible error of col(B̂) against col(B), so 0.10 is reached at ε_vis ≈ 0.018. The energy conjuncts are magnified by E[e_S]/E[e_comp]. No recorded quantity bounds ε_vis. Blind S2 diagnostic (F1; matrices only, no rows, no logits): the canonical angles between col(B̂(R@D)) and col(B), and κ_leak := ‖CM(I − P_S)B̂‖₂/‖CMB̂‖₂, reported, not gated.

**Lemma DG (gain invariance).** For the D-NULL family with any gain g > 0: A′_S, A′_full, A′^Y_S and A′^Y_full scale by g, and e′_S, e′_full and the random reference r′ (`c2_attrib.random_ref` on M′) scale by g². Hence ψ′, η′_S, the random-energy ratio, and the signs of the means of Z010′, Z050′, Vabs′, Vrand′, Y1′ and NEG′ do not depend on g. Their bootstrap bounds scale by g or g² on the shared index stream, so every D decision except RESP′ and SPEC′ (through whether Y1′ is active) is the same for every g (up to the max(1, ·) floor of the numerical guard, which can only make a decision more conservative at small g). Only V3x′ and V3y′ (hence whether Y1′ is active) depend on g. *Proof.* M′ = gM(I − P_S) is linear in g; the bootstrap mean is linear; quantiles commute with positive scaling. ∎ So fixing g_D from opened values cannot bias any D endpoint.

### 2.9 LN-scale share (descriptive; "is part of the complement just LayerNorm rescaling?") and the decoy's upstream channel
With σ± := √(Var(a(H±)) + ε) from `resid_post_3`, write Δy = Δy_dir + Δy_σ, with Δy_σ := (1 − σ⁺/σ⁻)·y⁺ and Δy_dir := (σ⁺/σ⁻)y⁺ − y⁻ (y⁺ renormalised with arm 2's scale). The decomposition is exact, because y is linear in 1/σ given the centred state. Reported per model: E[½dᵀM(I − P_S)Δy_σ]/E[A_full] (the LN-scale part of ψ_comp), the same with P_S, and the symmetric average over both arm orders. For the decoys: E[½dᵀM′Δy_σ]/E[A′_full], the part of the decoy's response that is pure rescaling. Through it, the upstream code's norm reaches the decoy's non-code readout. **This is the one residual channel by which the decoy can still depend on the upstream code. It is outside the registered readout interchange** (comparison MD-7). It is descriptive only and decides nothing; Q-CODE-D states it (§7.1).

### 2.10 Controls at a glance
- **Positive controls:** D0 (the base model through the refit pipeline, expected USED); D-ONLY (code-only head, expected USED and NECESSARY); D-ID (report-only, expected USED).
- **Negative controls:** D-NULL (the decision-bearing decoy, expected NOT_USED); D-NULL-R (report-only, expected NOT_USED).
- **Intermediate control:** D-DOSE (expected PARTIAL and NOT_NECESSARY).
- **Placebo:** the C2 y-translation donors (Y1 for the base model, Y1′ for D-NULL), with the C2 activity rule (κ_m < 0.01 and V3y PASS).
- **Feasibility controls:** the oracle identity θ_oracle = 1 and the 2× headroom check (ORACLE-FEAS, §3 row 9); the unamplified decoy's response gate (D-NULL₁, reported).
- **Synthetic known cases:** §5.1, run in the tests and in the synthetic dry run.

---

## 3. Gates in exact order (with statistics and thresholds)

Conventions as C2 §7: the `c1_records.run_c1_gate` / `classify_exception` taxonomy; scopes study / model / family; separate coordinator-dispatched jobs S1, S2, S3 + S4, S5, each metered, reviewed and accepted before the next, with the live-state dry check of §10.2 before each. New FAIL_TECHNICAL class `DECOY`. New INCONCLUSIVE/EXCLUDED reasons `KNOWN_CASE_UNRESOLVED`, `CONSTRUCTION`, `ORACLE_FEASIBILITY`. New family outcome `KNOWN_CASE_CONTRADICTED`. "VAL bound" means 5,000 draws at one-sided α = 1/60 (ranks 84 / 4,917); "TEST bound" means the family stream of §4.1.

| # | Stage | Gate | Content | Threshold | On failure | Scope |
|---|---|---|---|---|---|---|
| 0a | owner | AUTH-IMPL | owner addendum naming the C2ND-DESIGN-v1 sha256 and the dry-run budget → `AUTH_IMPL.json` (implementation, tests, synthetic-only dry run; §13 step 2) | recorded | nothing is written | study |
| 0 | IMPL | IMPL | `API.md` first; independent tests A/B before modules (§11.4); modules ≤ 400 lines; full suite detached; code freeze H; code index regenerated in its own commit | §11 | stop (S14) | study |
| 0b | pre-freeze | DRY | metered synthetic dry run end to end, scratch scope `c2nd-dry-v1` (§10.1) | every criterion of §10.1 | fix before freeze | study |
| 0c | freeze | FREEZE | C2ND-FROZEN-v1 is byte-identical to C2ND-DESIGN-v1 (OPEN items already closed in it); any text change → a new candidate and review. H, the DRY report sha256 and the CONTRACT sha256 are recorded in `c2nd-store/FREEZE.json` (C2 pattern), never in the protocol text. | exact | no AUTH request | study |
| 0d | owner | AUTH-ADMIT | owner AUTH-RUN addendum naming the C2ND-FROZEN-v1 sha256 and the staged budget → `AUTH.json` (§13 step 5) | exact | nothing runs | study |
| 1 | S1 | G0 | protocol sha256 and byte copy; CONTRACT; reused blobs at H (`tools/c2_readout` = H″ blobs of §2.1; c1prime, x4_circle_history, src); every C2 artefact of §2.1 by sha256, `0115.accepted.json` present, the FIT/DEC key sets of §2.1 present (structural check, no value read before S2); charts; K4 FREEZE; namespace `c2nd-v1` and the hygiene rule (§6.6); store admission; dispatch identity, meter binding, import directory; the reservation record (§6.5) | exact | FAIL_TECHNICAL/AUTHORITY or LINEAGE | study |
| 2 | S1 | PF | the unchanged suites of C2 §7 row 2 including `tests/c2_readout`, plus `tests/c2_nd`; `check_file_sizes` (no line names a C2ND file), `check_imports` | all pass | FAIL_TECHNICAL/PF | study |
| 3 | S1 | H1 | C2 H1 (`c2_oracle.h1_static`, lines 61–83) | exact | FAIL_TECHNICAL/IDENTITY | study |
| 4 | S1 | REG | R_ND complete (§6.2–§6.4) | complete | INCONCLUSIVE/REGISTRY_INCOMPLETE | study |
| 5 | S1 | H2 | sample DFIT, DFEAS, DVAL; separation from R_ND (all roles; the C2 TEST block included); first tokens (`c2_registry.first_token_ok`, lines 389–394); SYMBOL-ORDER (a) | 0 collisions | FAIL_TECHNICAL/LINEAGE | study |
| 6 | S1 | H3 | C2 H3 composition (`c2_oracle.h3`, lines 264–300) on the new splits, Decimal rows (`decimal_rows`, lines 303–330) | C2 T1–T8 | FAIL_TECHNICAL/ORACLE | study |
| 7 | S1 | H4 | f_x ≥ 0.90, f_y ≥ 0.85 on DFIT, DFEAS, DVAL with the frozen s_max; coverage tally | 0.90 / 0.85 | INCONCLUSIVE/ELIGIBILITY | study |
| 8 | S1 | H5 | DVAL lower 0.05 bounds (rank 250 of 5,000, seed 630518) of mean G_x over E_x and of mean G_y over E_y | > 0.01 nat | INCONCLUSIVE/HEADROOM | study |
| 9 | S1 | ORACLE-FEAS (track X §11.1; MD-8) | (i) oracle response identity: A_full computed with the oracle's own normalised log-predictive in place of model logits equals G row by row (C2 Lemma D2), \|A_full^oracle − G\| ≤ 1e-12·max(1, \|G\|) on every DVAL row, so θ_oracle = 1; (ii) headroom at 2× the margin: the same H5 lower bounds > 0.02 nat | as stated | (i) FAIL_TECHNICAL/ORACLE; (ii) INCONCLUSIVE/ORACLE_FEASIBILITY | study |
| 10 | S2 | M0 | C2 M0 per base model (`c2_model.m0`, lines 228–257) on the 1,024 lowest-id DFIT rows | C2 T9, T10, T18 | FAIL_TECHNICAL/MODEL | study |
| 11 | S2 | M0-D | per model and decoy: (i) the decoy weights equal the frozen formula recomputed from the bound inputs, bitwise, and `decoy_sha64` is recorded; (ii) every non-head parameter is bitwise the base's; (iii) the decoy's `ln_final_out` hook is bitwise the base's (head edits), or equals β + Q₀TQ₀ᵀ(u − β) within 1e-12 relative (coordinate decoys), on 1,024 rows; (iv) decoy identity patch at `ln_final_out` bitwise; (v) decoy readout identity ‖z′ − (W′_Uβ + M′y′)‖∞ ≤ 1e-9·max(1, ‖z′‖∞); (vi) construction of the coordinate decoys: rank(L_BV₀) = 6 with σ ratio ≥ 1e-6, cond₂(T) ≤ 1e8; (vii) **adapter identities at 1e-10, norm-scaled (track X §12; MD-8, MD-15):** ‖V₀ᵀV₀ − I‖_max, ‖L_BU − I₆‖_max, ‖MU‖_max/(‖M‖_max‖U‖_max), ‖TT⁻¹ − I‖_max, ‖TB − U‖_max/‖U‖_max, ‖TΓ − Γ‖_max/‖Γ‖_max, ‖L_BT − L_B‖_max/‖L_B‖_max, the actual decoy-head nullity ‖CM′B‖_max/(‖CM′‖_max‖B‖_max) for D-NULL and D-NULL₁, and the prediction identities D-NULL-R ≡ D-NULL and D-ID ≡ base on logit differences ‖Δz_a − Δz_b‖∞ ≤ 1e-10·max(1, ‖Δz_b‖∞) on the 1,024 rows; (viii) κ_X1 of each decoy head (as `c2_model.kappa_x1`, `x1_attainable`) | as stated | (i)–(v), (vii) for head edits: FAIL_TECHNICAL/DECOY; (vi), (vii) for coordinate decoys: those report-only cases NOT_COMPUTED (EXCLUDED_j/CONSTRUCTION recorded; family D unaffected); (viii) → INCONCLUSIVE/NUMERICAL for that decoy (D if D-NULL) | study / model |
| 12 | S2 | C0c | chart sha256; Sup(DFIT) ≥ 0.99 | 0.99 | EXCLUDED_j/CHART_UNAVAILABLE | model |
| 13 | S2 | F1 | refits R@D and R@T per model, exactly C2 F1 (`c2_stats.f1_problem` lines 370–379, `c2_code.problem` lines 287–307, `c2_stats.gls_ref` lines 185–202): design rank 47; cond ≤ 1e8; LW eigen-ratio; whitened rank 11 and cond ≤ 1e8; G1 identities; GLS-REF ρ_ref ≤ 1e-20 and projector gate; decoder equivalence. Plus the blind leak diagnostic of §2.8 for R@D (canonical angles between col(B̂(R@D)) and col(B), κ_leak; matrices only, no rows, no logits; reported, not gated) | C2 T11–T14, T17 | R@D: EXCLUDED_j/PATCH_MODEL_DEGENERATE or NUMERICAL (family D); R@T: the report-only cases NOT_COMPUTED | model |
| 14 | S3 | SUP | Sup(DFEAS) ≥ 0.99 (C0v is not rerun: charts frozen and validated by C2 S3; SUP covers new rows) | 0.99 | EXCLUDED_j/CHART_UNAVAILABLE | model |
| 15 | S3 | L1 | on DFEAS: the C2 code with the frozen C2 decoders (N-R; the C2 T-PRE-MODEL rule on new rows); R@D and R@T with their DFIT decoders (D; report-only cases); L1-2 with the frozen C2 M decoders (N-M) | R²_code\|0 ≥ 0.50, ρ_inc ≥ 0.90, denominators > 0 | EXCLUDED_j/LINK (that family) | model |
| 16 | S3 | R1 | the same codes; zero-modulus overrides (`c2_code.r1`, lines 189–214) | 0.75 | CNHS_j (that family) | model |
| 17 | S3 | N2 | the S and C states of N-M on DFEAS against the frozen C2 N2 fit (`c2_code.n2_gate`, lines 243–260); states only, no forward | max(0.05, F(D₂) + 0.02) | EXCLUDED_j/RADIAL_SUPPORT (N-M) | model |
| 18 | S3 | SURVIVAL | ≥ 2 ok models per family | 2 of 3 | the family stops | family |
| 19 | S4 | X1 (ephemeral) | base: natural arms, the R interchange arms and **the complement arm, computed directly and compared with A_full − A_S** (MD-15) on every DVAL eligible row; D-NULL: natural decoy arms and its R@D interchange arms on every eligible row; D-ONLY, D-DOSE, D-NULL₁, D-ID, D-NULL-R: the 1,024 lowest-id eligible rows; the base model's variant complement arms (R_E, R_K1, R_K2; §4.2) on the 1,024 lowest-id eligible rows | τ_X1 = 1e-9·max(1, ‖z‖∞) | FAIL_TECHNICAL/X1; a failure confined to decoy arms → FAIL_TECHNICAL/DECOY, scope family D | study (decoy-confined: family D) |
| 20 | S4 | DX (decoy exactness) | with the **construction** projector, per row: D-NULL, D-NULL₁ and D-NULL-R \|A′_S\| ≤ 1e-9·max(1, \|A′_full\|) and e′_S ≤ 1e-18·max(1, e′_full); D-ONLY \|A′_comp\| ≤ 1e-9·max(1, \|A′_full\|); D-DOSE \|A′_S − g_D(1 − ρ)A_S\| ≤ 1e-9·max(1, \|A′_S\|); D-ID ‖C(z″ − z)‖∞ ≤ 1e-9·max(1, ‖z‖∞). Ephemeral: identity diagnostics only | as stated | FAIL_TECHNICAL/DECOY; a failure confined to decoy arms → FAIL_TECHNICAL/DECOY, scope family D | study (decoy-confined: family D) |
| 21 | S4 | V3x, V3y | base, C2 §6.6 (seeds §4.1) | L_{1/60} > g_s | EXCLUDED_j/MODEL_HEADROOM (N-R, N-M); V3y: Y1 inactive (SPECIFICITY_NOT_ESTABLISHED) | model |
| 22 | S4 | Y1 | base, frozen C2 projector, if active | U_{1/60} < −g_s | EXCLUDED_j/NUISANCE_IN_S (N-R) | model |
| 23 | S4 | V3x′, Y1′; V3x′-g1 | D-NULL with the R@D refit projector: θ′_full > 0.30 (V3x′); Y1′ if V3y′ passes. **V3x′-g1 (report-only, R-C2ND-1):** the same bound for D-NULL₁ (expected to fail; desk 0.141 / 0.140 / 0.138). Releases PASS/FAIL only (§6.7 L5) | as V3x, Y1 | V3x′, Y1′: EXCLUDED_j/MODEL_HEADROOM or NUISANCE_IN_S (D); no redesign; V3x′-g1: none (reported) | model |
| 24 | S4 | KC (core known cases) | per model, at VAL bounds (5,000 draws, α = 1/60 per bound, seed 630506): D0 → USED; D-ONLY → USED and NECESSARY; D-DOSE → PARTIAL and NOT_NECESSARY (each with its own RESP and SPEC prerequisites; the R@D refit projector). PASS iff every resolved case equals its known category. Releases PASS/FAIL only | §5.2 | a declared category ≠ the known one → **KNOWN_CASE_CONTRADICTED(j, case)** (D stops for j; S13 before ACCEPT; reported as a finding, §4.3, §7.3); any case undeclared → EXCLUDED_j/KNOWN_CASE_UNRESOLVED (D) | model |
| 25 | S4 | KC-R (report-only known cases, R-C2ND-3) | D-NULL-R → NOT_USED, D-ID → USED, on the R@T refit, VAL bounds as KC (same seed stream, separate arrays). Releases PASS/FAIL only | §5.3 | a contradiction → qualifier MOVE_CASE_CONTRADICTED(j, case) on every D licence, named in the report; **no effect on the D outcome and no stop**; NOT_COMPUTED if row 11 (vi)/(vii) or row 13 (R@T) failed | model |
| 26 | S4 | P1 | §4.5 → N_F per family, k | §4.5 | INCONCLUSIVE/UNDERPOWERED or PRECISION_LIMITED(j) | family |
| 27 | — | ACCEPT | the coordinator's review of S1–S4 with sealed means unopened; the release names k | — | stop | study |
| 28 | S5 | REG2 | R′_ND (§6.4); sample k DTEST blocks; separation; first tokens; SYMBOL-ORDER (a) | 0 collisions | FAIL_TECHNICAL/LINEAGE | study |
| 29 | S5 | T-PRE | H1; DTEST oracle; H3 (4 rows); \|f − f_DVAL\| ≤ 0.02; H5 on DTEST; M0 and M0-D identity checks on 1,024 DTEST rows; X1 and DX as rows 19–20 on DTEST (ephemeral) | as above | INCONCLUSIVE/TEST_GATE (endpoints NOT_RUN/T-PRE); FAIL_TECHNICAL for identity, X1, DX (a failure confined to decoy arms → FAIL_TECHNICAL/DECOY, scope family D, as rows 19–20) | study |
| 30 | S5 | T-PRE-MODEL | Sup(DTEST) ≥ 0.99; L1, R1 with the frozen decoders (C2 code, R@D, R@T, M); N2 | as at DFEAS | EXCLUDED_j/TEST_GATE | model |
| 31 | S5 | RESP-SPEC | first part of each family stream: N-R RESP_j, SPEC_j; D RESP′_j, SPEC′_j; N-M RESP_j and the transmission statements | §4.3 | EXCLUDED_j/MODEL_HEADROOM or NUISANCE_IN_S; endpoint NOT_RUN | model |
| 32 | S5 | NUM | every decision bound clears g_s (§4.4) | §4.4 | INC_j/NUMERICAL | model |
| 33 | S5 | ENDPOINT | N-R, N-M, D per §4.3, with the rule-6 statements and qualifiers; the KC and KC-R cases re-evaluated on DTEST as report-only categories (seed 630507) | §4 | outcome | family |
| 34 | S5 | REPORT | licences (§7) with Q-CODE / Q-CODE-D; unsealing of the DVAL values; descriptives (§2.8, §2.9; the C2 §2.12 set for the base model on DTEST; the unamplified decoy result); POST-DESC rule of C2 §5.7; union bounds displayed (§8.3) | — | — | — |

**Gate order is enforced by an ND `LogitPolicy`** (§11.3), with `GATE_ORDER` = IMPL AUTH-ADMIT G0 PF H1 REG H2 H3 H4 H5 ORACLE-FEAS M0 M0-D C0c F1 SUP L1 R1 N2 SURVIVAL X1 DX V3x V3y Y1 V3x′ Y1′ V3x′-g1 KC KC-R P1 ACCEPT REG2 T-PRE T-PRE-MODEL RESP-SPEC NUM ENDPOINT REPORT. No check uses data before it exists, and no DTEST token exists before ACCEPT. (AUTH-IMPL, DRY and FREEZE are coordinator steps outside the driver.)

---

## 4. Statistics and decision machinery

### 4.1 Units, bounds, seeds
- **Rows, indicator form, conditioning:** C2 §6.1 unchanged: one history per row; arms are deterministic functions of it; s·1_E over all rows. Inference is conditional on the three models, the frozen C2 projectors, the frozen charts, the decoy constructions and the DFIT refits. No population-of-seeds claim.
- **TEST family bounds:** `c1_means.bootstrap_means(arrays, seed, draws=20000)` with one shared index stream per family (all models, all statistics), via `c2_decide.stream_bounds` (lines 38–46); L, U = `quantile_with_rank` at α and 1 − α (`c1_means.rank_for`: rank = ⌈20,000·p⌉). **α_NR = α_D = 1/300** (ranks 67 / 19,934; z_{1−α} ≈ 2.713). **α_NM = 1/360** (ranks 56 / 19,945; z ≈ 2.773). α_NR and α_D are lowered from track L's 1/240 by the recount (§8.1). RESP/SPEC run first, then the endpoint arrays, with the same seed and n (identical indices; C2 T-BOOT).
- **What the bounds deliver (C2 §6.2, RC-9).** Rank 67 of 20,000 has expected tail 67/20,001 = 0.0033498, slightly above 1/300 = 0.0033333 [W]; the tail Monte Carlo relative error is ≈ 12%. The error statements of §8 are exact event-counting arguments conditional on valid individual bounds; the implemented percentile-bootstrap family error rate is nominal. No rank treatment is chosen after results are seen.
- **VAL gate bounds:** 5,000 draws, α = 1/60 (ranks 84 / 4,917); H5 and ORACLE-FEAS (ii) at rank 250.
- **Seeds (PCG64; new, disjoint from C2's 6205xx and from the parallel rounds' 6201xx):** 630503 N-R stream; 630504 D stream; 630505 N-M stream; 630506 KC and KC-R (VAL); 630507 KC, KC-R and D-NULL-R report on DTEST (5,000 draws, two-sided 95%, ranks 125 / 4,875); 630508 descriptive ratio intervals (λ_D, LN-scale shares, ι_M, η_comp; `c2_attrib.ratio_intervals` lines 221–237, UNDEFINED on a zero or non-finite denominator, no redraw); 630511 V3x; 630512 V3y; 630513 Y1; 630514 V3x′; 630515 Y1′; 630516 / 630517 P1 SD / centred; 630518 H5 and ORACLE-FEAS (ii) (DVAL and DTEST, two calls); 630519 V3x′-g1.

### 4.2 Family streams (per model; indicator form; DTEST)
- **N-R (seed 630503), 9 arrays plus 1 check:** V3x = (A_full − 0.30·G)1_{E_x}; Y1 = (A^Y_S − 0.10·A^Y_full)1_{E_y} (frozen C2 projector); Zc010 = (A_comp − 0.10·A_full)1_{E_x}; Zc050 = (A_comp − 0.50·A_full)1_{E_x}; Wc = (A_comp + 0.10·A_full)1_{E_x}; Vc = (e_comp − 0.10·e_full)1_{E_x}; NEGc = A_comp·1_{E_x}; Zc090 = (A_comp − 0.90·A_full)1_{E_x}; Zc100 = (A_comp − A_full)1_{E_x}; and, report-only, Z090 = (A_S − 0.90·A_full)1_{E_x} as an algebra check (Zc010 ≡ −Z090 to rounding). **Report-only variant arrays (RC-1):** variant arrays v:Zc010 = (A_full − A_S^v − 0.10·A_full)1_{E_x} and v:Zc050 for v ∈ {R_E, R_K1, R_K2}, A_S^v from the frozen FIT keys `{v}_P_S`, `{v}_L`, `{v}_B` (guards β_A with δ_P(v) from `FIT_j.json` "delta"); outside Lemma FW-ND, as C2 §6.3 remark 6; X1 on the variant complement arms on the 1,024 lowest-id eligible rows (§3 row 19). Same seed and indices as the primary N-R arrays.
- **D (seed 630504), 7 arrays plus 5 report-only:** for D-NULL with P̂_S(R@D): V3x′, Y1′, Z010′, Z050′, Vabs′, Vrand′ (C2 §2.9 with r′ from `c2_attrib.random_ref`, lines 77–84, on M′ and the refit Σ̂), NEG′ = A′_S·1_{E_x}. Report-only, D-NULL-R with P̂_S(R@T): Z010, Z050, Vabs, Vrand, NEG (inputs to the qualifier DECOY_LOCATION_DEPENDENT only).
- **N-M (seed 630505), 7 arrays:** V3x; Ztau = (A_M,F − 0.10·A_full)1_E; ZMc010; ZMc050; WMc; VMc; NEGMc = A_M,C·1_E.

Arrays are built with the C2 kernels: `c2_attrib.ind` (lines 34–39), `half_dot` (43–46), `energy` (54–55), `pair` (87–92) and `threshold_arrays` (260–264) on (y¹, y²) with the projector or head in question; `cm_quantities` (197–205); `c1_endpoint.Zfull_hat` for V3x.

### 4.3 Per-model and overall rules
**Per-model rules.**
- **N-R** (an ND `nr_model` with the §2.3 table): RESP not declared → EXCLUDED/MODEL_HEADROOM; Y1 active and SPEC not declared → EXCLUDED/NUISANCE_IN_S; a bound inside its guard counts as neither sign; then the declared category, else INC. Then the coarse statements, the rule-6 statement (a), the nested unexpected-case entry and the qualifier NEGATIVE_COMPLEMENT; then the report-only variant categories and the qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR (§2.3), which never change the primary category.
- **D** follows C2 §6.4 R rules 1–5 verbatim through `c2_decide.r_model` (lines 137–145) on the D arrays: categories DECOY_USED_j (L(Z050′) > 0 and L(Z010′) > 0), DECOY_PARTIAL_j (L(Z010′) > 0 and U(Z050′) < 0), DECOY_LOW_ALIGNED_j (U(Z010′) < 0, U(Z050′) < 0, the energy conjuncts not both certified) and DECOY_NOT_USED_j (U(Z010′) < 0, U(Z050′) < 0, U(Vabs′) < 0, U(Vrand′) < 0), with C2's coarse statements. Then **rule-6 statement (b), DECOY_POSITIVE_BELOW_MARGIN_j:** declared iff L(NEG′) > 0, U(Z010′) < 0 and U(Z050′) < 0, with RESP′ and SPEC′ prerequisites; truth claimed 0 < ψ′ < 0.10. Qualifier NEGATIVE_ALIGNED_CONTRIBUTION(j) iff U(NEG′) < 0.
- **N-M** follows C2 §6.4 M rules 1, 3–7 with the §2.4 categories (`c2_decide.m_model` pattern, lines 148–161; no Y2), then rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN_j (§2.4).

**Overall rules (2 of 3; C2 §6.5 unchanged).** All three models are assessed and reported. Fewer than 2 models after a validity gate → INCONCLUSIVE/<gate>. ≥ 2 models in one category → that outcome:
- N-R: NECESSARY; COMPLEMENT_LOW_ALIGNED (≥ 2 in {NECESSARY, COMPLEMENT_LOW_ALIGNED}, < 2 NECESSARY); CODE_DOMINANT; NOT_NECESSARY.
- D: DECOY_NOT_USED; DECOY_LOW_ALIGNED; DECOY_PARTIAL; DECOY_USED.
- N-M: ROUTED_AROUND first, then the four _M outcomes.
Else MIXED (≥ 2 resolved) or INCONCLUSIVE/PRECISION. **The rule-6 statements and the nested entry aggregate the same way:** "in [k] models" is licensed iff ≥ 2 models declare it; per-model declarations are always listed. **D additionally:** if KNOWN_CASE_CONTRADICTED occurred in ≥ 1 model at KC, the family outcome is KNOWN_CASE_CONTRADICTED. A KNOWN_CASE_CONTRADICTED at S4 triggers S13 before ACCEPT. If the owner continues, D's TEST arrays are scored report-only with the outcome fixed. No DECOY_NOT_USED licence is issued: one contradicted core known case withholds the "method discriminates" licence. KC-R contradictions do not (R-C2ND-3).

### 4.4 Numerical guard
g_s := 1e-9·max(1, mean_i|s_i|) + β_s (`c2_decide.guard`, lines 49–50).
- **N-R:** A_comp = A_full − A_S, so the complement's error includes the code-projector error; it is never set to zero (track X §12). β_A (coefficient 1) uses δ_P of the frozen C2 projector (`FIT_j.json` "delta"; `c2_stats.delta_p`, lines 205–208; `c2_decide.beta_A`, lines 58–62). For Vc, β_E (`beta_E`, lines 65–72) with (I − P̂_S) in place of P̂_S: (2‖CM(I − P̂_S)Δy_i‖ + ‖CM‖₂δ_P‖Δy_i‖)·‖CM‖₂δ_P‖Δy_i‖. Wc, NEGc, Zc090 and Zc100 use β_A with their own coefficients. The report-only variant arrays v:Zc010, v:Zc050 use β_A with δ_P(v) from `FIT_j.json` "delta" (v ∈ {R_E, R_K1, R_K2}).
- **D:** δ_P of the R@D refit's own GLS-REF, with M′ in place of M.
- **The decoy matrix needs no guard term.** It is *defined* as the stored float64 `unembed.weight`, so M′ is exact by definition. The construction's rounding (A′_S ≠ 0 at ~1e-14 relative under the construction projector) is a property of the decoy, measured by DX, and lies about 10⁷ below the smallest decision margin (≈ 0.01 nat) [H]. (Track X's proposal to add a construction-error term to β_s is therefore not adopted, MD-15.)
- **N-M:** β = 0 (C2 C-44 rule).

### 4.5 Precision ladder P1 (DVAL; outcome-blind; C2 §6.7 pattern)
- P1 powers N-R Zc010 and Zc050; D Z010′ and Z050′; N-M Ztau. The alternative is 0.10·min_j mean(A_full·1_E) (N-R, N-M) and 0.03·min_j mean(G·1_{E_x}) on DVAL (D; 0.10 × the 0.30 gate × the oracle contrast, a lower bound on 0.10·mean(A′_full·1_E) whenever V3x′ passes; oracle-only). [W: SD(Z010′) ≈ 0.08 gives an mde of 0.0044 < 0.033 at N = 4,096, so k = 1 is still expected.]
- Kernels: `precision.sd_b4_draws`, `centered_draws`, `precision_summary` through `c2_stats._summaries` (lines 310–323) with the ND seeds and cfg alpha = α_F (`c2_stats.p1`, lines 326–349, hard-codes C2 seeds and is not called). N ∈ {4,096, 8,192, 16,384}. N_F = the smallest N at which every F-ok model passes; else the smallest N at which ≥ 2 pass (the others PRECISION_LIMITED(j)); else F → INCONCLUSIVE/UNDERPOWERED. N_test = max N_F over the families still alive; k = N_test/4,096.
- MDE reports (not gated): Wc, Vc, NEGc, Vabs′, Vrand′, NEG′, ZMc010, ZMc050, WMc, VMc.

### 4.6 Power, feasibility (addendum 25 rule 1) and uncertainty [H, from C2 TEST bounds]
The C2 one-sided half-widths at N = 4,096 are 0.0091 nat (Z010) and 0.0062 nat (Z050), i.e. SD ≈ 0.22 and 0.15 nat. A two-point variance model Var(Z^c) ≈ (ψ − c)²·V + n gives V ≈ 0.058 and n ≈ 0.015. Then:
- **N-R:** SD(Zc010) = SD(Z^{0.90}) ≈ 0.125 nat; half-width 2.713 × 0.125/64 ≈ 0.0053 nat against E[Zc010] = (ψ_comp − 0.10)E[A_full] ≈ 0.049 × 1.03 ≈ 0.050 nat: margin ≈ 9× (CODE_DOMINANT). P(INC) ≈ 0. Wc: E ≈ (0.149 + 0.10) × 1.03 ≈ 0.26 nat, far positive (but NECESSARY fails on Zc010).
- **D:** SD(Z010′) ≈ 0.1·g_D·SD(A_comp) ≈ 0.6 × 0.13 ≈ 0.08 nat; E[Z010′] ≈ −0.10·E[A′_full] ≈ −0.09 nat; half-width ≈ 0.0034 nat: margin ≈ 26× (sampling only). The energy conjuncts are negative by g_D²·e_comp-sized amounts, plus the refit leak, which is magnified by E[e_S]/E[e_comp] and not bounded in advance (§2.8).
- **N-M:** C2 passed P1 for M at N = 4,096; the ZMc arrays have the scale of the C2 ZM arrays.
- **P1 condition:** mde = (z_{1−α} + z_{0.80})·SD/√N ≤ 0.10 nat. At α = 1/300, z + z = 3.555, so N = 4,096 passes for SD ≤ 1.80 nat, 8,192 for SD ≤ 2.55, 16,384 for SD ≤ 3.60 (α = 1/360: 1.77, 2.50, 3.54). For D the alternative is 0.03·min_j mean(G·1_{E_x}) ≈ 0.033 nat (§4.5): SD(Z010′) ≈ 0.08 gives an mde of 0.0044 at N = 4,096. **k = 1 is expected in every family.**
- **Feasibility rule 1 (best case ≥ 2× the margin), per outcome.** CODE_DOMINANT: distance 0.049 (ψ units) to 0.10 against a half-width of ≈ 0.005 → ≈ 9×. DECOY_NOT_USED: the sampling half-width (≈ 0.003) is > 25× below the margin, but the refit leak is not bounded in advance (§2.8). DECOY_PARTIAL or DECOY_LOW_ALIGNED from leak alone is possible. Rule 1 is shown for the sampling component only [H]. NECESSARY: **best case 0.149 > 0.10 for the registered K = 3 GLS complement; rule 1 says it cannot be reached there, and no run can change that** (owner Q1). The R_E and R_K1 variant remainders (0.06–0.09, §1.4) are report-only and never license NECESSARY. NECESSARY_M: best case 0.14 > 0.10; the same. The rule-6 statements: COMPLEMENT_POSITIVE_BELOW_MARGIN cannot be reached for the same reason; DECOY_POSITIVE_BELOW_MARGIN is reachable only if the leak is certified positive, which the unbounded refit leak makes possible (§2.8) [H]. COMPLEMENT_M_POSITIVE_BELOW_MARGIN (c) cannot be reached for the same reason as NECESSARY_M.

---

## 5. Known-case checks (addendum 25 rule 5)

### 5.1 Synthetic fixtures (tests; synthetic data only, no payload; independent authors, §11.4)
- **T-N1 (Lemma N1):** A_comp = A_full − A_S per row on random readouts, and the direct patched complement equals the subtraction; ψ + ψ_comp = 1; Zc^c = −Z^{1−c} to rounding; L(−X) = −U(X) with ranks 67 / 19,934 (and 56 / 19,945) on a shared stream.
- **T-NEC-KNOWN (necessity on exactly constructed readouts):** a head reading only col(B) → ψ = 1, ψ_comp = 0 → USED and NECESSARY; a head reading only Γ and P_rest → NOT_USED (energy zero) and NOT_NECESSARY; half and half → PARTIAL and CODE_DOMINANT; a cancellation fixture with E[A_comp] ≈ 0 and large |A_comp| → COMPLEMENT_LOW_ALIGNED, never NECESSARY; **a large negative complement (ψ_comp = −0.4) → COMPLEMENT_LOW_ALIGNED with NEGATIVE_COMPLEMENT, never NECESSARY** (the lower bound, MD-2).
- **T-RULE6:** (a) 0 < ψ_comp < 0.10 with adequate precision → COMPLEMENT_POSITIVE_BELOW_MARGIN declared beside NECESSARY or COMPLEMENT_LOW_ALIGNED; (b) a decoy-like readout with a certified small positive leak (0 < ψ′ < 0.10) → DECOY_POSITIVE_BELOW_MARGIN beside DECOY_NOT_USED or DECOY_LOW_ALIGNED; (c) 0 < ψ < 0.10 → CODE_SHARE_POSITIVE_BELOW_MARGIN declared only inside NOT_NECESSARY; (d) 0 < ψ_M,comp < 0.10 → COMPLEMENT_M_POSITIVE_BELOW_MARGIN.
- **T-PROJ-ND (variant qualifiers; RC-1):** synthetic readouts with a primary (K = 3 GLS) complement and R_E, R_K1, R_K2 variant projectors: when a variant's category on v:Zc010, v:Zc050 differs from the primary (e.g. primary CODE_DOMINANT, R_E COMPLEMENT_LOW_ALIGNED) → PROJECTOR_DEPENDENT_NR(j) (R_E) or HARMONIC_DEPENDENT_NR(j, K) (R_K{K}); equal categories → no qualifier; the variant arrays never change the primary category; an EXCLUDED primary returns the primary status and a missing variant array gives NOT_COMPUTED (`c2_decide.variant_category` pattern).
- **T-RESP:** no full response (θ_full < 0.30) → EXCLUDED/MODEL_HEADROOM, never NOT_USED or NOT_NECESSARY; the unamplified decoy reproduces this.
- **T-COPY:** a linear copy of the code placed in other coordinates is absorbed by FWL into col(B̂) → USED; "move + visible copy" → USED; "an appended null copy without moving" → the original stays used. Shows why a copy is not a decoy.
- **T-DECOY-EXACT:** on a small random `TransformerLM`: the head edits reproduce CM′B = 0 (D-NULL, D-NULL₁) and the D-DOSE and D-ONLY identities; W′_Uβ cancels in every difference; the decoy forward equals the base upstream bitwise; `forward_with_patch` and `c2_model.readout_basis` work unchanged on the decoy; a mis-built decoy (wrong g_D, a transposed P_S, the projector of another model) fails M0-D or DX.
- **T-ILLUSION (track X's operator-illusion fixture; MD-9):** a synthetic readout with Σ ≠ I, so that the oblique P_S does not commute with the readout-null projector J, and a source displacement with a component in K. (i) The C2 operator decomposition shows A_S^null ≠ 0 although CMJΔy = 0 (the Makelov–Lange–Nanda mechanism, C2 §2.12), and the decomposition is reported, not used to decide. (ii) A wrongly built decoy that uses the Euclidean orthogonal projector onto col(B), or J, in place of the oblique P_S has M′P_S ≠ 0: DX and M0-D (vii) fail.
- **T-MOVE (Lemma DC4):** with V₀ ⊂ ker(M), U = V₀(L_BV₀)⁺ gives L_BU = I and MU = 0, independently of the basis of ker(M); the T⁻¹ formula; rank(L_BV₀) < 6 → CONSTRUCTION; D-NULL-R and D-NULL give identical logit differences; D-ID is functionally identical to the base (a compensating invertible map is not a negative case); OLS and GLS equivariance under T are exact; Ledoit–Wolf is equivariant under an orthogonal T and not under a non-orthogonal T (so D-ID may differ slightly from D0 while the category stays).
- **T-DOSE:** ψ′(ρ) = (1 − ρ)ψ/(1 − ρψ) and its PARTIAL range for ψ ∈ [0.80, 0.90].
- **T-LEAK:** with a refit projector from an independent sample, the D-NULL leak equals ½dᵀM′(P̂_S − P_S)Δy exactly; it vanishes when P̂_S = P_S.
- **T-GAIN (Lemma DG):** every D decision except V3x′ and V3y′ (hence whether Y1′ is active) is identical for g ∈ {1, 2, 6, 20} on the same rows and index stream.
- **KM1–KM4 (layer-2 necessity on tiny models, exact):**
  - KM1: block 3 with zero attention and MLP output weights, a head reading only the code directions, and every patched state (F, S, C) has the per-row mean and norm of a₂(H) → ψ_M = 1, ψ_M,comp = 0, I_M = 0 → NECESSARY_M;
  - KM2: a head reading only complement directions → NOT_NECESSARY_M;
  - **KM3 (the LN loophole):** as KM1, but the complement changes the row norm only → ψ_M,comp ≠ 0 through the LayerNorm scale alone, so a code that is the sole readout input is *not* shown necessary at layer 2. The N-M licence states that the complement includes LN-scale effects (MD-1);
  - KM4: an MLP gate multiplying code and complement coordinates → I_M ≠ 0, with ι_M reported and the categories computed on ψ_M,comp.
- **T-LNSCALE:** Δy = Δy_dir + Δy_σ exactly; a pure-rescaling pair puts the whole response in the σ part.
- **T-EDGE (track X's threshold-edge fixtures; MD-9):** for every threshold of §2.3, §2.4 and §4.3: a mean exactly at the threshold is never declared on either side; a bound inside its guard is neither sign; an interval straddling a threshold leaves the model INC; equality of L and U at a threshold is handled as INC.
- **T-FAMILY-ND:** the exhaustive grid of §8.4.
- **T-RULES-ND, T-BOOT-ND, T-LADDER-ND:** as C2 §13.3, with the ND seeds, ranks and arrays.

### 5.2 Core known cases on the real models (gate KC; decision-bearing for family D)
D-ONLY is the constructed model where the code is necessary (ψ′ = 1, ψ′_comp = 0, exact for the construction subspace). D-DOSE is an intermediate case known up to C2's precision (Lemma DC3). D0 checks that the refit pipeline reproduces C2. For each case and model, the case's RESP, SPEC and category statements are computed with the VAL bounds and the R@D refit projector, and its necessity category where listed.
- **PASS:** every case's declared category equals its known category.
- **Contradiction:** a declared category differs (D0 declared NOT_USED, LOW_ALIGNED or PARTIAL; D-DOSE declared USED or NOT_USED; D-ONLY declared anything but USED and NECESSARY) → KNOWN_CASE_CONTRADICTED(j, case).
- **Unresolved:** a case declares no category (INC) → EXCLUDED_j/KNOWN_CASE_UNRESOLVED for D.
- **Exactness of the known answers (R-C2ND-2 wording):** D-ONLY's answer is **exact for the construction subspace; robust by margin under the refit**, because A′_comp(D-ONLY) = ½dᵀMP_S(P_S − P̂_S)Δy ≠ 0 under P̂_S. D-DOSE's answer is robust for ψ ∈ [0.80, 0.90] (Lemma DC3). D0's answer is taken from C2's measured result, so a D0 contradiction means a failure to reproduce C2 with a re-estimated projector and is escalated to the owner (S13).

### 5.3 Report-only known cases (gate KC-R; R-C2ND-3)
D-NULL-R (code literally moved into ker(M) and read by the unchanged, scaled head; known NOT_USED) and D-ID (the move compensated; known USED) run on the R@T refit. Their known answers are **exact for the construction subspace and robust by margin under the refit**; they differ from D-NULL and D0 only through Ledoit–Wolf non-equivariance and rounding (Lemma DC4(iv)). They have **no error budget of their own** and no decision effect (coordinator ruling: report-only, own gate KC-R; a contradiction adds a qualifier only): a contradiction is reported as MOVE_CASE_CONTRADICTED(j, case), and a DTEST category of D-NULL-R that differs from D-NULL's gives the qualifier DECOY_LOCATION_DEPENDENT(j).

### 5.4 Coverage of rule 5
Each statistic and gate meets a case with a known answer on real activations: RESP and SPEC (every case), three R categories at validation (D0 USED, D-DOSE PARTIAL, D-ONLY USED) plus NOT_USED on the endpoint decoy D-NULL at TEST and on D-NULL-R (report-only), two necessity categories (D-ONLY NECESSARY, D-DOSE NOT_NECESSARY), the energy conjuncts (D-ONLY, D-NULL), X1, DX and the refit F1/L1/R1. LOW_ALIGNED has a synthetic known case only. NECESSARY_M, COMPLEMENT_LOW_ALIGNED, the rule-6 statements, the N-R variant qualifiers (T-PROJ-ND) and the layer-2 statistics have synthetic known cases only (§5.1; §1.5).

---

## 6. Data registration and separation (R-C2ND-6)

### 6.1 Splits (all new; scope `c2nd-v1`; never the `c2-v1` streams)

| Split | Rows | Use | Logits |
|---|---|---|---|
| DFIT | 8,192 (b0, b1) | refits R@D and R@T (FWL, LW, GLS, GLS-REF, decoders D0/Dcode/Dlin, m̃); M0 and M0-D on the 1,024 lowest-id rows | M0/M0-D rows only |
| DFEAS | 4,096 | activation-only validity on new rows: Sup ≥ 0.99; L1/R1 for the C2 code (frozen C2 decoders), for R@D and R@T (DFIT decoders); L1-2/R1-2 for N-M; N2 for the N-M S and C states | none |
| DVAL | 4,096 | X1 (ephemeral), DX, V3x, V3y, Y1, ORACLE-FEAS, decoy V3x′, Y1′, V3x′-g1, KC, KC-R, P1 | yes; every endpoint-bearing mean sealed (and the V3x′, V3x′-g1, Y1′ means and bounds; §6.7 L5) |
| DTEST | k × 4,096, k ∈ {1, 2, 4} | T-PRE, then the single confirmatory evaluation of N-R, N-M and D | after admission only |

There is no pilot split (R-C2ND-1). Sampling: `HMMSampler(...).sample(4096, SeedTree(0).generator("data", "c2nd-v1", split, block, "cylinder", "overlap", "1.25"))`; sequence ids `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c2nd-v1/{split}/b{block}"), "test", 4096)` (the `c2_data` lines 37–55 recipe with the scope replaced). Donors H⁺, H⁻ and H^Y exactly as C2 (`c2_data.k_y` lines 74–77, `y_donor` lines 80–90, `role_arrays` lines 98–104), including the pure inward y-translation with no wrapping or clamping. DTEST is sampled only after the coordinator's ACCEPT of the S1–S4 report.

### 6.2 Registry R_ND (version `c2nd-reg-v1`; built at S1 before DFIT is sampled)
R_ND is the union of the digest sets of every source below. Any unreadable source, or any unclassified history-bearing store, makes it INCONCLUSIVE/REGISTRY_INCOMPLETE (fail closed; never completed by opening a payload).

| # | Source | Reader | Covers |
|---|---|---|---|
| 1 | every source of C2's registry | the unchanged `c2_registry` readers: `token_sources` (lines 132–158), `inventory` (lines 192–211), `x6_source` (lines 99–128), composed by an ND wrapper because `build` (lines 241–302) accepts only the C2 version names | everything C2's C2-REG1/REG2 covered (C2 CONTRACT "registry": readers a, b, c, d, e, f, k, x6) |
| 2 | `c2-readout-store/hist/HIST_{fit_b0, fit_b1, feas_b0, val_b0, test_b0}.npz` (sha256 in §2.1) | new reader `c2`: the digest columns `digest_H`, `digest_Hp`, `digest_Hm`, `digest_HY` (`c2_data.history_table`, lines 115–130; roles `c2_config.ROLES`, line 100; "" where H^Y is undefined, dropped as in `table_digests`, lines 137–141) | every opened C2 block, the TEST block included |
| 3 | `c2-readout-store/superseded/{0107-a1, 0107-a2, 0109-a1}/` | name scan for any history-bearing array | the superseded C2 attempts. Their `SUPERSEDED.json` records show they stopped at the release check or G0 (vii), before sampling, and the directory listing holds no `hist/` file; the scan confirms this at execution and fails closed if an array appears |
| 4 | C2 dry-run scratch stores: `X:/Downloads/topo-scratch/0104/dry/{frc1, frc2, nat2, nat3}/hist/`, `X:/Downloads/topo-scratch/0105/dry/{full_forced, full_natural, smoke1, smoke2, smoke3}/hist/` | reader `c2scratch`: the same digest columns as row 2, for every `HIST_*.npz` there | the dry-run histories (MD-10, track X §8.3). The FIT/FEAS/VAL ones are bit-identical to C2's (coordinator addendum 4); the dry-run `HIST_test_b*` files are drawn under other names and are covered here |
| 5 | C2 live-state check copies: `X:/Downloads/topo-scratch/0109-pre/livecopy-{0112, 0113, 0114, 0115}/hist/` | reader `c2scratch` | byte copies of the live C2 hist files (expected identical to row 2) |
| 6 | the C2ND synthetic dry-run store `X:/Downloads/topo-scratch/<job>/dry/` (scope `c2nd-dry-v1`, §10.1) | reader `c2scratch` (the ND tables use the same columns) | C2ND's own dry-run histories |
| 7 | the store of the parallel round `coord-history-world-sweep-20261026`, planned `X:/Downloads/projects/topo-pilot/hws-store/` (scope `hws-v1`; histories as uint8 [n, 32] canonical tokens under `hist/<stage>/<key>.npz`) | reader `hws`: digests computed from the token arrays with `scores.history_digests` (as `c2_data.history_table` line 127) | its E4-process (cylinder-O) histories and every other world's histories, if the store exists at REG or REG2 time. OPEN-1 closed (§17): an unreadable or unfrozen store → REGISTRY_INCOMPLETE |
| 8 | the store of the parallel round `coord-x6zc-placebo-20261026`, planned `X:/Downloads/projects/topo-pilot/x6zc-store/` (new loop-sign variant histories; format not yet fixed) | reader `x6zc`, frozen with that round's history format | its new histories, if the store exists at REG or REG2 time. OPEN-1 closed (§17): an unreadable or unfrozen store → REGISTRY_INCOMPLETE |
| 9 | a name scan of `X:/Downloads/topo-scratch/` for any other `HIST_*.npz`, **excluding pytest basetemp trees (any path component whose name starts with `test_`; the pattern is frozen in the CONTRACT)** | reader `c2scratch` for a file in the C2 table format; any other file is listed as NON_C2_FORMAT (path and size recorded; not read; not a registry failure) | any C2-format dry-run history not listed above |

**Inventory classes (ND inventory adapter).** `c2-readout-store` becomes READER (`c2`; in C2 it was the exempt own store). `c2nd-store` is the new own store (EXCLUSION as own). `hws-store` and `x6zc-store` are READER once their readers are frozen; if either store exists at REG or REG2 time and its reader is not frozen, the registry is REGISTRY_INCOMPLETE. Scratch roots stay outside the C2 inventory (R-0100-3); rows 4–6 and 9 are explicit additional sources, as MD-10 requires.

### 6.3 Execution-time reads and what happens during planning (R-C2ND-6)
- **Planning (this document):** no `HIST_*.npz`, `payload.npz`, `state.pt`, `fits/*.npz` content or `sealed/` file was opened or hashed. Directory listings and JSON manifests only.
- **Execution, under the AUTH only:** the frozen registry reads the digest columns of `hist/HIST_*.npz` exactly as C2's REG2 did (rows 2, 4, 5, 6, 9), and the frozen readers of rows 7 and 8 read those stores' history arrays. These are history tables, not model payloads; no `payload.npz`, `state.pt` or `sealed/` file is read by the registry. The C2 store files of §2.1 are re-hashed before and after each C2ND job and must be unchanged (L7, §6.7).

### 6.4 Separation
- **H2 (S1):** U_DFIT, U_DFEAS and U_DVAL are pairwise disjoint and disjoint from R_ND over all roles (H, H⁺, H⁻, H^Y), using `c2_registry.separation` (lines 360–386) on the ND registry object.
- **REG2 (S5):** R′_ND = R_ND rebuilt at S5 (so it includes any parallel-round store written since S1) ∪ U_DFIT ∪ U_DFEAS ∪ U_DVAL. U_DTEST ∩ R′_ND = ∅.
- A collision → FAIL_TECHNICAL/LINEAGE. Rows are never rejected or replaced; within-split duplicates are counted and kept under the C2 convention.

### 6.5 Reservations: scheduling the three parallel rounds (R-C2ND-6; R-HWS-7)
The three rounds of addendum 27 draw histories at different times: HWS stage S0 draws E4-process (cylinder-O) histories; X6ZC draws loop-sign variant histories; C2ND draws at H2 (S1) and REG2 (S5). The coordinator schedules them so their **history-generation reservations never overlap**. Before C2ND's H2 and before its REG2, the dispatch records (i) that no other study holds a live history-generation reservation, and (ii) which of `hws-store` and `x6zc-store` exist, with their manifests' sha256. G0 checks this record. A parallel store that is created between C2ND's REG and REG2 is covered by REG2 (row 7 or 8 of §6.2). OPEN-2 is closed (§17): history generation of the three rounds runs in separate metered jobs, never concurrent; each round's registry at its registration time covers every store that exists then. The other two rounds must in turn list `c2nd-store` in their registries (their concern; noted for the coordinator).

### 6.6 Namespace admission and hygiene (needle `c2nd-v1`)
C2's `namespace_scan` hard-codes the needle `c2-v1` (`c2_data.NEEDLE`, line 174; lines 245–270). ND reimplements the loop with `contains_scope(path, needle=b"c2nd-v1")` (lines 197–205, which takes the needle as a parameter) and reuses `_walk` and `_scanned` (lines 218–233). **Cross-lineage hygiene:** no C2ND file in C2's scanned set (files named `CONTRACT*.json`, `FREEZE*.json`, `STAGES*.jsonl`, `GATES*.jsonl` anywhere, and `.json/.jsonl/.md/.txt/.py` files inside any `*-store*` directory; lines 175–176, 225–233) may contain the byte string `c2-v1`; otherwise a future C2 G0 would report a FOREIGN hit. The C2ND CONTRACT and records name C2 artefacts by path and sha256, never by scope. The byte copy of this protocol lives in `tools/c2_nd/` only, never in `c2nd-store` (it mentions `c2-v1`). Test T-NAMESPACE-ND checks both directions. ("c2nd-v1" does not contain "c2-v1" as a substring.) The parallel rounds name `c2nd-store` by path and sha256, never by the string `c2nd-v1`, and C2ND files never contain their scope strings. G0 and REG2 report a hit in a parallel store as FOREIGN; T-NAMESPACE-ND includes this case.

### 6.7 Fitting versus test; leakage rules; sealing
- (L1) No DTEST token before ACCEPT.
- (L2) No logit on DFIT outside the M0/M0-D rows; none on DFEAS; closed-form logits count as logits (C2 §12.1 policy).
- (L3) Every threshold, tolerance, seed, g_D, ρ, the U rule, the decoy list, split sizes and the family structure are fixed at the freeze.
- (L4) Nothing is selected on a model output: the refits use activations and oracle quantities only.
- (L5) DVAL endpoint-bearing statistics are sealed: the base A_S and A_comp, the D-NULL A′_S and e′_S, A_M,*, and the KC and KC-R arrays. **KC and KC-R release only PASS/FAIL per (case, model).** The facts these imply (D0 USED on DVAL ⇒ ψ_DVAL > 0.5) were already established by C2 and bear on no C2ND decision threshold (N-R tests 0.90 and 0.50 against ψ; D-DOSE PARTIAL at KC implies only 0.58 < ψ_refit < 0.93 on DVAL; no choice depends on it). V3x′, V3x′-g1 and Y1′ release PASS/FAIL only before the TEST outcome; their means and bounds are sealed with the DVAL endpoint values (mean(A′_full) reconstructs the sealed base A_S).
- (L6) Scratch and pytest basetemp outside the project root (`X:/Downloads/topo-scratch/<job>/`).
- (L7) The C2 store is read-only; its files are checked by sha256 before and after each C2ND job.
- **Never tune on test:** k is the only post-VAL choice, from P1 (VAL SDs, blind). g_D, ρ and U are design constants, not fitted to DVAL or DTEST.

### 6.8 Store and worktree
Store `X:/Downloads/projects/topo-pilot/c2nd-store/` (new; layout as C2 §11 item 1, plus `decoys/` for the construction records and the decoy head arrays): FREEZE.json, AUTH.json, registry/, hist/, oracle/, fits/, decoys/, stages/<S>/, sealed/, GATES.jsonl, STAGES.jsonl, superseded/, logs/, manifests/, a pre-created cpu_ledger.json, nd_meter_bind.py. Execution worktree `X:/Downloads/projects/topo-pilot/topo-pilot-c2nd` on branch `c2nd-<job>` from main b67f332 or later; `PYTHONPATH=<worktree>/src`, the venv interpreter with `-s`; the meter from `<worktree>/tools/x4_oracle_profile` with `--max-cpu inf`.

---

## 7. Outcomes and licences

### 7.1 Q-CODE clauses (mandatory)
- **N-R** (C2 Q-CODE verbatim plus one sentence): *"These outcomes concern the frozen, nuisance-excluding linear code defined by this fit and projector. They do not exclude predictive use of phase information in excluded directions, higher harmonics, interactions, or other encodings. At the linear readout the complement share equals one minus the code share by an exact identity; it is not an independent measurement."*
- **N-M:** C2's M clause, plus every C2-M caveat (skip path, non-natural interchanged state, N2 radial only, position 32, self-repair) and: *"The layer-2 complement includes LayerNorm-scale effects: changing the non-code coordinates rescales the code inside block 3 and at the final LayerNorm, so a code that is the only input the readout reads need not be shown necessary here."* (KM3; MD-1.)
- **Q-CODE-D:** *"These outcomes concern constructed decoys of the three models in which the readout of the registered code is removed or rescaled by an exact head edit, while the code stays in the activations. They show whether the frozen recipe, re-estimated on fresh data, returns NOT_USED when the readout provably ignores the code. The decoy's remaining readout can still depend on the upstream code through the LayerNorm scale; this is outside the registered interchange. They do not show that every form of non-use would be detected, that NOT_USED on a natural model would be correct, or that the C2 result excludes every alternative mechanism."* (The third sentence is MD-7.) Every D licence also discloses the gain ×6 and the head edit.

### 7.2 N-R (necessity at the readout)

| Outcome | Licensed sentence (+ Q-CODE N-R) | Not licensed |
|---|---|---|
| NECESSARY | "In [k] of 3 models, setting every readout coordinate except the six registered code coordinates to its counterfactual value, with the code held, carries between −10% and 10% of the model's signed oracle-aligned response (ψ̂_comp [ ], bounds [ ]) and less than 10% of its centred logit-change energy. With C2's USED, the registered code is sufficient and necessary for this readout response in this sense." | uniqueness of the carrier outside the linear code; other sites, donors, positions |
| COMPLEMENT_LOW_ALIGNED | "…the complement's signed aligned share is below 10% (it may be negative), but either its total logit-change energy was not shown below 10% or the share was not shown above −10%. **This is not a necessity result.**" | necessity; "little response" |
| **CODE_DOMINANT** (expected; an intermediate category, not the rule-6 licence) | "In [k] of 3 models, the complement interchange carries between 10% and 50% of the signed oracle-aligned response (ψ̂_comp [ ], bounds [ ]): the registered code is the main carrier of this readout response, not the only one. At this linear readout this is the same quantity as one minus C2's code share, replicated on fresh histories. [If PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR:] The size of the remainder depends on how 'everything except the code' is defined; under [variant] its category is [variant category] (ψ̂_comp^v [ ]; below 10% only if that category is COMPLEMENT_LOW_ALIGNED)." Owner text: "the code is the main carrier, not the only one". | "necessary"; "sufficient and necessary"; any account of what carries the rest; that the remainder is a property of the code rather than of the registered complement |
| NOT_NECESSARY | "…the complement alone carries more than half…" This contradicts C2's USED on new rows → S13 escalation and an impact review of C2; C2's verdict is not reopened | — |
| MIXED / INCONCLUSIVE/<reason> / FAIL_TECHNICAL | as C2 R6, R7, R0, R0′ | lack of necessity |

**Rule-6 statement (a), COMPLEMENT_POSITIVE_BELOW_MARGIN (owner addendum 25 rule 6):** "In [k] models the complement interchange carries a certified positive share of the signed oracle-aligned response that is below the 10% margin (ψ̂_comp [ ], bounds [ ]): a positive but below-margin contribution of everything except the code." It is reported with NECESSARY or COMPLEMENT_LOW_ALIGNED and is not itself a necessity result unless NECESSARY is also declared.
**Unexpected-case entry, CODE_SHARE_POSITIVE_BELOW_MARGIN** (only inside NOT_NECESSARY): "…and the registered code's own share is certified positive but below 10% (ψ̂ [ ])."
Qualifiers: NEGATIVE_COMPLEMENT(j); PROJECTOR_DEPENDENT_NR(j); HARMONIC_DEPENDENT_NR(j, K) (report-only variant categories, §2.3); SPECIFICITY_NOT_ESTABLISHED; PRECISION_LIMITED(j); DISSENT(j: status).

### 7.3 D (the decoy) and what each outcome means for C2 (MD-12; owner Q4)

| Outcome | Licensed sentence (+ Q-CODE-D) | What it means for C2 |
|---|---|---|
| **DECOY_NOT_USED** (expected) | "In [k] of 3 models, on a decoy that keeps the circle code bitwise in the activations (the same link and registration gates pass) but whose readout ignores it exactly, while responding to the counterfactual at [θ̂′] of the oracle contrast through its other readout directions (gain ×6, fixed in advance), the registered method, re-estimating the code on fresh data, returned NOT_USED (ψ̂′ [ ], upper bounds [ ]; energy share [ ]). The method also returned the constructed answer on every core known case at validation (code-only head: used and necessary; partial dose: partial; base model: used). [Report-only cases: moved code [ ], compensated move [ ].] [Unamplified decoy: response [ ] against the 0.30 gate.]" | The C2 USED is not an automatic consequence of "a history-sensitive code is present and the model responds". The recipe can say no, and re-estimating the projector does not manufacture a share at C2's sample sizes. C2's verdict and licences are unchanged; this result is added beside them |
| DECOY_LOW_ALIGNED | "…the aligned share of the decoy's response attributed to the code was below 10%, but its energy was not bounded…" | The method controls the aligned share, not the energy. C2's USED rests on the aligned share and is unaffected in substance; any future NOT_USED from this recipe needs this caveat |
| DECOY_PARTIAL (a false positive below the USED margin) | "…the method attributed between 10% and 50% of the decoy's response to a code that the decoy provably does not read…" | A decoy share λ corresponds, in C2's own models, to a refit error of about λ(1 − ψ)/ψ ≈ 0.18·λ in ψ (§2.8). The report states both scales and κ_leak. C2's lower bounds (0.354–0.363 nat above 0.50·A_full) would survive a bias below ≈ 0.35, but the method's specificity is not established. **Impact review of C2** (track X wording). Owner escalation (S13). **Every C2 statement carries "specificity not established on the decoy" until the owner decides** (owner Q4 default). The C2 verdict itself never changes, and no record is silently reclassified |
| DECOY_USED (a false positive) | "…the method called an unread code used…" | The C2 USED is not interpretable as evidence of use until the cause is found. **Impact review of C2**; S13; the C2 verdict stays as recorded (frozen), with this result and the caveat attached to every C2 statement until the owner decides |
| KNOWN_CASE_CONTRADICTED(j, case) | "At validation the method returned [category] on [case], whose constructed answer is [known]." | The recipe failed a constructed case. Owner escalation; no discrimination licence |
| EXCLUDED / MIXED / INCONCLUSIVE/<reason> (MODEL_HEADROOM at the frozen gain, KNOWN_CASE_UNRESOLVED, PATCH_MODEL_DEGENERATE, …) | as C2 R6, R0′; an entry-gate failure at the frozen gain is recorded as such, with no redesign (R-C2ND-1) | no information; C2 unchanged |

**Rule-6 statement (b), DECOY_POSITIVE_BELOW_MARGIN:** reported with DECOY_NOT_USED or DECOY_LOW_ALIGNED: "In [k] models the method attributed a small, certified positive share (below 10%; ψ̂′ [ ], bounds [ ]) to a code the decoy does not read." This is the estimation leak made visible; it does not withdraw a DECOY_NOT_USED licence, but it is printed beside it.
Qualifiers: DECOY_LOCATION_DEPENDENT(j) (D-NULL-R's DTEST category ≠ D-NULL's); MOVE_CASE_CONTRADICTED(j, case) (KC-R); NEGATIVE_ALIGNED_CONTRIBUTION(j); KC_TEST_DISAGREES(j, case) (a core case's report-only DTEST category ≠ its known answer; reported, not an outcome); PRECISION_LIMITED(j); DISSENT.

### 7.4 N-M (necessity at layer 2; secondary)
CODE_DOMINANT_M (expected): "In [k] models, the layer-2 complement interchange in the source context carries between 10% and 50% of the signed aligned effect of the full layer-2 interchange (ψ̂_M,comp [ ]); the interaction share is [ι̂_M] (descriptive)." NECESSARY_M (with the −0.10 lower bound), COMPLEMENT_LOW_ALIGNED_M and NOT_NECESSARY_M as §7.2, at layer 2. ROUTED_AROUND as C2 (restricted licence, verbatim). **Rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN:** "In [k] models the layer-2 complement interchange carries a certified positive share below the 10% margin (ψ̂_M,comp [ ], bounds [ ])", plus the C2-M caveats and KM3; reported beside NECESSARY_M or COMPLEMENT_LOW_ALIGNED_M. Every sentence carries the C2-M caveats and the KM3 sentence of §7.1. Not licensed: that block 3 reads the code; any skip/processing split; naturalness of the interchanged state.

### 7.5 Combination with the C2 licences (union displayed; §8.3)
- **The package statement**, only if C2-R USED, N-R CODE_DOMINANT (or NECESSARY) and D DECOY_NOT_USED all hold: "At position 32 of the final readout, setting the six registered code coordinates to the counterfactual's values carries more than half of the model's signed aligned response (C2); setting everything else carries between 10% and 50% (C2ND, fresh histories; the same quantity as one minus the code share); and on decoys of the same models in which the code is present but unread, the same method returns not used (C2ND)." Displayed beside it: **nominal union bound 0.15** (C2-R 0.05, N-R 0.05, D 0.05). Q-CODE and Q-CODE-D appended.
- If the three C2ND families are discussed together: **0.1417** (0.05 + 0.05 + 0.0417). If all six families of C2 and C2ND are discussed together: **0.2917** (C2-R, C2-M, C2-S* 0.05 each, plus 0.1417), displayed as "≤ 0.30". Without N-M (owner Q2 declined): 0.10 and 0.25.
- **Never** "sufficient and necessary" unless N-R is NECESSARY (not reachable, §4.6). Never "the method is validated" in general. No family changes another's outcome (C2 S10), and the favourable family is never selected as "the answer". C2's verdicts are not reopened by any C2ND outcome (S13 governs a conflict).

### 7.6 Never licensed (in addition to C2 §3.5)
Necessity of "the circle" beyond the registered linear code; necessity at other sites or positions; that ψ_comp is independent evidence at the readout; that a decoy result says anything about C2-M or C2-S*; that DECOY_NOT_USED shows the method detects every non-use or excludes the Makelov-type illusion in natural models; that the decoys are plausible language models; that N-M separates block-3 processing from the skip; that the LN-scale shares are causal channels (descriptive only); any claim about the content of the 0.145 remainder; any claim from the report-only cases (D-NULL-R, D-ID, D-NULL₁) beyond their stated results.

---

## 8. Error control and unions (R-C2ND-4 recount; MD-11)

Families are controlled separately, each at nominal 0.05 or less, as C2 §6.3 remark 6 (owner addendum 21). The union is displayed beside any combined statement. Coverage-failure events are F^L_s = {L(s) > μ_s} and F^U_s = {U(s) < μ_s}, each of probability ≤ α under valid individual bounds (nominal, §4.1). Track X's single-0.05-package allocation with 240,000 draws is not adopted (MD-11).

### 8.1 Lemma FW-ND (the recount after the lower bound and the rule-6 statements were added)
*Scope:* per family, the registered TEST statements RESP_j and SPEC_j, the per-model categories, the coarse statements, the rule-6 statements, the nested unexpected-case entry, and the 2-of-3 claims built from them. Operational statuses (LINK, CNHS, support, N2, EXCLUDED, NUMERICAL, INC, NOT_RUN), MIXED and INCONCLUSIVE, the qualifiers (NEGATIVE_COMPLEMENT, PROJECTOR_DEPENDENT_NR, HARMONIC_DEPENDENT_NR, NEGATIVE_ALIGNED_CONTRIBUTION, DECOY_LOCATION_DEPENDENT, MOVE_CASE_CONTRADICTED, KC_TEST_DISAGREES), the report-only N-R variant arrays and categories, KC, KC-R, DX, V3x′-g1, the S2 leak diagnostic and every descriptive interval are **outside** it.

*Common step.* RESP_j is false-and-declared only on F^L_{V3}, and SPEC_j only on F^U_{Y1}: 1 event each. On the complement of F^L_{V3}, every declared statement comes with μ_{V3} > 0, so E[A_full·1_E] > 0.30·E[G·1_E] ≥ 0. Lemma D3 then turns each threshold statement into the sign of a mean (ψ_comp > c ⇔ μ_{Zc^c} > 0; ψ_comp > −0.10 ⇔ μ_{Wc} > 0; ψ_comp > 0 ⇔ μ_{NEGc} > 0), and E[e_full·1_E] > 0 makes the energy statements statements about η.

**N-R: cases on κ = ψ_comp** (events beyond RESP and SPEC; "nested" is CODE_SHARE_POSITIVE_BELOW_MARGIN):

| Truth region | False statements that could be declared, and the event each needs | Events |
|---|---|---|
| κ < −0.10 or κ = −0.10 | NECESSARY: L(Wc) > 0 with μ_Wc ≤ 0, so F^L_Wc. CODE_DOMINANT, NOT_NECESSARY, coarse "> 0.10", nested: F^L_Zc010. Rule-6 (a): L(NEGc) > 0 with μ_NEGc < 0, so F^L_NEGc. (COMPLEMENT_LOW_ALIGNED and coarse "< 0.50" are true.) | 3 |
| −0.10 < κ ≤ 0 | NECESSARY only if η_comp ≥ 0.10: F^U_Vc. CODE_DOMINANT, NOT_NECESSARY, coarse, nested: F^L_Zc010. Rule-6 (a) (κ ≤ 0): F^L_NEGc | 3 |
| 0 < κ < 0.10 | NECESSARY via energy: F^U_Vc. CODE_DOMINANT, NOT_NECESSARY, coarse, nested: F^L_Zc010. (Rule-6 (a) true.) | 2 |
| κ = 0.10 | NECESSARY, COMPLEMENT_LOW_ALIGNED, rule-6 (a): F^U_Zc010. CODE_DOMINANT, NOT_NECESSARY, coarse "> 0.10", nested: F^L_Zc010 | 2 |
| 0.10 < κ < 0.50 | NECESSARY, COMPLEMENT_LOW_ALIGNED, rule-6 (a): F^U_Zc010. NOT_NECESSARY, nested: F^L_Zc050 | 2 |
| κ = 0.50 | NOT_NECESSARY, nested: F^L_Zc050. CODE_DOMINANT, NECESSARY, COMPLEMENT_LOW_ALIGNED, rule-6 (a), coarse "< 0.50": F^U_Zc050 | 2 |
| 0.50 < κ ≤ 0.90 | CODE_DOMINANT, NECESSARY, COMPLEMENT_LOW_ALIGNED, rule-6 (a), coarse "< 0.50": F^U_Zc050. Nested (claims 0.90 < κ < 1): F^L_Zc090 | 2 |
| 0.90 < κ < 1 | F^U_Zc050 (the same statements). Nested true | 1 |
| κ ≥ 1 | F^U_Zc050. Nested (claims ψ > 0): F^U_Zc100 | 2 |

So **≤ 3 events per model from the category, coarse, rule-6 and nested statements, plus RESP 1 and SPEC 1: ≤ 5 per model**. Over three models, P(any declared in-scope N-R statement false) ≤ 15α_NR = **0.05 at α_NR = 1/300** (0.04 if Y1 is inactive). Nesting the unexpected-case entry inside NOT_NECESSARY is what keeps it free: wherever it is false and κ < 0.10, it already needs F^L_Zc010.

**D: cases on ψ′ := E[A′_S·1_E]/E[A′_full·1_E] under the R@D refit projector** (the method's estimand on D-NULL, conditional on DFIT; its construction-subspace value is 0):

| Truth region | False statements that could be declared, and the event each needs | Events |
|---|---|---|
| ψ′ ≤ 0 | DECOY_USED, DECOY_PARTIAL, coarse "> 0.10": F^L_Z010′. DECOY_NOT_USED only if one energy conjunct s ∈ {Vabs′, Vrand′} is false: F^U_s. Rule-6 (b): F^L_NEG′ | 3 |
| 0 < ψ′ < 0.10 | F^L_Z010′; F^U_s. (Rule-6 (b) true.) | 2 |
| ψ′ = 0.10 | F^L_Z010′; DECOY_NOT_USED, DECOY_LOW_ALIGNED, rule-6 (b): F^U_Z010′ | 2 |
| 0.10 < ψ′ < 0.50 | DECOY_USED: F^L_Z050′. DECOY_NOT_USED, DECOY_LOW_ALIGNED, rule-6 (b): F^U_Z010′ | 2 |
| ψ′ = 0.50 | F^L_Z050′; F^U_Z050′ | 2 |
| ψ′ > 0.50 | F^U_Z050′ | 1 |

So **≤ 5 per model**, 15α_D = **0.05 at α_D = 1/300** (0.04 if Y1′ is inactive).

**N-M** (with the −0.10 lower bound in NECESSARY_M and rule-6 statement (c)). Transmission statements τ_M > 0.10 and ROUTED (τ_M < 0.10): ≤ 2 events, both only at τ_M = 0.10. If "τ_M > 0.10" is false, every category needs L(Ztau) > 0, which is the transmission event already counted. If τ_M < 0.10: every declared statement except ROUTED needs L(Ztau) > 0, so all lie in F^L_Ztau: ≤ 1 + RESP. If τ_M = 0.10: F^L_Ztau, F^U_Ztau, RESP (the categories lie in F^L_Ztau): ≤ 3. If τ_M > 0.10: ROUTED false needs F^U_Ztau. The categories and rule-6 (c) behave as N-R without the nested entry: κ_M ≤ −0.10 → F^L_WMc, F^L_ZMc010, F^L_NEGMc; −0.10 < κ_M ≤ 0 → F^U_VMc, F^L_ZMc010, F^L_NEGMc; 0 < κ_M < 0.10 → F^U_VMc, F^L_ZMc010; the other regions as C2 (≤ 2). So ≤ 1 + 3 + 1 = **5 per model**, 15α_NM = **0.0417 at α_NM = 1/360**; unions unchanged.

*Proof of the 2-of-3 step* (C2 Lemma FW, verbatim): a false claim "C holds in ≥ 2 models" needs ≥ 2 declared C_j while fewer than 2 are true, so at least one declared C_j is false. No independence between models is needed (a union bound), which matters because the models share histories and bootstrap indices. The same holds for the "[k] models" rule-6 aggregates. ∎

### 8.2 Per-family nominal levels

| Family | Events per model | α per bound | Ranks (of 20,000) | Nominal family level |
|---|---|---|---|---|
| N-R | 5 (4 if Y1 inactive) | 1/300 | 67 / 19,934 | 0.05 (0.04) |
| D | 5 (4 if Y1′ inactive) | 1/300 | 67 / 19,934 | 0.05 (0.04) |
| N-M (secondary) | ≤ 5 | 1/360 | 56 / 19,945 | 0.0417 |
| C2-R, C2-S* (existing, unchanged) | 4 | 1/240 | 84 / 19,917 | 0.05 |
| C2-M (existing, unchanged) | 6 | 1/360 | 56 / 19,945 | 0.05 |

### 8.3 Unions displayed beside combined statements

| Combination | Nominal union bound |
|---|---|
| The package statement (C2-R + N-R + D) | 0.15 |
| C2ND alone (N-R + D + N-M) | 0.1417 (0.10 without N-M) |
| C2-R + all C2ND families | 0.1917 (0.15 without N-M) |
| All six families (C2-R, C2-M, C2-S*, N-R, D, N-M) | 0.2917, displayed as "≤ 0.30" (0.25 without N-M) |

No independence is assumed. Descriptive intervals and qualifiers are outside every bound. No combined claim selects the favourable family.

### 8.4 T-FAMILY-ND (the exhaustive grid that checks §8.1; independent test author A)
- **Truth states per model:** κ (or ψ′, κ_M) ∈ {−0.5, −0.10, −0.05, 0, 0.05, 0.10, 0.30, 0.50, 0.70, 0.90, 0.95, 1.0, 1.2}; the energy truth ∈ {η < 0.10, η ≥ 0.10} (D: each of Vabs′, Vrand′ true or false); RESP truth ∈ {μ_V3 > 0, ≤ 0}; Y1 ∈ {inactive, active true, active false}; N-M τ_M ∈ {0.05, 0.10, 0.5}.
- **Bound patterns:** for every array of the stream, every (L, U) sign pattern in {(−, −), (−, +), (+, +)} plus "inside the guard", consistent with L ≤ U.
- **Checks:** every false declaration lies in the union of the events listed in §8.1 for its truth state; the number of events used is ≤ 5 per model in every family; the four categories of each family are mutually exclusive; a mean exactly at a threshold is never declared on either side; COMPLEMENT_LOW_ALIGNED never coexists with NECESSARY; the nested entry is never declared outside NOT_NECESSARY; KNOWN_CASE_CONTRADICTED blocks the DECOY_NOT_USED licence and KC-R contradictions do not; an unresolved KC case routes to KNOWN_CASE_UNRESOLVED.

---

## 9. Adaptive budget (addendum 26): stages, CPU forecast, extension rules, 3× pause

**Rate basis [W, measured C2 jobs 0111–0115, single thread]:** S1 724.5 CPU-s (PF suites, a registry of 6.0 M digests, 65,536 history-oracles, Decimal rows); S2 192.1; S3 327.4; S4 761.7 for 305,112 row-forwards (≈ 2.5 ms per row-forward all-in); S5 1,042.3 for 265,176 row-forwards plus REG2 and 99 × 20,000 bootstrap arrays. C2 total 3,114.4 CPU-s = 0.87 CPU-h against a central forecast of 2.1 (jobs/0115 review). The ND forecast scales the measured values, not the C2 heuristics.

**Row-forwards per model [W counts]:**
- DVAL: natural 4 roles 16,384; base X1 interchange arms (including the complement arm) ≈ 16,160; N-M patched F/S/C × 2 arms ≈ 24,228; decoy patched arms on 1,024 rows (D-ONLY, D-DOSE, D-NULL₁ × 4) 12,288; decoy full-forward equivalence 3,072; coordinate decoys 2 × 4 × 1,024 = 8,192. ≈ 80,300, i.e. ≈ 241,000 for three models (0.79 of C2 S4). The X1 check of the three N-R variant complement arms (RC-1) adds 3 × 2 × 1,024 = 6,144 per model and split (≈ 0.013 CPU-h for three models at DVAL, the same at DTEST), inside the low–high ranges; the central values are unchanged.
- DTEST per block: natural 16,384 + base X1 16,160 + D-NULL arms on every eligible row 16,152 + N-M 24,228 ≈ 72,900; once per split M0/M0-D 12,288 + other decoys' low-id arms 16,384. k = 1: ≈ 101,600 per model, ≈ 305,000 in all (1.15 of C2 S5). Decoy natural logits use the bitwise-checked head-only path (`unembed` on the base `ln_final_out`), so they cost no forwards.
- Bootstrap arrays at DTEST: N-R 10 (9 + 1 check) + 6 report-only variant arrays + D 12 + N-M 7 = 35 per model, 105 in all (C2 S5 ran 99), so the S5 bootstrap cost is ≈ 1.06× the C2 measurement, inside the S5 range.

| Stage (addendum 26 role) | Content | CPU-h central | low–high | 3× pause if cumulative measured exceeds |
|---|---|---|---|---|
| A0 feasibility (desk) | §2.5, §4.6 arithmetic; done in this plan | 0 | 0 | — |
| A1 synthetic dry run (pre-freeze; the pilot of the machinery; no learning stage exists, as no weights are learned) | §10.1, metered | 0.40 | 0.25–0.80 | A1: own valve 1.20 under AUTH-IMPL (4,320 CPU-s) |
| S1 | G0, PF, H1, REG, H2, H3, H4, H5, ORACLE-FEAS | 0.20 | 0.14–0.30 | S1–S5 under AUTH-RUN, cumulative from S1: 0.60 (2,160 s) |
| S2 | M0, M0-D, C0c, F1 (2 refits per model + GLS-REF + decoders; the blind leak diagnostic) | 0.05 | 0.03–0.10 | 0.75 (2,700 s) |
| S3 | DFEAS: SUP, L1, R1 (4 codes), N2 (states only), SURVIVAL | 0.07 | 0.04–0.10 | 0.96 (3,456 s) |
| S4 (validation: KC, KC-R, P1) | X1, DX, V3x, V3y, Y1, V3x′, Y1′, V3x′-g1, KC, KC-R (≈ 105 arrays × 5,000), P1 | 0.18 | 0.12–0.27 | 1.50 (5,400 s) |
| S5, k = 1 (main) | REG2, T-PRE, T-PRE-MODEL, RESP-SPEC, NUM, ENDPOINT, REPORT (105 arrays × 20,000) | 0.32 | 0.22–0.48 | 2.46 (8,856 s) |
| each further 4,096-row DTEST block | | +0.21 | 0.15–0.32 | +0.63 per extra block (+2,268 s) |
| **Totals without A1** | k = 1 / 2 / 4 | **0.82** / 1.03 / 1.45 | 0.55–2.2 | 2.46 / 3.09 / 4.35 |

N-M is ≈ 30% of the forwards (≈ 0.25 CPU-h of the central total); without it (owner Q2 declined) the totals fall accordingly.

**Frozen extension rules (blind quantities only):**
1. DTEST size k ∈ {1, 2, 4}, set once by P1 from DVAL SDs and the V3 gate means (C2 §6.7); for D, the oracle contrast mean in place of a decoy gate mean (§4.5). Never more than 4 blocks without an owner decision. A family that fails P1 at N = 16,384 is INCONCLUSIVE/UNDERPOWERED; no further growth.
2. No decoy, dose, gain, constant, family or split is added or changed after the freeze; no stage is extended on any endpoint value. A failed scientific gate is not repaired by adding rows.
3. Technical corrections: at most 2 correction jobs per defect (C2 §11 item 3), each rerunning only the affected stage. Environment reruns (S11) reproduce identical values and do not count.
4. **3× safety valve (addendum 26 item 5):** if the cumulative measured CPU passes 3× the cumulative central estimate of the stages run so far (last column; A1 has its own valve under AUTH-IMPL, and S1–S5 are cumulated from S1 under AUTH-RUN), the coordinator pauses at the next stage boundary and reports to the owner in plain language before continuing. The reference estimate is never reset to evade this rule.
5. **Unavoidable-overrun pause (track X §14):** before launching a stage, the coordinator adds that stage's updated forecast (from the measured rates so far) to the cumulative measured CPU; if the sum exceeds 3× the cumulative central estimate through that stage, the coordinator pauses and reports before launching it.
6. The meter keeps `--max-cpu inf` (measure-only); the C: ≥ 2 GB and X: ≥ 30 GB floors stay. Each model's arrays are processed in bounded memory, without duplicate full activation tensors.

---

## 10. Synthetic dry run and live-state dry check

### 10.1 Synthetic dry run (addendum 25 rule 4; a standing step before freeze; addendum 27 item 2)
- **What:** the full ND driver S1–S5 end to end on three random-initialised `TransformerLM`s with the trained architecture and **planted heads**. `unembed` is set so that a planted 6-d harmonic code of a synthetic phase is read with a known share (≈ 0.85). D0 is then USED and every decoy has a known answer. A synthetic stand-in for the C2 prerequisites (FIT projectors, decoders, N2 fit, frozen oracle constants) is produced by the C2 kernels (`c2_code.problem`, `c2_stats.fit_decoders`, `c2_code.n2_fit`) on the synthetic activations, inside the dry-run store. The synthetic phase replaces the chart phase (the C1′ charts do not fit random models). This is a dry-run-only switch, refused by G0 outside a dry-run store. The histories come from the real cylinder-O process (so the real oracle and registry contracts are exercised on a valid process; track X §7.3), under the scratch scope.
- **Where and how:** `X:/Downloads/topo-scratch/<job>/dry/`, scope **`c2nd-dry-v1`** (coordinator addendum 4 item 4: never the registered streams), outside the project root and outside the C2 inventory, but inside R_ND (§6.2 row 6). **Metered** with threads pinned to 1 (R-0111-1: values can then serve as reproducibility references). No trained weight, no C2 store file and no `c2nd-v1` stream is touched.
- **The run traverses (track X §7.3):** empty-store admission; metered stage entry; registry and synthetic data creation; fit construction and integrity checks; native complement and decoy construction; gate evaluation and variance-only precision selection; ACCEPT and fresh synthetic DTEST generation; RESP/SPEC admission; endpoint formation; guarded decisions, licences and report; interruption and resume; forbidden-access checks (a DTEST read before ACCEPT, a `sealed/` read, a construction-projector use in a method statistic, a KC, KC-R, V3x′, V3x′-g1 or Y1′ value release beyond PASS/FAIL: each refused).
- **Pass criteria:**
  1. every gate runs in the §3 order and the policy refuses out-of-order calls;
  2. every known case of §5.2–§5.3 returns its constructed answer on the planted models; at least one complete branch reaches a known NECESSARY result (planted D-ONLY) and another a known NOT_USED result (planted D-NULL); a random initialisation that merely fails the response gate does not count;
  3. DX and M0-D pass on correct decoys and fail on three deliberately broken ones (wrong g_D, wrong model's projector, transposed P_S) and on the T-ILLUSION Euclidean-projector decoy;
  4. the records, manifests, sealing and the PASS/FAIL-only KC, KC-R, V3x′, V3x′-g1 and Y1′ releases validate;
  5. a planted registry collision (a digest from a C2 TEST-format table) is caught;
  6. the measured CPU per stage is recorded and calibrates the §9 forecast (a blind quantity).

  A failure is fixed before the freeze. The dry run is repeated after any code change that touches a gate. Failure to produce a valid known-answer end-to-end case blocks the freeze.

### 10.2 Live-state dry check (job 0109 rule D-0109-1 / R-0109-1; before every metered stage S1–S5)
On the live store: G0 in full. On a **copy of the store without `sealed/`**, holding the stage's STARTED and AUTH-ADMIT lines and a root `METER_ACTIVE.lock` exactly as at G0 time: G0 item (vii) store admission, including the rejection of near-miss or foreign bookkeeping names. Also: the C2 store files of §2.1 re-hashed and unchanged; the reservation record of §6.5 present; C: ≥ 2 GB, X: ≥ 30 GB; a pre-created `cpu_ledger.json`. Any failure stops the launch.

---

## 11. Reuse and footprint (charter six-field assessment)

### 11.1 Reused unchanged (no edit to `tools/c2_readout`, `tools/c1prime` or `src`; line numbers at b67f332)

| Module | Functions (lines) | Use in C2ND |
|---|---|---|
| `c2_attrib.py` | `ind` 34–39, `half_dot` 43–46, `centre`/`energy` 49–55, `partition` 62–65, `energies` 68–69, `random_ref` 77–84, `pair` 87–92, `null_projector` 96–101, `decomposition` 104–112, `nu_S` 115–117, `cm_replacements` 191–194, `cm_quantities` 197–205, `ln_scale_ratio` 215–217, `ratio_intervals` 221–237, `threshold_arrays` 260–264, `r_arrays` 267–275, `point_ratios` 291–315, `descriptives` 331–369 | every closed form, the C2-M quantities, the descriptive intervals |
| `c2_code.py` | `harmonics` 37–43, `standardise` 46–47, `fwl` 50–68, `f1_fwl` 71–80, `ledoit_wolf` 83–84, `gls` 104–128, `gls_identities` 136–161, `interchange` 164–168, `code_phase` 176–179, `zero_code_threshold` 182–185, `r1` 189–214, `n2_fit` 218–235, `n2_gate` 243–260, `problem` 287–307 | the refits R@D, R@T; R1; N2 |
| `c2_stats.py` | `gls_ref` 185–202, `delta_p` 205–208, `fit_decoder` 234–247, `decoder_features` 250–257, `l1` 275–292, `_summaries` 310–323, `f1_problem` 370–379, `fit_decoders` 385–389, `l1_split` 392–395 | GLS-REF, decoders, P1 kernels with ND seeds (`p1` 326–349 hard-codes C2 seeds, so the ND wrapper calls `_summaries`) |
| `c2_model.py` | `load_models` 35–48, `activations3` 80–82, `natural_pass` 85–87, `patched_logits` 90–99, `helmert` 103–111, `readout_basis` 114–136 (head-edit decoys), `readout_coords` 139–140, `closed_logits` 143–145, `placed` 148–151, `identity_patch` 155–162, `readout_identity` 174–177, `kappa_x1` 180–184, `two_route` 192–204, `symbol_order_*` 207–225, `m0` 228–257, `x1` 261–282 | M0, X1, patches; an ND basis adapter only for the coordinate wrapper |
| `c2_decide.py` | `stream_bounds` 38–46, `guard` 49–50, `beta_A` 58–62, `beta_E` 65–72, `sign` 75–76, `stream_guards` 79–92, `r_model` 137–145, `overall` 182–202 (R semantics), `endpoint_status` 212–229 | D family rules; bounds and guards for all families |
| `c2_oracle.py` | `load_process` 31–58, `h1_static` 61–83, `oracle_split` 113–134, `nuisance5` 137–145, `d_named` 148–149, `eligibility` 156–163, `phi_star` 194–198, `reason_flags` 201–214, `h3` 264–300, `decimal_rows` 303–330 | the oracle on the new splits; ORACLE-FEAS (i) |
| `c2_data.py` | `k_y` 74–77, `y_donor` 80–90, `donors4` 93–95, `role_arrays` 98–104, `history_table` 115–130, `table_digests` 137–141, `coverage_tally` 168–170, `file_sha` 189–194, `contains_scope` 197–205 (needle parameter), `_walk` 218–222, `_scanned` 225–233, `store_admission` 281–293 | donors, tables, hashing, admission, registry reader `c2` |
| `c2_registry.py` | `x6_source` 99–128, `token_sources` 132–158, `inventory` 192–211, `Registry` 306–357, `separation` 360–386, `first_token_ok` 389–394 | R_ND and separation (`build` 241–302 accepts only the C2 version names, so an ND wrapper composes the same readers) |
| `c1prime/*`, `x4_circle_history/*`, `src` | as C2 §13.1 | unchanged |
| `src/topo_pilot/learner/model.py`, `patch.py` | `TransformerLM.forward` 108–126; `forward_with_patch` 66–118 (`_check` 34–63) | the decoys are model instances or `ln_final` wrappers; no src change |

### 11.2 Six-field assessment
1. **Reused unchanged:** §11.1.
2. **Not reusable unchanged (verified at b67f332):**
   - `c2_data.history_generator`, `sequence_ids` and `sample_block` read `cc.SCOPE` = `c2-v1` (lines 37–55), so ND needs thin samplers with scope `c2nd-v1`;
   - `namespace_scan` hard-codes the C2 needle (line 174; lines 245–270), so the ND scan loop passes the needle to `contains_scope`;
   - `c2_driver.LogitPolicy` (lines 50–73) reads the module-level C2 `GATE_ORDER` (lines 27–31), so ND needs its own policy (≈ 30 lines) with the §3 order; no monkey-patching of a frozen module;
   - `c2_registry.build` accepts only C2 version names (`VERSIONS`, line 32);
   - `c2_stats.p1` hard-codes C2 seeds;
   - `c2_model.readout_basis` requires `ln_final.weight`, so the coordinate wrapper needs an adapter.
3. **Missing capability:** the decoy constructions, `decoy_sha64`, M0-D and DX; the coordinate wrapper; the N-R and N-M arrays and rules; the rule-6 statements; KC and KC-R; the LN-scale and leak descriptives; the registry readers `c2`, `c2scratch`, `hws`, `x6zc` and the inventory adapter; ORACLE-FEAS; the ND stage functions, records, sealing and CLI; the dry-run planted models.
4. **Smallest change:** one new package `tools/c2_nd/` and one test directory `tests/c2_nd/`; nothing else edited.
5. **Invariants:** `tools/c2_readout` bitwise at H″; the C2 store read-only and re-hashed; float64, single thread; donors keep w32; one symbol-order convention; the refit projector, never the construction projector, in every method statistic; X1 and DX ephemeral; DVAL endpoint values sealed; KC, KC-R, V3x′, V3x′-g1 and Y1′ release PASS/FAIL only before the TEST outcome.
6. **Regression and next extension:** regression: the PF suites including `tests/c2_readout` unchanged, the dry run, X1/DX on real data. Next (not built): decoys for C2-S* and for the layer-2 code; a natural-pairs donor family; position profiles (`STRONGER_EVIDENCE_OPTIONS_HE.md` §2.4); the remainder decomposition (§2.2 there) as its own preregistered study.

### 11.3 Files (every `.py` ≤ 400 lines; 11 modules, ≈ 3,150 lines planned)

| File | Contents | Budget |
|---|---|---|
| `tools/c2_nd/API.md`, `PROTOCOL_C2ND_v1.md` (byte copy of C2ND-DESIGN-v1 = C2ND-FROZEN-v1; G0 checks its sha256 against `FREEZE.json`), `CONTRACT.json` (thresholds, seeds, g_D, ρ, every C2 artefact sha256 of §2.1, `state_sha`, the H″ blob list, the registry sources of §6.2), `TEST_PLAN.md` | contract first | — |
| `nd_config.py` | contract loading, constants, Fractions, ranks, seeds, paths, sys.path convention (as `c2_config`) | ≈ 150 |
| `nd_data.py` | `c2nd-v1` samplers and ids, tables through `c2_data`, the needle scan and hygiene check, store admission | ≈ 220 |
| `nd_registry.py` | readers `c2`, `c2scratch`, `hws`, `x6zc`; R_ND and R′_ND builds composing the `c2_registry` readers; the inventory adapter; separation; the reservation record check | ≈ 280 |
| `nd_decoy.py` | head edits (D-NULL, D-NULL₁, D-ONLY, D-DOSE), V₀, U and T, the coordinate wrapper and its basis adapter, `decoy_sha64`, M0-D (incl. the 1e-10 adapter identities), DX | ≈ 340 |
| `nd_attrib.py` | N-R arrays (A_comp direct and by subtraction, e_comp, Wc, Zc090, Zc100; the report-only R_E, R_K1, R_K2 variant arrays), N-M arrays (ψ_M,comp, WMc, ι_M), D arrays with M′, the leak, canonical angles and κ_leak, the LN-scale decomposition | ≈ 300 |
| `nd_decide.py` | `nr_model`, `nm_model`, D through `c2_decide.r_model`, the rule-6 statements (a)–(c) and the nested entry, the N-R variant categories and qualifiers, KC and KC-R rules, overall rules, qualifiers, licences with Q-CODE / Q-CODE-D, the union display | ≈ 380 |
| `nd_driver.py` | the ND `LogitPolicy`, records, sealing, G0, release binding, meter check, `run_stage`, CLI | ≈ 350 |
| `nd_stage_pre.py` | S1–S3 step functions in §3 order (incl. ORACLE-FEAS) | ≈ 400 |
| `nd_stage_val.py` | S4 step functions | ≈ 380 |
| `nd_stage_post.py` | S5 step functions, REPORT, POST-DESC | ≈ 400 |
| `nd_dry.py` | planted synthetic models and the synthetic C2-prerequisite fixture (refused by G0 outside a dry-run store) | ≈ 200 |
| `tests/c2_nd/test_a_*.py` (≤ 5 files; algebra, statistics, decoy maths: T-N1, T-NEC-KNOWN, T-RULE6, T-PROJ-ND, T-COPY, T-MOVE, T-DOSE, T-LEAK, T-GAIN, T-LNSCALE, T-ILLUSION, T-EDGE, T-FAMILY-ND, T-BOOT-ND, T-LADDER-ND), `test_b_*.py` (≤ 5 files; models, gates, operations: T-DECOY-EXACT, KM1–KM4, T-RESP, T-POLICY-ND, T-NAMESPACE-ND, T-REG-ND (a planted collision with a C2 TEST digest → FAIL_TECHNICAL/LINEAGE; an unreadable parallel store → REGISTRY_INCOMPLETE; a HIST_*.npz under a test_* directory is skipped by the row-9 scan, and a non-C2-format HIST_*.npz outside one is listed NON_C2_FORMAT without failing the registry), T-G0-ND, T-SEAL-ND (KC, KC-R, V3x′, V3x′-g1 and Y1′ release PASS/FAIL only), T-METER, T-SIZE), `AUTHORSHIP_A.md`, `AUTHORSHIP_B.md` | see §11.4 | ≤ 400 each |
| store-local `nd_meter_bind.py` | as `c2_meter_bind.py` | outside the repo |
| `docs/code_index/` | regenerated by `.venv/Scripts/python.exe tools/build_code_index.py` in its own `docs(index): …` commit after the code commit (CLAUDE.md) | — |

### 11.4 Independent test authors (C2 §13.3 pattern; binding)
Two independent authors, A (algebra and statistics) and B (models, gates and operations), write the tests from C2ND-DESIGN-v1 (sha256) and `API.md` only. They never read `tools/c2_nd/*.py`, never execute anything, and their files are never formatted by a tool. The implementer does not author the acceptance tests. Protected paths for the freeze diff: `src`, `pyproject.toml`, `tools/{c1prime, c1prime_registry, x4_circle_history, x4_oracle_profile, k4b, x6_stage1, c2_readout, c2_nd}`, `tests/{…the C2 list…, c2_readout, c2_nd}`; the allowlist has `A` entries for the files above only.

---

## 12. Stop rules and lineage
C2 §8 S1–S14 and §11 apply with these substitutions. The scope is `c2nd-v1`, the store `c2nd-store`. S3 and S6 include g_D, ρ, the U rule and the decoy list.
- **S13 also triggers on** NOT_NECESSARY, DECOY_PARTIAL, DECOY_USED, KNOWN_CASE_CONTRADICTED, or a D0 contradiction: stop and wait for the owner. C2's verdicts are never reopened by a coordinator ruling.
- **S12 also covers:** a write to the C2 store; use of the construction projector in a method statistic; a KC, KC-R, V3x′, V3x′-g1 or Y1′ value (beyond PASS/FAIL) released before the TEST outcomes; a registry read of a payload, `state.pt` or `sealed/` file.
- From track X §15: no retry seeks a different scientific outcome; a correction that changes an already computed scientific quantity needs an owner disposition and a revised protocol; a result that materially challenges a published claim is escalated before any publication changes; leakage → INVALID, evidence preserved, review awaited.
- Final outcomes are never rerun; supersede is append-only; at most 2 corrections per defect.

---

## 13. Authorisation steps
Owner addendum 27 authorises planning only. Addendum 24's C2 AUTH does not transfer to this study (track X §1).
1. **Now:** clean-context review (addendum 28) of this merged plan, result-blind; the coordinator's confirmation and acceptance as design freeze candidate C2ND-DESIGN-v1 (sha256 recorded); OPEN-1 to OPEN-3 closed (§17).
2. **Owner AUTH-IMPL (owner Q5, first part):** an owner addendum naming the C2ND-DESIGN-v1 sha256 and the dry-run budget → `AUTH_IMPL.json`: implementation, tests (independent authors, written from C2ND-DESIGN-v1) and the metered synthetic-only dry run (≈ 0.4 CPU-h central, 0.25–0.80, 3× pause at 1.20). This is not an AUTH for real data.
3. **Implementation job:** `API.md` → independent tests A/B (from C2ND-DESIGN-v1 and `API.md`, §11.4) → modules → full suite (detached) → code freeze H → code index commit. Then the synthetic dry run (§10.1), reviewed.
4. **Final freeze C2ND-FROZEN-v1:** byte-identical to C2ND-DESIGN-v1; `FREEZE.json` binds its sha256, H and the dry-run report sha256; any text change → a new candidate and review. CONTRACT and the parallel stores' readers (§6.2) recorded.
5. **Owner AUTH-RUN (asked again after the freeze):** an owner addendum naming the C2ND-FROZEN-v1 sha256 and the staged budget of §9 (≈ 0.8 CPU-h central at k = 1, up to ≈ 1.5 at k = 4, with the 3× pause) → `AUTH.json`, for S1–S5.
6. **Stage jobs** S1, S2, S3 + S4, ACCEPT, S5, each with the reservation record (§6.5) and the live-state dry check before launch (§10.2), a review after, and the 3× valve at every boundary.

---

## 14. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Necessity at the readout is a mirror of ψ | it could be over-read as new evidence | Lemma N1 in every N-R licence; N-M carries the non-linear test; §1.5 |
| The expected partial result | a 15% complement exceeds the 10% margin, so "necessary" is unreachable for the registered K = 3 GLS complement | stated in advance (§1.4, §4.6); owner Q1; never renamed after the data |
| The remainder depends on the complement definition | C2's R_E and R_K1 variants put it at 6–9%, so "≈ 15%" could be read as a property of the code | report-only variant categories, qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR, licence wording (§2.3, §7.2), owner Q1 |
| The decoy's answer is nearly determined | low surprise value; looks like a demonstration | stated (§1.5); the refit projector and the core known cases make it a calibration of the recipe, not a tautology; the leak, canonical angles and rule-6 statement (b) are reported |
| g_D = 6 makes the decoy's predictive unnatural | "a decoy no model would learn" | the claim is about the recipe's specificity, not about plausible models (Q-CODE-D); D-DOSE and D-ONLY cover milder edits; the unamplified result is reported |
| Opened C2 data informed g_D and ρ | perceived tuning | disclosed (§1.4, §2.5); Lemma DG (the share does not depend on g_D); thresholds unchanged; no C2ND data used |
| Assay entry failure at the frozen gain | the decoy cannot reach NOT_USED | recorded as such, no redesign (R-C2ND-1); desk margins ≥ 2.6× |
| Leak magnified by ψ/(1 − ψ) | a false PARTIAL or LOW_ALIGNED | §2.8 scale statement, S2 blind diagnostic, dual-scale reporting |
| Ledoit–Wolf non-equivariance moves D-ID or D-NULL-R | a report-only contradiction that is not a method failure | report-only (R-C2ND-3); categories, not values, are checked; T-MOVE quantifies |
| U badly conditioned (L_BV₀ near rank 5) | coordinate decoys unusable | construction gate; those report-only cases NOT_COMPUTED; D-NULL unaffected |
| LayerNorm scale (layer 2; the decoy's upstream channel) | the N-M complement includes rescaling; the decoy can still depend on the upstream code through σ | KM3; LN ratios and shares reported; licence wording (§7.1) |
| Registry misses a store created after C2, or a parallel round's store | leakage risk | the readers of §6.2; REG2 rebuilds; the reservation schedule (§6.5); INCOMPLETE fails closed |
| C2ND records containing "c2-v1" | a future C2 G0 would fail | hygiene rule and T-NAMESPACE-ND (§6.6) |
| C2 store altered or unavailable | broken bindings | G0 sha256 checks before and after each job; read-only |
| Nominal inference | bootstrap approximation and Monte Carlo error (≈ 12% in the tail) | stated (§4.1); event counting exact conditional on valid bounds |
| CPU larger than forecast | budget surprise | measured C2 rates; the 3× pause at stage boundaries and before an unavoidable overrun |
| Defects late in S5 (C2 needed 4 S1 attempts) | delay | dry run, live-state dry check, ≤ 2 corrections per defect |
| A KC contradiction from D0 | apparent failure to reproduce C2 | escalation (S13); never reclassified |

---

## 15. Owner questions (with defaults; from the MERGE decisions)
1. **Necessity lines.** Keep the 10% / 50% lines, so the expected answer is "the code is the main carrier (about 85%), not the only one (the rest carries about 15%)", and "sufficient and necessary" cannot be claimed? With C2's two registered alternative definitions of 'everything else', the rest is about 6–9%, so the answer depends on that definition, and the result will say so. **Default: keep.**
2. **Layer-2 necessity.** Include the one necessity test that is not just the mirror of the existing result? It adds about 0.25 CPU-h, has synthetic known cases only, and is also expected at about 14%. **Default: include, as a secondary result.**
3. **Decoy amplification.** Accept a decoy whose remaining readout is scaled ×6, fixed now and disclosed, so that it still passes the response check? The scaling does not change the share the method measures. The unscaled version fails the response check in all three models, and that is reported. **Default: accept.**
4. **What a decoy failure does to C2.** If the method calls the decoy "used" or "partly used", should every C2 statement carry "specificity not established" until the owner decides, with the C2 verdict itself never changed? **Default: yes.**
5. **Two-step authorisation.** First, AUTH-IMPL: implementation, tests and the metered synthetic-only dry run (≈ 0.4 CPU-h, pause at 1.20) on the design freeze candidate C2ND-DESIGN-v1. Then, after the final freeze C2ND-FROZEN-v1, AUTH-RUN: the staged run (≈ 0.8 CPU-h central, up to ≈ 1.5), with a plain-language pause if measured use passes 3× the estimate at any stage boundary. **Default: approve AUTH-IMPL now; ask again for AUTH-RUN after the freeze.**

---

## 16. Desk arithmetic [W] (from opened C2 records and exact algebra; no data)
- E[A_full·1_E] (1729, TEST) = (Z010 mean − Z050 mean)/0.4 = (0.771824 − 0.360531)/0.4 = 1.028 nat; E[A_S·1_E] = 0.36053 + 0.514 = 0.875; ψ̂ = 0.851 ✓.
- E[e_full·1_E] (1729) from the Vabs mean 105.53 and η_S 0.9046: 105.53/0.8046 = 131.2 nat².
- ψ_comp = 1 − ψ̂: 0.1494, 0.1461, 0.1443; ψ_Γ + ψ_rest (1729) = 0.0018 + 0.1475 = 0.1494 ✓.
- θ_full = 0.946924 / 0.958800 / 0.955590; θ_S = 0.805484 / 0.818717 / 0.817726 (C2 S5 report, TEST R point blocks).
- Naive (unamplified) decoy θ′ = (1 − ψ)θ_full: 0.1415, 0.1401, 0.1380 (all < 0.30). D-NULL (g_D = 6): 0.849, 0.841, 0.828. g_min for θ′ ≥ 0.60: 4.24, 4.28, 4.35.
- D-DOSE (ρ = 0.92, g_D = 6): 1 − ρψ = 0.21745, 0.21441, 0.21276; ψ′ = 0.3129, 0.3186, 0.3218; θ′ = 1.235, 1.234, 1.220. For ψ ∈ [0.80, 0.90]: ψ′ ∈ [0.242, 0.419].
- D-ONLY θ′ = θ_S = 0.8055, 0.8189, 0.8180.
- N-M (C2 TEST, descriptive): ψ_M 0.8391, 0.8443, 0.8462; ψ_M,C 0.1409, 0.1437, 0.1404; ι_M = 0.0200, 0.0120, 0.0134.
- Energy: η_comp ≥ (1 − √0.905)² = 0.0024.
- Ranks (`c1_means.rank_for` = ⌈n·p⌉): α = 1/300 → ⌈66.67⌉ = 67 and ⌈19,933.33⌉ = 19,934 (67 + 19,934 = 20,001, symmetric); α = 1/360 → 56 / 19,945; α = 1/60 at 5,000 → 84 / 4,917.
- z_{1−1/300} ≈ 2.713; z + z_{0.80} = 3.555; N = 4,096 passes P1 for SD ≤ 6.4/3.555 = 1.80 nat.
- Family levels: 15/300 = 0.05; 12/300 = 0.04; 15/360 = 0.0417. Unions: 0.05 + 0.05 + 0.05 = 0.15; 0.05 + 0.05 + 0.0417 = 0.1417; 0.15 + 0.1417 = 0.2917.
- 3× thresholds: A1 alone 3 × 0.40 = 1.20 CPU-h (under AUTH-IMPL); S1–S5 cumulative from S1 (under AUTH-RUN) 3 × (0.20, 0.25, 0.32, 0.50, 0.82) = 0.60, 0.75, 0.96, 1.50, 2.46 CPU-h; +3 × 0.21 = +0.63 per extra block.

---

## 17. OPEN items (values that could not be fixed from manifests, stage records or writer code; all closed by coordinator rulings, 2026-10-26)
- **OPEN-1 (parallel stores and their readers). Closed: unreadable or unfrozen parallel store → REGISTRY_INCOMPLETE.** A parallel-round store (`hws-store`, `x6zc-store`) that exists without a frozen registry reader makes the registry fail closed (INCOMPLETE). Background as recorded in v1: The final paths, history file layouts and registry readers of `coord-history-world-sweep-20261026` (planned `X:/Downloads/projects/topo-pilot/hws-store/`, `hist/<stage>/<key>.npz`, uint8 [n, 32] canonical tokens, per its track L §10.3) and `coord-x6zc-placebo-20261026` (planned `X:/Downloads/projects/topo-pilot/x6zc-store/`; its history format is not fixed in its plan). Neither round has a merged protocol yet. To be copied from HWS-MERGED/X6ZC-MERGED (or their frozen versions) into the C2ND CONTRACT before the freeze. **Default if still open at freeze:** a parallel store that exists at REG or REG2 time without a frozen reader makes the registry REGISTRY_INCOMPLETE (fail closed), and C2ND waits.
- **OPEN-2 (reservation schedule). Closed: history generation of the three rounds in separate metered jobs, never concurrent; each registry covers every store existing at its registration.** Background as recorded in v1: the order and dates in which the three addendum-27 rounds draw histories (R-C2ND-6, R-HWS-7). The coordinator sets it; C2ND only requires that no other reservation is live during its H2 and REG2 (§6.5).
- **OPEN-3 (code-index freshness check). Closed: the coordinator runs `--check`.** It is a coordinator task, not a protocol item. Background as recorded in v1: `tools/build_code_index.py --check` was not run during this planning step, because running Python was not permitted. All citations were verified directly in the source at b67f332.
- **Ruling on the two "move" known cases (confirmed).** D-NULL-R and D-ID are report-only: own report-only gate KC-R; a contradiction adds a qualifier only (MOVE_CASE_CONTRADICTED). v1 already conformed (§3 row 25, §5.3).

Every sha256 and key name requested by R-C2ND-5 was found (§2.1). Values that only exist after implementation (the C2ND protocol, CONTRACT, API and H sha256, the `decoy_sha64` values) are freeze-time fields, not OPEN items.

---

## 18. Provenance
- **Inputs read:** the request; track L (base); track X; the COMPARISON; the MERGE; owner addenda 25–27; `C2-FROZEN-v2.md` §2.1–§2.6, §2.9, §2.12, §3, §6 (by heading); coordinator addendum 4; `jobs/0115/review.md`, `jobs/0111/review.md`, and job 0104/0105/0109/0111/0115 records by search; the MERGE files of `coord-x6zc-placebo-20261026` and `coord-history-world-sweep-20261026`, and the store and scope sections of their track L plans (no output of the other track of *this* id was used beyond the merge inputs).
- **Code read at b67f332:** `tools/c2_readout/{c2_stage_pre (lines 125–294), c2_stage_base (lines 35–36, 96–97, 216–222), c2_code (lines 50–68, 104–128, 230–235), c2_stats (lines 213–231, 255–270, 382–396), c2_model (lines 114–137), c2_data (lines 33–112, 113–297), c2_decide (lines 36–52), c2_config (lines 50–55, 97–115), c2_driver (lines 27–31), c2_registry (definitions list)}`; `tools/c1prime/c1_means.py` (lines 57–79); `src/topo_pilot/learner/model.py` (lines 84–126); `patch.py` (lines 34–63, 88–118); C2 `CONTRACT.json` (models, hashes, registry). Every `def` line cited was checked by a definition listing. `git diff 0a67c5a b67f332 -- tools/c2_readout src/topo_pilot/learner` and `git diff 3e234b3 b67f332 -- tools/c2_readout` are empty, and every `tools/c2_readout` git blob at b67f332 equals the C2 `FREEZE.json` record.
- **Records read (JSON and listings only):** `c2-readout-store/manifests/{0112, 0115, 0115.accepted}.json`, `FREEZE.json`, `fits/FIT_{1729,2718,3141}.json`, `oracle/ORACLE_FROZEN.json`, `superseded/*/SUPERSEDED.json`; directory listings of the C2 store, `superseded/`, and the scratch dry-run and live-copy `hist/` directories (file names only). sha256 values of JSON and Markdown files were computed with `sha256sum`; for every array file the sha256 was taken from the manifests, never computed.
- **Not read or hashed:** any `payload.npz`, `state.pt`, `*.npz` or `*.npy` content, anything under a `sealed/`, `topo-pilot/00_READ_ME_FIRST_*`, `topo-pilot/docs/research_summary/`.
- **No Python, tests, sampling or model runs; no git writes; only this file was written.**

---

## 19. Changes from track L
1. **Gain renamed and ruled (R-C2ND-1; MD-4).** The decoy gain is g_D = 6, fixed now and disclosed as chosen with knowledge of the opened C2 values. Added Lemma DG (every D decision except RESP′ is gain-invariant; v2: SPEC′ also depends on g through whether Y1′ is active, RC-7). Added the unamplified decoy D-NULL₁ and the report-only gate V3x′-g1. "No redesign if the frozen-gain decoy fails an entry gate" stated. No pilot split, no gain menu.
2. **Refit, never the construction projector (R-C2ND-2; MD-5).** Kept, and made explicit as an S12 violation. The estimation leak is reported as such.
3. **"Exact" corrected (R-C2ND-2; comparison error L-2).** D-ONLY's and D-NULL-R's known answers are "exact for the construction subspace; robust by margin under the refit", not "exact".
4. **Coordinate variants report-only (R-C2ND-3; MD-6).** D-NULL-R and D-ID moved from the decision-bearing KC gate to a new report-only gate KC-R, without an error budget or decision effect (qualifiers MOVE_CASE_CONTRADICTED and DECOY_LOCATION_DEPENDENT). Their construction failure makes them NOT_COMPUTED.
5. **Full-logit nullity (MD-6).** V₀ is a basis of ker(M) (dim ≥ 91), not ker(CM); hence MU = 0 and D-NULL-R's logits equal D-NULL's up to a fixed vector. U is shown basis-independent.
6. **Lower bound in NECESSARY (R-C2ND-4; MD-2; comparison gap L-3).** NECESSARY now requires L(Wc) > 0 (ψ_comp > −0.10), also for NECESSARY_M. COMPLEMENT_LOW_ALIGNED is redefined as "aligned complement below 10%, NECESSARY not declared".
7. **Rule-6 labels fixed (R-C2ND-4; MD-3; comparison error L-1).** CODE_DOMINANT is no longer called the rule-6 licence. Two rule-6 statements are registered: COMPLEMENT_POSITIVE_BELOW_MARGIN and DECOY_POSITIVE_BELOW_MARGIN. Track X's native 0 < ψ < 0.10 statement is kept as a nested unexpected-case entry (CODE_SHARE_POSITIVE_BELOW_MARGIN) inside NOT_NECESSARY. (v2: a third, rule-6 (c) for N-M, added per coordinator ruling; item 21.)
8. **Error events recounted (R-C2ND-4; MD-11).** N-R and D now have ≤ 5 events per model (track L had 4), so α_NR = α_D = 1/300 (ranks 67 / 19,934) instead of 1/240. N-M stays at 1/360. Case tables for N-R, D and N-M are given (§8.1). The T-FAMILY-ND grid is specified (§8.4).
9. **Unions recomputed (R-C2ND-4).** 0.15 (package), 0.1417 (C2ND), 0.2917 (all six), with the "without N-M" values, displayed beside any combined statement (§8.3).
10. **Artefact bindings completed (R-C2ND-5).** Full sha256 for every reused C2 file, the H″ blob list, the model `state_sha` values, and the FIT/DEC key names from the writer code (§2.1). Track L gave prefixes only.
11. **Registry widened (R-C2ND-6; MD-10).** Added the superseded C2 attempts, the C2 dry-run scratch stores (0104, 0105), the live-state copies, C2ND's own dry run, a scratch name scan, and the stores of the two parallel rounds, with execution-time reading rules and the reservation scheduling (§6.2–§6.5).
12. **Layer 2 kept as secondary (R-C2ND-7; MD-1)**, with track X's fallback text if the owner declines, and the KM3 sentence in the N-M licence.
13. **LN loophole sentence (MD-7)** added to Q-CODE-D and §2.9.
14. **Gate additions (MD-8).** ORACLE-FEAS (oracle θ = 1 identity; 2× headroom at 0.02 nat) in S1; the 1e-10 adapter identities in M0-D.
15. **Fixtures added (MD-9).** T-ILLUSION (the operator-illusion fixture), T-EDGE (threshold edges), T-RULE6, T-RESP, T-GAIN; the negative-complement case in T-NEC-KNOWN.
16. **Impact wording (MD-12; owner Q4).** DECOY_PARTIAL and DECOY_USED trigger an "impact review of C2" and the automatic "specificity not established" caveat on every C2 statement until the owner decides; the C2 verdict never changes; no record is reclassified. NOT_NECESSARY also triggers an impact review.
17. **Budget (MD-13).** Track L's forecast and per-boundary valve kept, with CPU-s equivalents and track X's "pause before an unavoidable overrun" rule. Array counts updated (90 at DTEST in v1; 105 in v2 with the RC-1 variant arrays).
18. **Numerics (MD-15).** The complement computed directly and by subtraction in X1; the complement's guard includes the code-projector error. Track L's "no guard term for the decoy matrix" kept.
19. **Dry run (track X §7.3).** The traversal list, the NECESSARY and NOT_USED end-to-end branches, interruption/resume and forbidden-access checks added. Failure to produce a known-answer branch blocks the freeze.
20. **Authorisation (MERGE owner Q5; track X §1).** Two owner steps made explicit (§13); addendum 24's AUTH does not transfer. Owner questions replaced by the MERGE list with defaults (§15).
21. **Rule-6 statement (c) for N-M, COMPLEMENT_M_POSITIVE_BELOW_MARGIN.** Added per coordinator ruling; 5 events, 0.0417.
22. **Citations re-based** from 0a67c5a to b67f332 (the code is unchanged); the request's structure (questions and claims; design; gates; known cases; data; outcomes; error control; budget; dry run; reuse; authorisation; risks; owner questions) adopted as the section order.

---

## Change log v1 → v2

Writer step for coordinator Claude 243a611b, 2026-10-26. Inputs: `C2ND-MERGED-v1.md` (sha256 `749760fe…2c71`), the clean-context review `coord-c2nd-review-20261026.claude-reviewer.md` (sha256 `e0fc9b60…9318`; Codex frozen by owner, addendum 28), the rulings `coord-c2nd-review-20261026.rulings.md` (sha256 `5a41daf0…9c2f`; every RC accepted) and the coordinator's rulings on OPEN-1 to OPEN-3. Checked for placement only (no Python, no tests, no array or `sealed/` file opened or hashed): `c2_decide.variant_category` (line 164), `c2_model.kappa_x1` / `x1_attainable` (lines 180, 187), `c1_chart.c0_val` (line 161) and its C2 use (`c2_stage_pre.py` line 231; C2 §6.6 "3 direct constructions, ledger limit 3"), and `c2-readout-store/fits/FIT_1729.json` "delta", which holds δ_P for `R_E`, `R_K1`, `R_K2`. Nothing outside the items below was changed.

**Header.** STATUS line replaced by: "STATUS: MERGED v2, design freeze candidate (pending confirmation). Next: clean-context result-blind review (addendum 28), coordinator acceptance as design freeze candidate C2ND-DESIGN-v1 (sha256 recorded), owner AUTH-IMPL (implementation, tests, synthetic-only dry run; ≈ 0.4 CPU-h central, 3× pause at 1.20), implementation and dry run, final freeze C2ND-FROZEN-v1 binding H and the dry-run report sha256, then owner AUTH-RUN for S1–S5. Nothing here authorises a run." (RC-5 (a)). Title "C2ND-MERGED-v1:" → "C2ND-MERGED-v2 (supersedes v1; see "Change log v1 → v2" at the end):". Plan-id row extended ("v2 applies the result-blind review RC-1 to RC-12 and closes OPEN-1 to OPEN-3 under the coordinator's rulings"); rows "Supersedes" (v1 sha256) and "Review applied" (review and rulings sha256) added; "Owner rules" row gains addendum 28 (`650d8b6b…666c`; Codex frozen, reviews by clean-context Claude); "Authorises" row: "(go-ahead for implementation and dry run; AUTH after freeze)" → "(AUTH-IMPL for implementation, tests and the synthetic-only dry run on C2ND-DESIGN-v1; AUTH-RUN after the final freeze C2ND-FROZEN-v1)".

### RC-1 (MAJOR): the N-R remainder depends on the complement definition
- **§1.4**, appended verbatim: "C2's registered variants give, on C2 TEST, 1 − ψ = 0.093/0.077/0.072 (R_E, Euclidean complement), 0.062/0.059/0.057 (R_K1), 0.156/0.150/0.158 (R_K2) [W]. The ≈ 0.15 remainder is a property of the registered K = 3 GLS complement, not of the code alone. Expected: PROJECTOR_DEPENDENT_NR and HARMONIC_DEPENDENT_NR(K = 1) in all three models."
- **§4.2 N-R**, appended: "**Report-only variant arrays (RC-1):** variant arrays v:Zc010 = (A_full − A_S^v − 0.10·A_full)1_{E_x} and v:Zc050 for v ∈ {R_E, R_K1, R_K2}, A_S^v from the frozen FIT keys `{v}_P_S`, `{v}_L`, `{v}_B` (guards β_A with δ_P(v) from `FIT_j.json` "delta"); outside Lemma FW-ND, as C2 §6.3 remark 6; X1 on the variant complement arms on the 1,024 lowest-id eligible rows (§3 row 19). Same seed and indices as the primary N-R arrays."
- **§2.1 "C2ND uses"**, inserted after the basis keys: "the variant keys `{v}_P_S`, `{v}_L`, `{v}_B` for v ∈ {`R_E`, `R_K1`, `R_K2`} (the report-only N-R variant arrays, §4.2; their δ_P(v) from `FIT_j.json` "delta"),".
- **§2.3**, after the coarse statements, inserted: "**Variant categories (report-only):** the CODE_DOMINANT / NOT_NECESSARY / COMPLEMENT_LOW_ALIGNED rule on v:Zc010, v:Zc050 with the primary RESP/SPEC prerequisites (`c2_decide.variant_category` pattern). Qualifiers PROJECTOR_DEPENDENT_NR(j) iff the R_E category ≠ the primary; HARMONIC_DEPENDENT_NR(j, K) iff the R_K{K} category ≠ the primary. (The variant arrays are defined in §4.2; they are outside Lemma FW-ND, as C2 §6.3 remark 6.)"
- **§7.2 CODE_DOMINANT**, appended to the licence: "[If PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR:] The size of the remainder depends on how 'everything except the code' is defined; under [variant] it is below 10%." Added to "Not licensed": "that the remainder is a property of the code rather than of the registered complement". The §7.2 qualifiers line gains "PROJECTOR_DEPENDENT_NR(j); HARMONIC_DEPENDENT_NR(j, K) (report-only variant categories, §2.3);".
- **§15 Q1**, inserted before the default: "With C2's two registered alternative definitions of 'everything else', the rest is about 6–9%, so the answer depends on that definition, and the result will say so."
- **§5.1**, new fixture after T-RULE6: "**T-PROJ-ND (variant qualifiers; RC-1):** synthetic readouts with a primary (K = 3 GLS) complement and R_E, R_K1, R_K2 variant projectors: when a variant's category on v:Zc010, v:Zc050 differs from the primary (e.g. primary CODE_DOMINANT, R_E COMPLEMENT_LOW_ALIGNED) → PROJECTOR_DEPENDENT_NR(j) (R_E) or HARMONIC_DEPENDENT_NR(j, K) (R_K{K}); equal categories → no qualifier; the variant arrays never change the primary category; an EXCLUDED primary returns the primary status and a missing variant array gives NOT_COMPUTED (`c2_decide.variant_category` pattern)." Added to the `test_a_*` list in §11.3 and to the synthetic-only list in §5.4 ("the N-R variant qualifiers (T-PROJ-ND)").
- **Propagation ("necessary is unreachable" restricted to the main complement).** Summary: "is not reachable" → "is not reachable for the registered complement (C2's variants: 6–9%, report-only)". §2.3 consequence bullet, appended: "This holds for the registered K = 3 GLS complement only: C2's registered variants put 1 − ψ at 0.06–0.09 (R_E, R_K1; §1.4), so the remainder's size depends on the complement definition (report-only variant categories below)." §4.6 NECESSARY clause → "**best case 0.149 > 0.10 for the registered K = 3 GLS complement; rule 1 says it cannot be reached there, and no run can change that** (owner Q1). The R_E and R_K1 variant remainders (0.06–0.09, §1.4) are report-only and never license NECESSARY." §1.3: new row "E-proj: the size of the remainder depends on how "everything except the code" is defined (C2 §1.3) | the report-only variant categories on the R_E, R_K1, R_K2 complements and the qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR (§2.3) | which complement definition is "right" (none is chosen)". §3 row 19 (X1) adds "the base model's variant complement arms (R_E, R_K1, R_K2; §4.2) on the 1,024 lowest-id eligible rows". §4.3 N-R rule appended: "then the report-only variant categories and the qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR (§2.3), which never change the primary category." §4.4 N-R guard appended: "The report-only variant arrays v:Zc010, v:Zc050 use β_A with δ_P(v) from `FIT_j.json` "delta" (v ∈ {R_E, R_K1, R_K2})." §8.1 scope: the two qualifiers and "the report-only N-R variant arrays and categories" listed as outside. §11.3 `nd_attrib.py` gains "the report-only R_E, R_K1, R_K2 variant arrays"; `nd_decide.py` gains "the N-R variant categories and qualifiers". §14 row "The expected partial result": effect → "…so "necessary" is unreachable for the registered K = 3 GLS complement"; new row "The remainder depends on the complement definition | C2's R_E and R_K1 variants put it at 6–9%, so "≈ 15%" could be read as a property of the code | report-only variant categories, qualifiers PROJECTOR_DEPENDENT_NR / HARMONIC_DEPENDENT_NR, licence wording (§2.3, §7.2), owner Q1". §9 row-forwards, appended: "The X1 check of the three N-R variant complement arms (RC-1) adds 3 × 2 × 1,024 = 6,144 per model and split (≈ 0.013 CPU-h for three models at DVAL, the same at DTEST), inside the low–high ranges; the central values are unchanged." §9 bootstrap line → "N-R 10 (9 + 1 check) + 6 report-only variant arrays + D 12 + N-M 7 = 35 per model, 105 in all (C2 S5 ran 99), so the S5 bootstrap cost is ≈ 1.06× the C2 measurement, inside the S5 range."; §9 S5 row "90 arrays × 20,000" → "105 arrays × 20,000".

### RC-2 (MAJOR): the decoy leak is magnified
- **§2.8**, "Expected λ_D ≪ 0.10 [H]." replaced verbatim by: "Scale [H]: λ_D ≈ ε_vis·ψ/(1 − ψ) ≈ 5.7·ε_vis, ε_vis the relative readout-visible error of col(B̂) against col(B), so 0.10 is reached at ε_vis ≈ 0.018. The energy conjuncts are magnified by E[e_S]/E[e_comp]. No recorded quantity bounds ε_vis. Blind S2 diagnostic (F1; matrices only, no rows, no logits): the canonical angles between col(B̂(R@D)) and col(B), and κ_leak := ‖CM(I − P_S)B̂‖₂/‖CMB̂‖₂, reported, not gated." Because κ_leak uses P_S, in the same section "P_S appears only in the exactness gate DX." → "P_S appears only in the exactness gate DX and in the blind S2 diagnostic κ_leak below (reported, never decision-bearing)."
- **§4.6 feasibility rule 1**, the DECOY_NOT_USED clause replaced verbatim by: "DECOY_NOT_USED: the sampling half-width (≈ 0.003) is > 25× below the margin, but the refit leak is not bounded in advance (§2.8). DECOY_PARTIAL or DECOY_LOW_ALIGNED from leak alone is possible. Rule 1 is shown for the sampling component only [H]."
- **§7.3 DECOY_PARTIAL**, "A bias of ≥ 0.10 in ψ is possible." replaced verbatim by: "A decoy share λ corresponds, in C2's own models, to a refit error of about λ(1 − ψ)/ψ ≈ 0.18·λ in ψ (§2.8). The report states both scales and κ_leak."
- **§14**, row added: "Leak magnified by ψ/(1 − ψ) | a false PARTIAL or LOW_ALIGNED | §2.8 scale statement, S2 blind diagnostic, dual-scale reporting".
- **Propagation.** §3 row 13 (F1) adds "Plus the blind leak diagnostic of §2.8 for R@D (canonical angles between col(B̂(R@D)) and col(B), κ_leak; matrices only, no rows, no logits; reported, not gated)"; §9 S2 row adds "the blind leak diagnostic". §1.5: "so NOT_USED is expected with a large margin (§4.6)" → "so NOT_USED is expected; its sampling margin is large, but the refit leak is not bounded in advance (§2.8, §4.6)". §1.3 E-estimation row → "the leak share of D-NULL (§2.8; magnified by ψ/(1 − ψ)), the blind S2 diagnostic κ_leak and DECOY_POSITIVE_BELOW_MARGIN". §4.6 D bullet: "margin ≈ 26×." → "margin ≈ 26× (sampling only)."; "plus a small leak." → "plus the refit leak, which is magnified by E[e_S]/E[e_comp] and not bounded in advance (§2.8)." §4.6 last clause: "which is not expected [H]" → "which the unbounded refit leak makes possible (§2.8) [H]". §8.1 scope adds "the S2 leak diagnostic". §11.3 `nd_attrib.py` adds "κ_leak".

### RC-3 (MAJOR): sealing breach through V3x′
- **§6.7 L5**: in the parenthesis, "the D endpoint is D-NULL, which is not in KC" replaced verbatim by "D-DOSE PARTIAL at KC implies only 0.58 < ψ_refit < 0.93 on DVAL; no choice depends on it"; appended verbatim: "V3x′, V3x′-g1 and Y1′ release PASS/FAIL only before the TEST outcome; their means and bounds are sealed with the DVAL endpoint values (mean(A′_full) reconstructs the sealed base A_S)."
- **§4.5**: "0.10·min_j mean(A′_full·1_E) (D; a V3x′ gate quantity, not an endpoint)" replaced verbatim by "0.03·min_j mean(G·1_{E_x}) on DVAL (D; 0.10 × the 0.30 gate × the oracle contrast, a lower bound on 0.10·mean(A′_full·1_E) whenever V3x′ passes; oracle-only). [W: SD(Z010′) ≈ 0.08 gives an mde of 0.0044 < 0.033 at N = 4,096, so k = 1 is still expected.]"
- **§3 row 23**: appended "Releases PASS/FAIL only (§6.7 L5)".
- **Propagation.** §4.6 P1 condition adds "For D the alternative is 0.03·min_j mean(G·1_{E_x}) ≈ 0.033 nat (§4.5): SD(Z010′) ≈ 0.08 gives an mde of 0.0044 at N = 4,096." §9 extension rule 1 adds "; for D, the oracle contrast mean in place of a decoy gate mean (§4.5)". §6.1 DVAL row adds "(and the V3x′, V3x′-g1, Y1′ means and bounds; §6.7 L5)". §2.5's V3x′-g1 reference adds "PASS/FAIL only before the TEST outcome, its value unsealed at REPORT, §6.7 L5". "KC and KC-R" → "KC, KC-R, V3x′, V3x′-g1 and Y1′" in the PASS/FAIL-only release rules of §10.1 (forbidden-access list and pass criterion 4), §11.2 item 5 (plus "before the TEST outcome"), §11.3 T-SEAL-ND and §12 S12.

### RC-4 (MAJOR): layer-2 rule-6 statement
- **§2.4**: "There is no rule-6 statement for N-M (R-C2ND-4 registers two, both above; see §19 item 21)." replaced verbatim by: "**Rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN_j:** declared iff L(Ztau) > 0, L(NEGMc) > 0, U(ZMc010) < 0 and U(ZMc050) < 0, with RESP. Truth claimed: 0 < ψ_M,comp < 0.10. Reported beside NECESSARY_M or COMPLEMENT_LOW_ALIGNED_M; it uses the existing NEGMc array."
- **§8.1 N-M**: text from "On the event that it is true…" to the end of the paragraph replaced verbatim by: "If τ_M < 0.10: every declared statement except ROUTED needs L(Ztau) > 0, so all lie in F^L_Ztau: ≤ 1 + RESP. If τ_M = 0.10: F^L_Ztau, F^U_Ztau, RESP (the categories lie in F^L_Ztau): ≤ 3. If τ_M > 0.10: ROUTED false needs F^U_Ztau. The categories and rule-6 (c) behave as N-R without the nested entry: κ_M ≤ −0.10 → F^L_WMc, F^L_ZMc010, F^L_NEGMc; −0.10 < κ_M ≤ 0 → F^U_VMc, F^L_ZMc010, F^L_NEGMc; 0 < κ_M < 0.10 → F^U_VMc, F^L_ZMc010; the other regions as C2 (≤ 2). So ≤ 1 + 3 + 1 = **5 per model**, 15α_NM = **0.0417 at α_NM = 1/360**; unions unchanged." Its heading "(with the −0.10 lower bound in NECESSARY_M; no rule-6 statement)" → "(with the −0.10 lower bound in NECESSARY_M and rule-6 statement (c))". §8.2, §8.3 and §16 unchanged (5 events, 0.0417; unions 0.15 / 0.1417 / 0.1917 / 0.2917).
- **§7.4**, inserted: "**Rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN:** "In [k] models the layer-2 complement interchange carries a certified positive share below the 10% margin (ψ̂_M,comp [ ], bounds [ ])", plus the C2-M caveats and KM3; reported beside NECESSARY_M or COMPLEMENT_LOW_ALIGNED_M."
- **§5.1 T-RULE6**: added "(d) 0 < ψ_M,comp < 0.10 → COMPLEMENT_M_POSITIVE_BELOW_MARGIN".
- **§19 item 21** replaced by: "**Rule-6 statement (c) for N-M, COMPLEMENT_M_POSITIVE_BELOW_MARGIN.** Added per coordinator ruling; 5 events, 0.0417." §19 item 7 appended "(v2: a third, rule-6 (c) for N-M, added per coordinator ruling; item 21.)".
- **Propagation.** §1.2 N-M claim adds "a registered "positive but below margin" statement for the layer-2 complement (rule 6 (c))". §4.3 N-M rule adds "then rule-6 statement (c), COMPLEMENT_M_POSITIVE_BELOW_MARGIN_j (§2.4)". §4.6 adds "COMPLEMENT_M_POSITIVE_BELOW_MARGIN (c) cannot be reached for the same reason as NECESSARY_M." §11.3 `nd_decide.py`: "the rule-6 statements (a)–(c)".

### RC-5 (MAJOR): authorisation sequence
- **STATUS line**: as under Header (the RC-5 (a) text, verbatim, after the required status words).
- **§3 row 0a**: gate "GO-IMPL" → "AUTH-IMPL"; content → "owner addendum naming the C2ND-DESIGN-v1 sha256 and the dry-run budget → `AUTH_IMPL.json` (implementation, tests, synthetic-only dry run; §13 step 2)". **Row 0c** content → "C2ND-FROZEN-v1 = C2ND-DESIGN-v1 plus the binding fields only (H, DRY report sha256, OPEN closures); any other text change → a new candidate and review. C2ND-FROZEN-v1 sha256 and CONTRACT recorded". **Row 0d** (the driver gate name AUTH-ADMIT is kept, so `GATE_ORDER` is unchanged) content → "owner AUTH-RUN addendum naming the C2ND-FROZEN-v1 sha256 and the staged budget → `AUTH.json` (§13 step 5)" (v1's "§13 step 2" corrected to step 5). Gate-order note: "(GO-IMPL, DRY and FREEZE …)" → "(AUTH-IMPL, DRY and FREEZE …)".
- **§11.4**: "from the frozen plan and `API.md` only" → "from C2ND-DESIGN-v1 (sha256) and `API.md` only". **§11.3**: `PROTOCOL_C2ND_v1.md` "(byte copy of the frozen plan)" → "(byte copy of C2ND-DESIGN-v1, replaced by the identical-substance frozen text at freeze; G0 checks it against FROZEN)".
- **§13** steps 1–5 rewritten: 1 "clean-context review (addendum 28) of this merged plan, result-blind; the coordinator's confirmation and acceptance as design freeze candidate C2ND-DESIGN-v1 (sha256 recorded); OPEN-1 to OPEN-3 closed (§17)"; 2 "Owner AUTH-IMPL (owner Q5, first part): an owner addendum naming the C2ND-DESIGN-v1 sha256 and the dry-run budget → `AUTH_IMPL.json`: implementation, tests (independent authors, written from C2ND-DESIGN-v1) and the metered synthetic-only dry run (≈ 0.4 CPU-h central, 0.25–0.80, 3× pause at 1.20). This is not an AUTH for real data."; 3 adds "(from C2ND-DESIGN-v1 and `API.md`, §11.4)" to the tests; 4 "Final freeze C2ND-FROZEN-v1: C2ND-DESIGN-v1 plus the binding fields only (H, the dry-run report sha256, OPEN closures); any other text change → a new candidate and review. CONTRACT and the parallel stores' readers (§6.2) recorded."; 5 "Owner AUTH-RUN (asked again after the freeze): … → `AUTH.json`, for S1–S5." "Codex review" → "clean-context review (addendum 28)".
- **§15 Q5** → "**Two-step authorisation.** First, AUTH-IMPL: implementation, tests and the metered synthetic-only dry run (≈ 0.4 CPU-h, pause at 1.20) on the design freeze candidate C2ND-DESIGN-v1. Then, after the final freeze C2ND-FROZEN-v1, AUTH-RUN: the staged run (≈ 0.8 CPU-h central, up to ≈ 1.5), with a plain-language pause if measured use passes 3× the estimate at any stage boundary. **Default: approve AUTH-IMPL now; ask again for AUTH-RUN after the freeze.**"
- **Header "Authorises" row**: as under Header.

### RC-6 (MINOR): missing upper conjuncts in rule-6 (a) and (b)
- **§2.3** rule-6 (a): "declared iff L(NEGc) > 0 and U(Zc010) < 0" → "declared iff L(NEGc) > 0, U(Zc010) < 0 and U(Zc050) < 0". **§4.3** rule-6 (b): "declared iff L(NEG′) > 0 and U(Z010′) < 0" → "declared iff L(NEG′) > 0, U(Z010′) < 0 and U(Z050′) < 0". The §8.1 attributions (F^U_Zc050 for κ ≥ 0.50; F^U_Z050′ for ψ′ ≥ 0.50) are now correct as printed; no table change.

### RC-7 (MINOR): V3y′ also scales with g
- **§2.8 Lemma DG**: "Only V3x′ = (A′_full − 0.30·G)1_E depends on g." → "Only V3x′ and V3y′ (hence whether Y1′ is active) depend on g."; in the same lemma "every D decision except RESP′" → "every D decision except RESP′ and SPEC′ (through whether Y1′ is active)". §5.1 T-GAIN: "except V3x′" → "except V3x′ and V3y′ (hence whether Y1′ is active)". §19 item 1 annotated "(v2: SPEC′ also depends on g through whether Y1′ is active, RC-7)".

### RC-8 (MINOR): 3× column separated by authorisation
- **§9 table, last column**: A1 → "A1: own valve 1.20 under AUTH-IMPL (4,320 CPU-s)"; S1 → "S1–S5 under AUTH-RUN, cumulative from S1: 0.60 (2,160 s)"; S2 → "0.75 (2,700 s)"; S3 → "0.96 (3,456 s)"; S4 → "1.50 (5,400 s)"; S5 → "2.46 (8,856 s)"; further block → "+0.63 per extra block (+2,268 s)" (v1: 1.20, 1.80, 1.95, 2.16, 2.70, 3.66). The totals row is unchanged (2.46 / 3.09 / 4.35). Rule 4 adds "(last column; A1 has its own valve under AUTH-IMPL, and S1–S5 are cumulated from S1 under AUTH-RUN)". §16 3× line → "A1 alone 3 × 0.40 = 1.20 CPU-h (under AUTH-IMPL); S1–S5 cumulative from S1 (under AUTH-RUN) 3 × (0.20, 0.25, 0.32, 0.50, 0.82) = 0.60, 0.75, 0.96, 1.50, 2.46 CPU-h; +3 × 0.21 = +0.63 per extra block."

### RC-9 (MINOR): decoy κ_X1 and decoy-confined failures
- **§3 row 11**: added "(viii) κ_X1 of each decoy head (as `c2_model.kappa_x1`, `x1_attainable`)", failure "(viii) → INCONCLUSIVE/NUMERICAL for that decoy (D if D-NULL)". **Rows 19–20**: failure column adds "a failure confined to decoy arms → FAIL_TECHNICAL/DECOY, scope family D"; scope "study (decoy-confined: family D)". Propagated to row 29 (T-PRE runs X1 and DX on DTEST): "(a failure confined to decoy arms → FAIL_TECHNICAL/DECOY, scope family D, as rows 19–20)".

### RC-10 (MINOR): C0v
- The reviewer's second alternative was applied: "C0v is not rerun: charts frozen and validated by C2 S3; SUP covers new rows." Inserted in **§2.5 (R1)** (with "(§3 row 14)") and in **§3 row 14** (SUP). Reason for choosing it over row 14b: C2's C0v claims direct constructions in the C1′ `ConstructionLedger` (`CHART_CONSTRUCTIONS.json`, ledger limit 3, used by C2 S3), which C2ND binds as lineage only; a rerun would need new claims on that ledger. `GATE_ORDER` is unchanged.

### RC-11 (MINOR): cross-round namespace hazard
- **§6.6**, appended verbatim: "The parallel rounds name `c2nd-store` by path and sha256, never by the string `c2nd-v1`, and C2ND files never contain their scope strings. G0 and REG2 report a hit in a parallel store as FOREIGN; T-NAMESPACE-ND includes this case."

### RC-12 (MINOR): editorial
- **§17**: OPEN-1, OPEN-2 and OPEN-3 marked closed (see below); the heading adds "; all closed by coordinator rulings, 2026-10-26".
- **§4.3**: "Its TEST endpoints are still scored for the remaining models and reported, but no DECOY_NOT_USED licence is issued:" → "A KNOWN_CASE_CONTRADICTED at S4 triggers S13 before ACCEPT. If the owner continues, D's TEST arrays are scored report-only with the outcome fixed. No DECOY_NOT_USED licence is issued:". §3 row 24 failure adds "S13 before ACCEPT" and "§4.3".
- **§2.6**: "≥ 2.7×" → "≥ 2.6×"; propagated to §14 ("desk margins ≥ 2.6×").
- **§4.2**: "10 arrays plus 1 check" → "9 arrays plus 1 check" (propagated to the §9 bootstrap count, under RC-1).
- **§5.1 KM1**: "complement donors built with equal per-row mean and norm (σ unchanged)" → "every patched state (F, S, C) has the per-row mean and norm of a₂(H)".

### OPEN items (coordinator rulings)
- **OPEN-1** (§17): "**Closed: unreadable or unfrozen parallel store → REGISTRY_INCOMPLETE.** A parallel-round store (`hws-store`, `x6zc-store`) that exists without a frozen registry reader makes the registry fail closed (INCOMPLETE). Background as recorded in v1:" (the v1 text follows unchanged). §6.2 rows 7 and 8: "**OPEN-1**" → "OPEN-1 closed (§17): an unreadable or unfrozen store → REGISTRY_INCOMPLETE". The §6.2 inventory paragraph already stated this rule and is unchanged.
- **OPEN-2** (§17): "**Closed: history generation of the three rounds in separate metered jobs, never concurrent; each registry covers every store existing at its registration.** Background as recorded in v1:". §6.5: "The schedule itself is **OPEN-2**." → "OPEN-2 is closed (§17): history generation of the three rounds runs in separate metered jobs, never concurrent; each round's registry at its registration time covers every store that exists then."
- **OPEN-3** (§17): "**Closed: the coordinator runs `--check`.** It is a coordinator task, not a protocol item." v1's sentence "The implementation job runs the check before relying on the index." was removed.
- **The two "move" known cases** (new §17 bullet; §5.3): "Ruling on the two "move" known cases (confirmed). D-NULL-R and D-ID are report-only: own report-only gate KC-R; a contradiction adds a qualifier only (MOVE_CASE_CONTRADICTED). v1 already conformed (§3 row 25, §5.3)." §5.3 adds "(coordinator ruling: report-only, own gate KC-R; a contradiction adds a qualifier only)". No decision rule changed.

### Codex frozen (addendum 28)
- Every place where v1 named a Codex review (the STATUS line; §13 step 1) now names a clean-context Claude reviewer (addendum 28). References to track X's file name and to "track X §…" cite an input; they are not reviewer assignments and are unchanged.

## Confirmation and design freeze candidate (coordinator 243a611b, 2026-10-26)
- Claude result-blind confirmation of v2 (`coord-c2nd-review-20261026.v2confirm.claude-reviewer.md`; Codex frozen, addendum 28): **CONFIRM_AFTER_MINOR_FIXES**; RC-1..RC-12 applied; writer choices accepted.
- RC-13 and NEW-1..NEW-3 applied verbatim. No other change from v2.
- This document is the **C2ND design freeze candidate (C2ND-DESIGN-v1)**. C2ND-FROZEN-v1 will be byte-identical to it; the implementation hash, the dry-run report sha256 and the CONTRACT sha256 are bound in `c2nd-store/FREEZE.json` after a separate owner AUTH for implementation, tests and synthetic-only dry runs. S1 onward needs a later owner AUTH.
