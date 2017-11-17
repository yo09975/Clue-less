"""test_location.py"""
from src.location import Location

test_loc1 = Location('Test Location 1')
test_loc2 = Location('Test Location 2')
test_loc3 = Location('Test Location 3')
test_loc4 = Location('Test Location 4')
test_loc5 = Location('Test Location 5')


def test_init():
    assert type(test_loc1) is Location


def test_create_neighbors():
    if test_loc1.is_neighbor(test_loc2) is False:
        assert True
    else:
        assert False
    test_loc1.create_neighbors([test_loc2, test_loc3])
    if test_loc1.is_neighbor(test_loc2) is True:
        assert True
    else:
        assert False
    if test_loc1.is_neighbor(test_loc3) is True:
        assert True
    else:
        assert False
    if test_loc1.is_neighbor(test_loc4) is False:
        assert True
    else:
        assert False


def test_add_occupant():
    assert test_loc1.get_occupant_count() == 0
    test_loc1.add_occupant()
    assert test_loc1.get_occupant_count() == 1
    assert type(test_loc1.add_occupant()) is bool
    if test_loc1.add_occupant() is True:
        assert True
    else:
        assert False
    test_loc1.add_occupant()
    test_loc1.add_occupant()
    test_loc1.add_occupant()
    assert test_loc1.get_occupant_count() == 6
    if test_loc1.add_occupant() is False:
        assert True
    else:
        assert False
    assert test_loc1.get_occupant_count() == 6


def test_get_occupant_count():
    assert test_loc1.get_occupant_count() == 6
    assert type(test_loc1.get_occupant_count()) is int


def test_remove_occupant():
    assert test_loc1.get_occupant_count() == 6
    test_loc1.remove_occupant()
    assert test_loc1.get_occupant_count() == 5
    assert type(test_loc1.remove_occupant()) is bool
    test_loc1.remove_occupant()
    test_loc1.remove_occupant()
    test_loc1.remove_occupant()
    test_loc1.remove_occupant()
    assert test_loc1.get_occupant_count() == 0
    if test_loc1.remove_occupant() is False:
        assert True
    else:
        assert False


def test_is_available():
    if test_loc1.is_available() is True:
        assert True
    else:
        assert False
    assert type(test_loc1.is_available()) is bool
