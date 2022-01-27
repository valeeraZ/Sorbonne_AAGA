from hypothesis import given, strategies as st

from src.binary_min_heap import BinaryHeap


@given(st.lists(st.integers(min_value=1), unique=True, min_size=10, max_size=50))
def test_binary_heap(vals):
    bh = BinaryHeap()
    bh.build_heap(vals)
    vals = sorted(vals)
    for i in range(len(vals)):
        heap = bh.del_min()
        assert vals[i] not in heap


if __name__ == "__main__":
    print("MAIN")
    test_binary_heap()
