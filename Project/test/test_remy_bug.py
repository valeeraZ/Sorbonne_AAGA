from src.remy_bug import test_covering


def test_remy_uniform():
    assert not all([test_covering(i) for i in range(9)])
