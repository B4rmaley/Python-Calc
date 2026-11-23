from src.code1 import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_add1():
    assert add(-1, 1) == 1