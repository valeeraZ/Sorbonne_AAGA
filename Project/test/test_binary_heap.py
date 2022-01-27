from hypothesis import given, strategies as st

from src.binary_heap_min import BinaryHeap


@given(st.lists(st.integers(min_value=1), unique=True, min_size=10, max_size=50))
def test_binary_heap(vals):
    bh = BinaryHeap()
    bh.buildHeap(vals)
    vals = sorted(vals)
    for i in range(len(vals)):
        heap = bh.delMin()
        assert vals[i] not in heap
