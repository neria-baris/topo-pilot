# Extensions: orientability, unions of tori, higher-dimensional holes

**Precondition:** E2 reached. Extensions never modify the decisions of the core pilot. Each one adds registered plugins, configs, and its own preregistration addendum (`PREREGISTRATION_X<k>.md`, written before training).

## 1. Built-in extensibility (required in the core build)

The core modules must already satisfy the following, so that extensions add classes without editing existing ones:

| Module | Requirement |
|---|---|
| `world` | `CubicalComplex` with cells of dimension 0–3, stored as ordered vertex tuples. Signed boundary matrices over ℤ; ranks over GF(p) for any prime p. `QuotientLatticeBuilder(dims, identifications)` handles plain, periodic, and **flipped** periodic gluings. A `WorldBuilder` registry. Metrics: `FlatQuotientMetric` (minimum over deck-transformation lifts) and `GraphGeodesicMetric` |
| `process` | Max-degree lazy walk for any connected graph (uniform π; reduces exactly to the core rule). `CenterStrategy` ABC with `GridCenters` (core) and `FPSCenters` (farthest-point sampling on any metric). `EmissionModel` works with any `Metric` |
| `topology` | `coeff_p` and `maxdim` parameters. Per-dimension summaries $S_k$ and $\pi_{\max,k}$. Landmark subsampling (maxmin) as an option, used only when `maxdim ≥ 2` |
| `analysis` | Spaces and summaries keyed by (dimension, field). A component analysis using β₀ and a clustering-free H₀ gap statistic |

## 2. X1: orientability

Reference table (Betti numbers over GF(2) vs ℚ, where GF(3) agrees with ℚ for these spaces):

| Space | χ | β over F₂ | β over F₃ / ℚ | Orientable |
|---|---|---|---|---|
| Disk (square) | 1 | (1,0,0) | (1,0,0) | yes |
| Cylinder | 0 | (1,1,0) | (1,1,0) | yes |
| Möbius band | 0 | (1,1,0) | (1,1,0) | no |
| Torus | 0 | (1,2,1) | (1,2,1) | yes |
| Klein bottle | 0 | (1,2,1) | (1,1,0) | no |
| S² | 2 | (1,0,1) | (1,0,1) | yes |
| RP² | 1 | (1,1,1) | (1,0,0) | no |

**X1a: Möbius band vs cylinder.** These are homotopy equivalent, so homology cannot separate them. They differ in their **boundary**: the cylinder has two boundary circles of 12 vertices each, and the Möbius band has one boundary circle of 24.

- **Worlds:** $12\times12$ lattice; x-periodic. The cylinder uses a plain identification. The Möbius band uses a flipped one: $(11,y)\to(0,11-y)$.
- **Test:**
  1. Select histories whose oracle belief mass on boundary states is ≥ 0.8. This is an analysis-side selection using beliefs only, not latent labels.
  2. Compute PH of their activations.
  3. **Prediction:** the cylinder gives β̂₀ = 2 with one H₁ bar per component; the Möbius band gives β̂₀ = 1 with one H₁ bar.
- **Controls:** P (axis-wise permutation) and N, as in the core pilot.

**X1b: closed non-orientable vs orientable surfaces.**

- **Pairs:**
  - torus vs Klein bottle: both $12\times12$, N = 144. The Klein bottle uses a flipped x-gluing and a plain y-gluing;
  - S² vs RP²: S² is the surface of the cube lattice $[0,5]^3$ (N = 152); RP² is the surface of $[0,7]^3$ modulo the antipodal map $v\mapsto(7,7,7)-v$, which is free on the surface (N = 148).
- **Test:** VR with `maxdim = 2`, computed over **both F₂ and F₃**, on maxmin landmarks (M ≤ 400). The torsion signature is the drop β₁(F₂) − β₁(F₃) = 1, and β₂(F₂) = 1 while β₂(F₃) = 0.
- **Prediction:** a representation that is faithful at this resolution reproduces the signature for the Klein bottle and RP², and does not show it for the torus or S².
- **Always calibrate first** on the worlds themselves (VR on $d_M$) and on synthetic noisy embeddings.
- **Caveat:** Vietoris–Rips at finite scale can create or hide torsion. The claim is limited to "signature reproduced / not reproduced at the calibrated scale band".

