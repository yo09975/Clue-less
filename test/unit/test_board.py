"""test_board.py.

Performs basic tests to ensure that Board is configured and functioning
properly.
"""

from src.board import Board
import pytest
import json
import os


dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../../data/locations.json')

# Load all locations
with open(filename) as data_file:
    location_data = json.load(data_file)


def test_init_fetch_by_name():
    """Fetch by name.

    Request all rooms from Board by name, and verify that the object
    returned has the same name.
    """
    b = Board()

    # Iterate through all locations and only request Rooms by name
    for l in location_data['locations']:
        if l['type'] == 'room':
            loc = b.get_location(l['name'])
            assert loc._name == l['name']


def test_init_fetch_by_coordinates():
    """Fetch by coordinates.

    Request all locations by coordinates on the game board, and verify that
    the returned object has a name that corresponds to the location.
    """
    b = Board()

    # Iterate through all locations
    for l in location_data['locations']:
        loc = b.get_location(l['key'])
        assert loc._key == l['key']


def test_init_initial_locations():
    """Test that all game pieces are in correct inital locations."""

    b = Board()

    assert b.get_location("4x0").get_occupant_count() == 1


def test_manage_occupancy():
    """Test that the board is properly managing occupancy after moves."""
    b = Board()

    _4x0 = b.get_location("4x0")
    _4x1 = b.get_location("4x1")
    hall = b.get_location("3x1")
    _2x1 = b.get_location("2x1")
    _1x1 = b.get_location("1x1")
    _1x2 = b.get_location("1x2")

    # Move person from
    b.move(_4x0, _4x1)
    b.move(_4x1, hall)
    b.move(hall, _2x1)
    b.move(_2x1, _1x1)
    b.move(_1x1, _1x2)

    # Check occupancy is correct
    assert _4x0.get_occupant_count() == 0
    assert _4x1.get_occupant_count() == 0
    assert hall.get_occupant_count() == 0
    assert _2x1.get_occupant_count() == 0
    assert _1x1.get_occupant_count() == 0
    assert _1x2.get_occupant_count() == 1


def test_invalid_current_location():
    """Catch condition in which Board is told to move from empty location."""
    b = Board()

    hall = b.get_location("3x1")
    _2x1 = b.get_location("2x1")

    with pytest.raises(ValueError) as e:
        b.move(hall, _2x1)


def test_invalid_destination():
    """Catch condition in which Board is told to move to occupied location."""
    b = Board()

    _4x0 = b.get_location("4x0")
    _4x1 = b.get_location("4x1")
    _4x1.add_occupant()

    with pytest.raises(ValueError) as e:
        b.move(_4x0, _4x1)

        assert _4x0.get_occupant_count() == 1
        assert _4x1.get_occupant_count() == 0
