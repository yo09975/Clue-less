"""test_hallation.py"""
from src.hall import Hall


test_hall1 = Hall('Test Location 1')
test_hall2 = Hall('Test Location 2')
test_hall3 = Hall('Test Location 3')
test_hall4 = Hall('Test Location 4')
test_hall5 = Hall('Test Location 5')


def test_init():
    assert type(test_hall1) is Hall


def test_create_neighbors():
    if test_hall1.is_neighbor(test_hall2) is False:
        assert True
    else:
        assert False
    test_hall1.create_neighbors([test_hall2, test_hall3])
    if test_hall1.is_neighbor(test_hall2) is True:
        assert True
    else:
        assert False
    if test_hall1.is_neighbor(test_hall3) is True:
        assert True
    else:
        assert False
    if test_hall1.is_neighbor(test_hall4) is False:
        assert True
    else:
        assert False


def test_add_occupant():
    assert test_hall1.get_occupant_count() == 0
    assert type(test_hall1.add_occupant()) is bool
    assert test_hall1.get_occupant_count() == 1
    if test_hall1.add_occupant() is False:
        assert True
    else:
        assert False
    assert test_hall1.get_occupant_count() == 1


def test_get_occupant_count():
    assert test_hall1.get_occupant_count() == 1
    assert type(test_hall1.get_occupant_count()) is int


def test_remove_occupant():
    assert test_hall1.get_occupant_count() == 1
    if test_hall1.remove_occupant() is True:
        assert True
    else:
        assert False
    assert test_hall1.get_occupant_count() == 0
    assert type(test_hall1.remove_occupant()) is bool
    if test_hall1.remove_occupant() is False:
        assert True
    else:
        assert False
    assert test_hall1.get_occupant_count() == 0


def test_is_available():
    if test_hall1.is_available() is True:
        assert True
    else:
        assert False
    assert type(test_hall1.is_available()) is bool
    test_hall1.add_occupant()
    if test_hall1.is_available() is False:
        assert True
    else:
        assert False
