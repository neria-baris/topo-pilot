"""X6S1 data: bindings, constants, stage-0 constant map, seeds, pools, sampling, digests,
stage-0 regeneration and init states (X6S1-FROZEN-v1 §2.1, §4, §6.1-§6.2; API.md §3).
Import performs no I/O and no computation beyond small constants."""
# fmt: off

from __future__ import annotations

import hashlib
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_EXTRA = [REPO / p for p in ("tools/x6_stage1", "tools/x6_stage0", "tools/x4_oracle_profile",
                             "tools/d2a", "tools/k4b", "tools/c1prime_registry",
                             "tests/oracle_profile")]
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]

import numpy as np  # noqa: E402
import x6_model as xm  # noqa: E402

from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout  # noqa: E402
from topo_pilot.dataset import HMMSampler  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402
from topo_pilot.learner import ModelConfig, TrainConfig  # noqa: E402

# ---- bindings and paths (API 3.1) ----
PROTOCOL_ID = "X6S1-FROZEN-v1"
PROTOCOL_SHA256 = "2a909ace38231fbc6647e8ffdb5e6b5f22669a7c92182ae84240f32cd36efb9e"
ADDENDUM1_SHA256 = "bd9dd7338f32635f55860cf9b1a6933d5becc07fcffa48bb4761c5de2620ffe6"
REQUEST_SHA256 = "1d567d297f0aab8946a2d98708043f189c508e00283473100c67a065acb8e401"
R_COMMIT = "72ad039e36ae56340ec48e34059ff6afeeefe02f"
P_COMMIT = "0c341aa4b101f2f6e0d9b500c36d9a2084072784"
REPAIR_BLOBS = {
    "tools/d2a/process_tree.py": (
        "253551cd7f52eb62eae8c732ef1c86191338cad7088873422438b919afa5df94",
        "9dd679dede436ce3bf78646173a40c09f937b887"),
    "tools/d2a/d2a_train.py": (
        "a26a263020a4a04038e42b73889f77835a75a562a35cfb2e02e792e2b8396551",
        "58495d9feabcdcf18380fd37e3c984dcc27c4a22"),
    "tests/d2a/test_process_tree_repair.py": (
        "0021f6255bd8b02311f0257ebd8118e6e616787304ffea9aa86299db45ea9928",
        "6014683c4fe9ca87ae47c833f1133207f5f86ec6"),
    "docs/proposals/D2A_RUNTIME_MAINTENANCE_V1.md": (
        "a89e6314a0e50d7f15c5d81dfcfeeba110d4b899ae71ddeb2b6abb488b032262",
        "51a56175d86dc504e1681d740573fb2cf50fec18"),
    "tools/x4_oracle_profile/winjob.py": (
        "3b29e863ab6ae97c16540c0d56dbf678d18b88922e54fbc731f5cc0ec5405785",
        "1e354d54f473d9c1fb65de1c054ef40d18834c2f"),
}
PROJECT_ROOT = "X:/Downloads/projects/topo-pilot"
STORE = PROJECT_ROOT + "/x6-stage1-store"
WORKTREE = PROJECT_ROOT + "/topo-pilot-x6s1"
SCRATCH_ROOT = "X:/Downloads/topo-scratch"
MAILBOX = PROJECT_ROOT + "/agent-handoff"
STAGE0_STORE = PROJECT_ROOT + "/x6-stage0-oracle-store"
K4B_STORE = PROJECT_ROOT + "/k4b-store"
KREG_DIR = K4B_STORE + "/registry"
STAGE0_FILES = {
    "run/report.json": "e7846911b33d5c06eaadb633cf3cf4a2dae4a3e49dc6c0b50209f3fc09333aca",
    "run/GATES.jsonl": "c871f5e487c7f79e9ebb57cecc6acb4bdc584106e6bd86e64e48189614082462",
    "run/model.npz": "e1b9a753de211da4320b289b2737f0e3d0c7ee88eb4cecb07046d02b590f230b"}
STAGE0_OUTCOME = "GO_X6_NATURAL"
KREG2_FILES = {
    "K-REG2.json": "3a2698849f3de80883c2571b7c7c026577afb5ff986cce44ce76defa7900bb90",
    "K-REG2_digests.npz": "28897ebb43350dcf54eb5ba10bdf3edaeb1d3688c9e112a449c14f6b61290b44"}
KREG2_N_DIGESTS = 6024521

