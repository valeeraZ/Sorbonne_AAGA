from src.remy_valid import test_covering


def test_remy_uniform():
    n = 4
    assert all([test_covering(i) for i in range(n)])
