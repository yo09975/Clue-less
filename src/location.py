"""location.py."""


class Location(object):
    """Represents a space on the game board

    Location class in the Game Management Subsystem. Location class will be
    used to store information on game board spaces.

    Attributes:
    _name - String representing the name of the Location
    _neighbors - List of Locations that are adjacent to the self Location
                 representing possible valid moves
    _occupants - Integer representing the Location's current number of
                 occupants
    _key - String representing the Location's coordinates on the board (XxY)

    """

    def __init__(self, name: str, key: str):
        """Constructor"""
        # print('Constructor in Location class')
        self._name = name
        self._occupants = 0
        self._neighbors = []
        self._key = key

    def create_neighbors(self, neighbors: list):
        """Accepts a List of Locations to set Locations adjacent to self
        Location"""
        # print('add_neighbors method in Location class')
        self._neighbors = neighbors

    def is_neighbor(self, destination) -> bool:
        """Accepts a Location and returns a Boolean on whether it is a neighbor
        to the self Location"""
        # print('is_neighbor method in Location class')
        return (destination in self._neighbors)

    def add_occupant(self) -> bool:
        """Increments the number of occupants in the Location. Returns a boolean
        if adding the occupant was successful of not."""
        # print('add_occupant method in Location class')
        if self._occupants > 5:
            print('!!! ERROR MORE OCCUPANTS THAN TOTAL SUSPECTS IN GAME !!!')
            return False
        else:
            self._occupants += 1
            return True

    def get_occupant_count(self) -> int:
        """Returns an Integer representing the current number of occupants"""
        return self._occupants

    def remove_occupant(self) -> bool:
        """Decrements the number of occupants in the Location"""
        # print('remove_occupant method in Location class')
        if self._occupants == 0:
            print('!!! ERROR LOCATION EMPTY CANNOT REMOVE AN OCCUPANT !!!')
            return False
        else:
            self._occupants -= 1
            return True

    def is_available(self) -> bool:
        """Returns a Boolean on whether the referenced Location is available
        for more occupants. Will return True unless overridden."""
        # print('is_available method in Location class')
        return True

    def get_key(self) -> str:
        """ Return the Location's coordinates in a string, formatted "XxY"."""
        return self._key

    def get_name(self) -> str:
        """ Return the Location's name """
        return self._name
