"""test_board.py.

Performs basic tests to ensure that Board is configured and functioning
properly.
"""

from src.board import Board
from src.gamestate import GameState
from src.playerlist import PlayerList
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


gs = GameState()
pl = PlayerList()


def test_serialize_locations():
    b = Board()
    payload = b.serialize()
    assert type(payload) is str
    # Ensure that Col. Mustard's starting location is serialized
    assert payload.find('"Colonel Mustard": "6x2"') != -1


def test_deserialize_locations():
    # Invoke GameState so that starting positions are initialized
    b = Board()
    payload = b.serialize()

    # Change Col. Mustard's location and test to see if serialization worked
    payload = payload.replace("6x2", "5x2")
    b.deserialize(payload)

    # Check to see if PlayerList has correct location
    COL = pl.get_player("Colonel Mustard")
    assert COL.get_current_location() == "5x2"

    # Check to see if Board has correct occupancy for new and old location
    assert b.get_location("5x2").get_occupant_count() == 1
    assert b.get_location("6x2").get_occupant_count() == 0
