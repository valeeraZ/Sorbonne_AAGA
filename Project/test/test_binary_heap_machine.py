from hypothesis import given, strategies as st
from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule
from hypothesis.strategies import integers

from src.binary_min_heap import BinaryHeap


@given(st.lists(st.integers(min_value=1), unique=True, min_size=10, max_size=50))
def test_binary_heap(vals):
    bh = BinaryHeap()
    bh.build_heap(vals)
    vals = sorted(vals)
    for i in range(len(vals)):
        heap = bh.del_min()
        assert vals[i] not in heap


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
        min_val = bh.heap[1]
        bh_after_del_min = bh.del_min()
        assert min_val not in bh_after_del_min


TestBinaryHeaps = BinaryHeapMachine.TestCase
