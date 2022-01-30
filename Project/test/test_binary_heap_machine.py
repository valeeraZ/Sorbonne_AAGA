from hypothesis import given, strategies as st
from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule
from hypothesis.strategies import integers

from src.binary_min_heap import BinaryHeap


@given(st.lists(st.integers(min_value=1), unique=True, min_size=10, max_size=50))
def test_binary_heap(vals):
    bh = BinaryHeap()
    bh.build_heap(vals)
    vals.sort()
    for i in range(len(vals)):
        min, _ = bh.del_min()
        assert min == vals[i]


class BinaryHeapMachine(RuleBasedStateMachine):
    BinaryHeaps = Bundle('BinaryHeaps')

    @rule(target=BinaryHeaps)
    def new_heap(self):
        return BinaryHeap()

    @rule(bh=BinaryHeaps, value=integers())
    def insert(self, bh, value):
        bh.insert(value)

    @rule(bh=BinaryHeaps.filter(lambda bh: len(bh.heap) > 2))
    def test_del_min(self, bh):
        bh_before_del = bh.return_heap()
        min_val, bh_after_del_min = bh.del_min()
        assert len(bh_after_del_min) == len(bh_before_del) - 1
        assert all(map(lambda x: min_val <= x, bh_after_del_min))


TestBinaryHeaps = BinaryHeapMachine.TestCase
