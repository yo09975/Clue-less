"""test_board.py.

Performs basic tests to ensure that Board is configured and functioning
properly.
"""

from src.board import Board
import json
import os


def test_init_fetch_by_name():
    """Fetch by name.

    Request all rooms from Board by name, and verify that the object
    returned has the same name.
    """

    b = Board()

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../data/locations.json')

    # Load all locations
    with open(filename) as data_file:
        location_data = json.load(data_file)

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

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../../data/locations.json')

    # Load all locations
    with open(filename) as data_file:
        location_data = json.load(data_file)

    # Iterate through all locations
    for l in location_data['locations']:
        loc = b.get_location(l['key'])
        assert loc._name == l['name']
