# D-1 seam oracle check: outputs manifest (job 0020)

**Protocol:** D1-FROZEN-v1 (68EBD82F…0B21), with addendum 1 (1EE0291D…2669) and addendum 2 (2258ED96…3F6F). This is a pre-registered, oracle-only existence check: no sampling, no training.

**Verdict: PASS.** Every gate, G0, G0S, G0O, G1, G2 (including G2.11), G3, G4, G5 and G6, is PASS. The mandatory preflight passed and S0 passed.

**Source.** topo-pilot-d1, branch d1-seam-0019. The run was at HEAD 7cb687b (module) and S0 verified an empty kernel diff against 4f219d6.
- contract 6803a66, with deltas a5152f5 and 933a983;
- independent tests 70fc3a8;
- `d1_seam.py` sha256 104c516d…39d2 (400 lines);
- `d1_seam_checks.py` sha256 0592c4fa…37b6 (335 lines).

**Store:** `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`

| File | sha256 |
|---|---|
| run_0020/report.json | 174b1e194b51fd3397c888dcc73bfdf6ae96ba5145e6347526824f445e45a9b2 |
| run_0020/model.npz | 3992c4bfd5da7beb9135b7292034148f9b2d392b8a84c0ab2fd037d714e31d1b |
| preflight.json | a99038dfe323fc43f1d3251f318644be0a2f6c70d83791b124e7e59ac996d9cd |
| preflight_detail.json | cd35654776d3f0c96cba315a93101f0a9492c63ad496e0f7deecadd005ac8067 |
| d1_meter_bind.py (store-local meter binding) | 5b02aad465dd343538e0ce004e1d7bcd75c275101bc736248fdd40c38eeec619 |
| d1_preflight.py (store-local preflight driver) | 59fa9bca12b129861efdab18f75f31b8fb8615fdf84220464cd17279a0b6b612 |

**Ledger** (store `cpu_ledger.json`, measure-only; the S1 ceiling of 1200 CPU s applies to the gate run):

| Label | Status | Exit | Charged CPU s | Wall s |
|---|---|---|---|---|
| d1__tests-dev | FINISHED | 1 | 145.147 | 144.657 |
| d1__tests-dev2 | FINISHED | 0 | 144.428 | 143.687 |
| d1__smoke-dev | FINISHED | 0 | 35.428 | 35.281 |
| d1__preflight | FINISHED | 0 | 148.834 | 148.968 |
| d1__run | FINISHED | 0 | 159.459 | 158.562 |

**Total:** 633.297 CPU s charged (632.797 s measured, plus 0.5 s tail).
