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
    assert not test_hall1.is_neighbor(test_hall2)
    test_hall1.create_neighbors([test_hall2, test_hall3])
    assert test_hall1.is_neighbor(test_hall2)
    assert test_hall1.is_neighbor(test_hall3)
    assert not test_hall1.is_neighbor(test_hall4)


def test_add_occupant():
    assert test_hall1.get_occupant_count() == 0
    assert type(test_hall1.add_occupant()) is bool
    assert test_hall1.get_occupant_count() == 1
    assert not test_hall1.add_occupant()
    assert test_hall1.get_occupant_count() == 1


def test_get_occupant_count():
    assert test_hall1.get_occupant_count() == 1
    assert type(test_hall1.get_occupant_count()) is int


def test_remove_occupant():
    assert test_hall1.get_occupant_count() == 1
    assert test_hall1.remove_occupant()
    assert test_hall1.get_occupant_count() == 0
    assert type(test_hall1.remove_occupant()) is bool
    assert not test_hall1.remove_occupant()
    assert test_hall1.get_occupant_count() == 0


def test_is_available():
    assert test_hall1.is_available()
    assert type(test_hall1.is_available()) is bool
    test_hall1.add_occupant()
    assert not test_hall1.is_available()
