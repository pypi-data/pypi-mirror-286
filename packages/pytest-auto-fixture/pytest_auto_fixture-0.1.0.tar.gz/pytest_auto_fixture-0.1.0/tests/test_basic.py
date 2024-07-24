import pytest


@pytest.fixture
def one():
    return 1


@pytest.fixture
def two():
    return 2


@pytest.fixture
def three(one, two):
    return one + two


def test_explicit(one):
    assert one == 1


def test_implicit():
    assert one == 1


def test_three():
    assert one == 1
    assert two == 2
    assert three == 3
