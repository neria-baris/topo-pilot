"""C1' float64 model evaluation: exact float64 cast of the frozen float32 weights, activations
at resid_post_3/32, patched and tail-path logits, identity checks (API.md §8; protocol §5.1,
§5.4, §15.1). Logits of activation forwards are discarded unread (computation-order rule)."""

from __future__ import annotations

import hashlib

import c1_config
import numpy as np
import torch
from c1_records import C1GateFailure

from topo_pilot.learner import forward_with_patch
from topo_pilot.learner.stage import load_model

SITE, INDEX, BOS = c1_config.SITE, c1_config.INDEX, c1_config.BOS


def state_sha(model) -> str:
    h = hashlib.sha256()
    for key, value in sorted(model.state_dict().items()):
        t = value.detach().to(torch.float32).contiguous().cpu().numpy()
        h.update(key.encode() + str(t.dtype).encode() + str(t.shape).encode() + t.tobytes())
    return h.hexdigest()


def load_model64(checkpoint) -> tuple:
    torch.set_num_threads(1)
    model = load_model(checkpoint)
    originals = {k: v.detach().clone() for k, v in model.state_dict().items()}
    sha = state_sha(model)
    model64 = model.to(torch.float64).eval()
    for k, v in model64.state_dict().items():
        back = v.detach().to(originals[k].dtype)
        if not torch.equal(back, originals[k]):
            raise C1GateFailure("FAIL_TECHNICAL/MODEL", f"float64 round trip differs at {k}")
    return model64, sha


def model_inputs(named32) -> torch.Tensor:
    named32 = np.asarray(named32, dtype=np.int64)
    bos = np.full((named32.shape[0], 1), BOS, dtype=np.int64)
    return torch.from_numpy(np.hstack((bos, named32)))


def _batches(n, batch):
    for s in range(0, n, batch):
        yield slice(s, min(n, s + batch))


def activations(model64, inputs, batch=1024) -> np.ndarray:
    out = []
    with torch.no_grad():
        for sl in _batches(inputs.shape[0], batch):
            res = model64(inputs[sl], return_hooks=(SITE,))
            out.append(res.hooks[SITE][:, INDEX, :].to(torch.float64).numpy().copy())
            del res  # logits discarded unread
    return np.vstack(out)


def patched_logits(model64, inputs, a, batch=1024) -> np.ndarray:
    a = torch.as_tensor(np.asarray(a, dtype=np.float64))
    out = []
    with torch.no_grad():
        for sl in _batches(inputs.shape[0], batch):
            res = forward_with_patch(model64, inputs[sl], SITE, INDEX, a[sl])
            out.append(res.logits[:, INDEX].to(torch.float64).numpy().copy())
    return np.vstack(out)


def natural_logits(model64, inputs, batch=1024) -> np.ndarray:
    out = []
    with torch.no_grad():
        for sl in _batches(inputs.shape[0], batch):
            out.append(model64(inputs[sl]).logits[:, INDEX].to(torch.float64).numpy().copy())
    return np.vstack(out)


def tail_logits(model64, a) -> np.ndarray:
    with torch.no_grad():
        x = torch.as_tensor(np.asarray(a, dtype=np.float64))
        return model64.unembed(model64.ln_final(x)).to(torch.float64).numpy().copy()


def identity_patch_ok(model64, inputs, a) -> bool:
    return bool(np.array_equal(patched_logits(model64, inputs, a), natural_logits(model64, inputs)))


def _log_softmax(z) -> np.ndarray:
    return torch.log_softmax(torch.as_tensor(np.asarray(z, dtype=np.float64)), dim=-1).numpy()


def tail_identity(model64, inputs, a_forced) -> float:
    ref = _log_softmax(patched_logits(model64, inputs, a_forced))
    tail = _log_softmax(tail_logits(model64, a_forced))
    return float(np.max(np.abs(ref - tail)))
