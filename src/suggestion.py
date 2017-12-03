"""suggestion.py"""

from src.card import Card
import json


class Suggestion:
    """The object that contains the room, weapon, and character Cards that comprise a 'suggestion.'

    """

    def __init__(self, room: Card, weapon: Card, character: Card):
        """Constructor. Creates a tuple of three Cards that represents a possible solution."""

        self.suggestion_set = (room, weapon, character)

    def get_suggestion_set(self):
        """Returns the tuple that represents all three suggested Cards."""

        return self.suggestion_set

    def get_room(self):
        """Returns the Card object that represents the suggested room."""

        return self.suggestion_set[0]

    def get_weapon(self):
        """Returns the Card object that represents the suggested weapon."""

        return self.suggestion_set[1]

    def get_character(self):
        """Returns the Card object that represents the suggested character."""

        return self.suggestion_set[2]

    def serialize(self):
        suggestions = {}
        for s in self.suggestion_set:
            suggestions[s.get_type()] = s.get_id()
        return json.dumps(suggestions)

    def deserialize(self, payload):
        suggestions = json.loads(payload)
        for s in suggestions:
            print(s.get_type)
            print(s.get_id)
