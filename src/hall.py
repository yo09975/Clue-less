from location import Location


class Hall(Location):
    """Represents a Hall space on the game board

    Hall class in the Game Management Subsystem. Hall extends Location.
    """

    def __init__(self, name: str):
        """Constructor"""
        # print('Constructor in Hall class')
        super(Hall, self).__init__(name)

    def add_occupant(self):
        """Increments the number of occupants in the Hall"""
        # print('add_occupant method in Hall class')
        if self.get_occupant_count() > 0:
            print('!!! ERROR CANNOT HAVE MORE THAN ONE IN HALL !!!')
        else:
            self._occupants += 1

    def is_available(self) -> bool:
        """Returns a Boolean on whether the Hall is available for an
        occupant."""
        # print('is_available method in Hall class')
        return not (self._occupants > 0)