# ---- constants (API 3.2) ----
SCOPE, DATA_MASTER, MODEL_MASTER = "x6s1", 2026101861, 2026101862
ARMS, SEEDS = ("NA", "AB", "ZC"), (1, 2, 3, 4)
MODELS = tuple(f"{a}-s{s}" for a in ARMS for s in SEEDS)
INITS = tuple(f"init-s{s}" for s in SEEDS)
PREDICTORS = MODELS + INITS
WAVES = {"C0": ("SMOKE",), "C1": ("NA-s1", "NA-s2", "ZC-s1"),
         "C2": ("NA-s3", "NA-s4", "AB-s1", "AB-s2", "AB-s3", "AB-s4", "ZC-s2", "ZC-s3", "ZC-s4")}
T_STAR, N_OBS, V, BOS, N_MIN = 32, 33, 18, 18, 8
PROFILE_T, EMERGENCE_STEPS = (16, 24), (1000, 3000, 10000, 20000)
LC_STEPS = (0, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 25000, 30000)
N_PROFILE, N_EMERGE, N_DET, N_SMOKE_EVAL = 2**17, 2**14, 1024, 1024

MODEL_CFG = ModelConfig(vocab_in=19, vocab_out=18)
TRAIN_CFG, K = TrainConfig(steps=30000), 1000
SMOKE_CFG, K_SMOKE = TrainConfig(steps=200, warmup=10), 100
EQUIV_CFG = TrainConfig(steps=60, warmup=10, checkpoint_steps=(0, 20, 40, 60))
K_EQUIV = 20
ACCT_CFG = TrainConfig(steps=50, warmup=10)

Q, EPS, B_EB, E_ROW, SUM_TOL = 2**20, Fraction(1, 10**6), 17, Fraction(1, 10**12), 1e-12
FLOOR, FLOOR_SLACK = Fraction(1012287, 10**12), Fraction(1, 10**12)
DELTA_SHARP, DELTA_LEARN = Fraction(1, 160), Fraction(1, 40)
B_GATE, B_CORD, B_MODEL = 2000, 20000, 2000
BAND, XCHECK_TOL, DET_TOL = Fraction(1, 10**9), 1e-9, 1e-12

CORD_MEAN, CORD_LB = Fraction(1, 4), Fraction(1, 20)
PLACEBO, RHO_MAX = Fraction(1, 10), Fraction(1, 4)
CUE_MASS_MIN, W2_BETA = Fraction(1, 10), Fraction(1, 4)
REGRET_FRAC, TARGET_FRAC = Fraction(3, 4), Fraction(3, 4)
LOWN, PREC_BETA, PREC_FRAC = Fraction(1, 10), Fraction(1, 10), Fraction(1, 4)
TAIL_D1, TAIL_D2, Z975 = Fraction(1, 100), Fraction(1, 50), 1.959964
FEAS_PAIRS, FEAS_SE = 24000, 0.04
ACCT_CPU_MIN, ACCT_MEM_MIN, ACCT_KILL_CPU = 10.0, 200 * 10**6, 5.0
ACCT_KILL_SLACK_S, ACCT_POLL_S = 10.0, 2.0

THREADS, EVAL_BATCH, MAX_CHILDREN = {"intra": 2, "interop": 1}, 1024, 3
PROCESS_MEM, JOB_MEM, OUTPUT_CAP = 3 * 2**30, 12 * 2**30, 16 * 2**30
MAX_WALL_S, ALARM_CPU_S, REG_RUN, ORACLE_CHUNK = 43200, 90 * 3600, 2**22, 2**16


# ---- stage-0 constant map (API 3.3) ----
def _enc(path: str, lo: str, hi: str) -> dict:
    return {"path": path, "lo": lo, "hi": hi}


