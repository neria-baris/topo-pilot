import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, SequenceLayout, StageFailure

pytestmark = pytest.mark.contracts

ROW = [3, 1, 4, 1, 0, 2, 2, 4, 0, 1, 3, 3, 1, 4, 0, 2, 1,
       1, 3, 4, 0, 0, 2, 4, 3, 1, 2, 3, 0, 4, 4, 1, 2]
assert len(ROW) == 33


def test_C11_inputs_targets_history_known_answer():
    L = SequenceLayout()
    V = 5
    tokens = np.array([ROW, ROW[::-1]], dtype=np.uint8)
    assert L.bos_id(V) == 5
    x = L.model_inputs(tokens, V)
    assert x.shape == (2, 33) and x.dtype == np.int64
    assert x[0].tolist() == [5] + ROW[:32]
    assert x[1].tolist() == [5] + ROW[::-1][:32]
    y = L.targets(tokens)
    assert y.shape == (2, 33) and y.dtype == np.int64
    assert y[0].tolist() == ROW and y[1].tolist() == ROW[::-1]
    # analysis position p = 32: input w_32 (ROW[31]), target w_33 (ROW[32]), history w_1..w_32
    p = L.analysis_position
    assert p == 32 and L.context == 32 and L.n_obs == 33
    assert x[0, p] == ROW[31] and y[0, p] == ROW[32]
    assert L.history(tokens[0], p).tolist() == ROW[:32]
    for pos in range(1, 33):
        assert x[0, pos] == ROW[pos - 1] and y[0, pos] == ROW[pos]
    assert y[0, 0] == ROW[0]  # BOS predicts w_1


def test_C11_history():
    L = SequenceLayout()
    row = np.array(ROW, dtype=np.uint8)
    assert L.history(row, 0).size == 0
    assert L.history(row, 1).tolist() == [3]
    assert L.history(row, 3).tolist() == [3, 1, 4]
    assert L.history(row, 32).tolist() == ROW[:32]


def test_C11_targets_is_a_copy():
    L = SequenceLayout()
    tokens = np.array([ROW], dtype=np.int64)
    L.targets(tokens)[0, 0] = 99
    assert tokens[0, 0] == 3


@pytest.mark.parametrize("call", [
    lambda L: L.model_inputs(np.zeros((2, 32), dtype=np.uint8), 5),
    lambda L: L.model_inputs(np.zeros((33,), dtype=np.uint8), 5),
    lambda L: L.model_inputs(np.zeros((2, 33), dtype=np.float64), 5),
    lambda L: L.targets(np.zeros((2, 34), dtype=np.int64)),
    lambda L: L.targets(np.zeros((33,), dtype=np.int64)),
    lambda L: L.history(np.zeros(32, dtype=np.int64), 3),
    lambda L: L.history(np.zeros((2, 33), dtype=np.int64), 3),
    lambda L: L.history(np.zeros(33, dtype=np.int64), 33),
    lambda L: L.history(np.zeros(33, dtype=np.int64), -1),
])
def test_C11_alignment_errors(call):
    with pytest.raises(StageFailure) as ei:
        call(SequenceLayout())
    assert ei.value.code == ErrorCode.ALIGNMENT_ERROR
