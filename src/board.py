"""board.py.

A map that allows the system to a Location on the Board by either its
coordinates on the grid, or by the room identifier.
"""
import json
import os
from src.hall import Hall
from src.location import Location


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
                loc = Location(l['name'])

                # Store the location with its room name as key
                self._locations[l['name']] = loc
            else:
                # Create a Hall
                loc = Hall(l['name'])

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
        self._locations[from_location].remove_occupant()
        self._locations[to_location].add_occupant()

        return

    def get_location(self, location_id):
        """Return a location from either a coordinate string or room id."""
        return self._locations[location_id]