CONST_MAP = {
    "G_Parikh_32": _enc("natural/NA/G/Parikh/32",
        "0.0026358964806790516544074195299418525190876670746427621626951934793579293430931071",
        "0.0026358964806790516544074195299418525190876670746427621626971934793579293430931071"),
    "G_8_32": _enc("natural/NA/G_k/8/32",
        "0.0088553050512358844408577637624772307516013467873269249611029142273162701006695055",
        "0.0088553050512358844408577637624772307516013467873269249611049142273162701006695055"),
    "G_empty_32": _enc("natural/NA/G/empty/32",
        "0.010593527986497549359252006084138555993127156334917732289525354912438293374555259",
        "0.010593527986497549359252006084138555993127156334917732289527354912438293374555259"),
    "G_parity_32": _enc("natural/NA/G/parity/32",
        "0.0077918136361268966093229003778309576632577318464705699718604667184601923814331744",
        "0.0077918136361268966093229003778309576632577318464705699718624667184601923814331744"),
    "G_H1_32": _enc("natural/NA/G/H1/32",
        "0.0029868330805394917008518103703350360446063062121711452599965280377903897431099882",
        "0.0029868330805394917008518103703350360446063062121711452599985280377903897431099882"),
    "G_counts_32": _enc("natural/NA/G/counts/32",
        "0.0027360466251330357283986671289765521159094130432521006187981248848235868652143178",
        "0.0027360466251330357283986671289765521159094130432521006188001248848235868652143178"),
    "G_Parikh_16": _enc("natural/NA/G/Parikh/16",
        "0.00087481878390924800028049215495243428442769052148881691765265451850816780319221880",
        "0.00087481878390924800028049215495243428442769052148881691765465451850816780319221880"),
    "G_Parikh_24": _enc("natural/NA/G/Parikh/24",
        "0.0018950636053054594572854707040565480586105007720591051905464316715473854993561797",
        "0.0018950636053054594572854707040565480586105007720591051905484316715473854993561797"),
    "D_blk_32": _enc("blocks/kblk/NA/D_blk",
        "0.0013097210879466838286281212242406617310575248163552880055774825009415866752451283",
        "0.0013097210879466838286281212242406617310575248163552880055794825009415866752451283"),
    "J_8_32": _enc("natural/NA/J/8/32",
        "0.000037201925132837002548644427563472653549075986721412848440177176632924088968581341",
        "0.000037201925132837002548644427563472653549075986721412848442177176632924088968581341"),
    "Delta_W2": {"path": "exact/G3/set_gaps/W2|0", "value":
        "0.061119371341896547955524807971231695289846551087376421303896009064819738013445345"},
    "Delta_W3": {"path": "challenge/challenge/delta_challenge/0", "value":
        "0.037832084794304540254080229574490474113844007878061695581602399097047383150353710"},
    "E_cue_hits": {"path": "mc/hits/E_cue", "value": 200306},
    "amb_nb_hits": {"path": "mc/hits/amb_nb", "value": 13402},
}
_LADDER_NAMES = {"empty": "G_empty_32", "parity": "G_parity_32", "counts": "G_counts_32",
                 "H1": "G_H1_32", "Parikh": "G_Parikh_32", "blk": "D_blk_32"}


# ---- models, seeds and pools (API 3.4) ----
def parse_model(name) -> tuple:
    if name == "SMOKE":
        return ("NA", "smoke")
    head, sep, tail = str(name).partition("-s")
    if sep and head in ARMS + ("init",) and tail in ("1", "2", "3", "4"):
        return (head, int(tail))
    raise ValueError(f"unregistered model name {name!r}")


def run_key(name) -> tuple:
    return (SCOPE, parse_model(name)[1])


def init_seed(name) -> int:
    return SeedTree(MODEL_MASTER).seed("init", *run_key(name))


def batch_generator(name) -> np.random.Generator:
    return SeedTree(MODEL_MASTER).generator("batch_order", *run_key(name))


_POOL_ROWS = {"train": 2**20, "dev": 2**12, "smoke": 2**12, "prefix": 2**12, "val": 2**15,
              "test": 2**21}


def pool_spec(pool, arm="NA", s=None) -> dict:
    seeded = pool in ("train", "dev")
    ok = (pool in _POOL_ROWS or pool == "gate") and arm in ARMS and (
        s in SEEDS if seeded else s is None) and (arm == "NA" or pool not in ("smoke", "prefix"))
    if not ok:
        raise ValueError(f"unregistered pool {(pool, arm, s)!r}")
    rows = (2**16 if arm == "NA" else 2**14) if pool == "gate" else _POOL_ROWS[pool]
    split = pool if pool in ("train", "test") else "dev"
    stream = {"smoke": (SCOPE, "smoke", "NA"), "prefix": (SCOPE, "prefix")}.get(
        pool, (SCOPE, pool, arm, s) if seeded else (SCOPE, pool, arm))
    name = {"smoke": "smoke", "prefix": "prefix"}.get(
        pool, f"{pool}_{arm}_s{s}" if seeded else f"{pool}_{arm}")
    replicate = s if seeded else 0
    return {"pool": pool, "arm": arm, "s": s, "name": name, "rows": rows, "split": split,
            "stream": stream, "code": process_code(SCOPE, arm, pool, replicate),
            "replicate": replicate}


NONTEST_POOLS = tuple(
    [pool_spec("smoke")] + [pool_spec("gate", a) for a in ARMS] + [pool_spec("prefix")]
    + [pool_spec("val", a) for a in ARMS]
    + [pool_spec(p, a, s) for a in ARMS for s in SEEDS for p in ("train", "dev")])
TEST_POOLS = tuple(pool_spec("test", a) for a in ARMS)


def sequence_ids(spec) -> np.ndarray:
    return make_sequence_ids(spec["code"], spec["split"], spec["rows"])


@lru_cache(maxsize=None)
def arm_model(arm) -> dict:
    return xm.model(arm)


