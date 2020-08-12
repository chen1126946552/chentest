import pytest
def test_1():
    print("测试用例1111")
    assert 1 == 1


@pytest.mark.skip("跳过")
def test_2():
    print("测试用例22222")
    assert 1 == 1


def test_3():
    print("测试用例3333")


def test_4():
    print("测试用例44444444")
    assert 1 == 2