"""board.py.

A map that allows the system to a Location on the Board by either its
coordinates on the grid, or by the room identifier.
"""
import json
import os
from src.hall import Hall
from src.location import Location
from src.playerlist import PlayerList


class Board:
    """The gameboard.

    A map that allows the system to a Location on the Board by either its
    coordinates on the grid, or by the room identifier.
    """

    def __init__(self):
        """Initialize board with information from data file."""

        self._locations = {}

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/locations.json')

        with open(filename) as data_file:
            location_data = json.load(data_file)

        # Initialize all locations without neighbors
        for l in location_data['locations']:
            if l['type'] == 'room':
                loc = Location(l['name'], l['key'])

                # Store the location with its room name as key
                self._locations[l['name']] = loc
            else:
                # Create a Hall
                loc = Hall(l['name'], l['key'])

            # Initialize starting locations
            if l.get('init', False):
                print("init ", l['key'])
                loc.add_occupant()

            # Store location with coordinates as key
            self._locations[l['key']] = loc

        # Add neighbors of each room
        for l in location_data['locations']:
            neighbors = []

            # Create a list of neighbor Locations
            for n in l['neighbors']:
                neighbor = self._locations[n]
                neighbors.append(neighbor)

            # Add neighbors to location
            self._locations[l['key']].create_neighbors(neighbors)

    def move(self, from_location, to_location):
        """Move a player from one location and to another."""
        if type(from_location) is not str or type(to_location) is not str:
            raise TypeError('to_location and from_location should be type str')
        if not self._locations[from_location].remove_occupant():
            #raise ValueError()
            return

        if not self._locations[to_location].add_occupant():
            # If you can't add occupant to the location, reverse the removal
            self._locations[from_location].add_occupant()
            #raise ValueError()

        return

    def get_location(self, location_id):
        """Return a location from either a coordinate string or room id."""
        return self._locations[location_id]


    def serialize(self):
        board = {}
        # Serialize where all players' locatations
        pl = PlayerList()
        for p in pl.get_players():
            board[p.get_card_id()] = p.get_current_location()

        return json.dumps(board)


    def deserialize(self, payload):
        pl = PlayerList()
        # Deserialize here
        board = json.loads(payload)

        # Clear board location's occpancy
        for l in self._locations:
            while self._locations[l].get_occupant_count() != 0:
                self._locations[l].remove_occupant()

        # Update locations in PlayerList and set occupancy in Board
        for p in board:
            if board[p] is None:
                continue
            pl.get_player(p).set_location(board[p])
            self._locations[board[p]].add_occupant()

        return self