def sample_pool(spec) -> np.ndarray:
    m = arm_model(spec["arm"])
    gen = SeedTree(DATA_MASTER).generator(*spec["stream"])
    tokens, states = HMMSampler(m["Tf"], m["Ef"], m["pif"], SequenceLayout()).sample(
        spec["rows"], gen)
    del states  # latent states are never stored or returned (S9)
    return np.ascontiguousarray(tokens, dtype=np.uint8)


def observation_set(spec, tokens) -> ObservationSet:
    return ObservationSet(split=spec["split"], V=V, sequence_id=sequence_ids(spec),
                          tokens=np.ascontiguousarray(tokens, dtype=np.uint8))


def token_digest(tokens) -> str:
    return hashlib.sha256(np.ascontiguousarray(tokens, dtype=np.uint8).tobytes()).hexdigest()


def _file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_pool(path, tokens) -> str:
    with open(path, "xb") as fh:
        np.save(fh, np.ascontiguousarray(tokens, dtype=np.uint8), allow_pickle=False)
    return _file_sha(path)


def load_pool(path, file_sha256) -> np.ndarray:
    if _file_sha(path) != str(file_sha256).lower():
        raise ValueError(f"pool file hash mismatch: {path}")
    return np.load(path, allow_pickle=False)


def init_state(name) -> dict:
    import torch

    from topo_pilot.learner import TransformerLM

    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(init_seed(name))
        model = TransformerLM(MODEL_CFG)
    return {"model": model.state_dict()}


# ---- stage-0 regeneration and constants (API 3.4; S0 (v), REG1 (a)) ----
def regenerate_stage0() -> dict:
    import x6_run as xr

    return {arm: np.asarray(xr.sample(arm, xm.MC_ROWS[arm], SeedTree(xm.MASTER_SEED))[0],
                            dtype=np.uint8) for arm in xm.MC_ARMS}


@lru_cache(maxsize=None)
def holonomy_classes(arm="NA", n_max=31) -> dict:
    """{S: {n: {(v, statistic): {g: count}}}} for n = 1..n_max (x6_dp, unchanged)."""
    import x6_dp as xd

    out = {S: {} for S in xm.LADDER}
    for n, layer in xd.segment_dp(arm, n_max):
        if n:
            for S in xm.LADDER:
                out[S][n] = xd.classes(layer, S)
    return out


def stage0_counts(na_tokens) -> dict:
    """Stage-0 G6 `hits` semantics (x6_run.gate_G6): E_cue = a cue in w_1..w_32; amb_nb =
    n >= 1, v_32 in N(a*) and the row's Parikh class ambiguous for y."""
    import x6_dp as xd

    tables, hits = holonomy_classes("NA")["Parikh"], {"E_cue": 0, "amb_nb": 0}
    for row in np.asarray(na_tokens)[:, :32].tolist():
        p = xm.parse(row)
        if p["segment"] is None:
            continue
        hits["E_cue"] += 1
        if p["n"] >= 1 and p["v"] in xm.ANCHOR_NB:
            cls = tables[p["n"]][(p["v"], xm.parikh(p["segment"]))]
            hits["amb_nb"] += xd.ambiguous(cls, p["y"])
    return hits


def stage0_count_check(counts) -> str:
    ok = all(counts.get(k) == CONST_MAP[n]["value"]
             for k, n in (("E_cue", "E_cue_hits"), ("amb_nb", "amb_nb_hits")))
    return "PASS" if ok else "FAIL_TECHNICAL/LINEAGE"


def stage0_value(report, name):
    node = report
    for key in CONST_MAP[name]["path"].split("/"):
        node = node[key]
    return node


def _same(got, want) -> bool:
    return type(got) is type(want) and got == want


def check_stage0_constants(report) -> dict:
    bad = []
    for name, spec in CONST_MAP.items():
        try:
            node = stage0_value(report, name)
            ok = (all(_same(node.get(k), spec[k]) for k in ("lo", "hi")) if "lo" in spec
                  else _same(node, spec["value"]))
        except (KeyError, TypeError, AttributeError):
            ok = False
        if not ok:
            bad.append(name)
    return {"status": "FAIL" if bad else "PASS", "mismatches": bad}


def g0_lo() -> Fraction:
    return Fraction(CONST_MAP["G_Parikh_32"]["lo"])


def g8_lo() -> Fraction:
    return Fraction(CONST_MAP["G_8_32"]["lo"])


def target_threshold() -> Fraction:
    return TARGET_FRAC * g0_lo()


def regret_bar(dw2_lo: Fraction) -> Fraction:
    return REGRET_FRAC * Fraction(dw2_lo)


def prec_delta() -> Fraction:
    return PREC_FRAC * g0_lo()


def ladder_lo(S) -> Fraction:
    return Fraction(CONST_MAP[_LADDER_NAMES[S]]["lo"])