## 3. X2: unions of tori

**X2a: disjoint union T²⊔T²** gives uncertainty about *which world* the sequence comes from.

- **States:** two $12\times12$ tori, N = 288, with no transitions between them. The start distribution is uniform over all 288 states, so each component has probability ½.
- **Emissions:** a shared alphabet with V = 36. Component A uses O. Component B uses O composed with a fixed axis-wise permutation. The marginal symbol statistics are therefore identical, and the component can be identified only through sequence structure.
- **World Betti numbers:** (2, 4, 2).
- **Oracle:** the belief is a distribution over 288 states. Its component marginal $P(\text{comp}\mid h)$ is the "belief about the world".
- **Predictions:**
  - activations at late positions split into two clusters (β̂₀ = 2), each with two H₁ bars;
  - at early positions, where the component marginal is near ½, the clusters are not separated.
- **Measure:** the H₀ gap statistic against the component-marginal entropy, as a function of position.

**X2b: connected sum T²#T²** (genus 2).

- **Construction:**
  1. Take two $12\times12$ tori.
  2. From each, remove an open $2\times2$ block of faces: 4 faces, 4 interior edges, and 1 interior vertex.
  3. Glue the two 8-vertex boundary loops vertex-to-vertex, with one loop reversed so the result is orientable.
- **Result:** N = 278, χ = −2, β = (1, 4, 1).
- **Degrees:** the 4 seam corners have degree 6, so $D_\text{max}=6$. This changes the walk speed relative to the core pilot; report the spectral gap.
- **Metric:** graph geodesic (there is no flat metric near the seam corners).
- **Emissions:** `FPSCenters` with V = 70 (N/V ≈ 4) and a Gaussian kernel on the geodesic metric.
- **Generalisation:** `connected_sum(g)` chains g tori. Expected β = (1, 2g, 1).
- **Prediction:** β̂₁ = 4 at the calibrated scale band, with H₂ exploratory.
- **Comparison:** a single torus with matched N/V.

## 4. X3: higher-dimensional holes

| World | Construction | N | Expected β |
|---|---|---|---|
| S² | surface of cube lattice $[0,5]^3$ | 152 | (1,0,1) |
| T³ | $5\times5\times5$ periodic lattice, 6-neighbourhood, cells up to 3-cubes | 125 | (1,3,3,1) |
| S³ | boundary of 4-cube lattice $[0,3]^4$ | 240 | (1,0,0,1) |

**Emissions:** `FPSCenters`, V ≈ N/4, with a geodesic Gaussian. σ is calibrated with the same rule as the core pilot.

**PH:**

- H₂ uses Vietoris–Rips with maxmin landmarks (M ≤ 400).
- H₃ is **approximate**: either Vietoris–Rips with `maxdim = 3` on M ≤ 150 landmarks, or a witness complex (gudhi) on M ≤ 400. Results are flagged `approximate`.
- Calibration on synthetic noisy $S^2$ and $S^3$ in $\mathbb{R}^{128}$ is **mandatory** before any claim.

**Budget:** the H₃ computations can dominate the run time. Cap each PH call at 10 minutes and record a timeout as status `censored`.

**Prediction:** the top-dimensional class is reproduced in the activations only when beliefs are concentrated, so use the belief-entropy filter as in the core analysis. The interesting comparison is the dimension at which the representation stops being faithful.

## 5. Plugin checklist for each extension world

1. A `WorldBuilder` subclass registered under a new family key, with tests:
   - homology over F₂ and F₃ against the table above;
   - χ;
   - ∂∂ = 0 over ℤ;
   - metric axioms;
   - for quotient metrics, `dist ≤ dist_graph`.
2. A config in `configs/extensions/x<k>_*.yaml`.
3. A preregistration addendum.
4. A world-level PH calibration (G-A analog) before any training.
5. Runs and analysis through the unchanged S3–S6 machinery.
6. A README section with its own exit criterion: a finding, or "not run".
