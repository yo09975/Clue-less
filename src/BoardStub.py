"""BoardStub.py."""
import Board


class BoardStub(Board):
        """The gameboard."""

        def get_location(self, location_id):
            """Return a location from either a coordinate string or room id."""
            return "hall"
