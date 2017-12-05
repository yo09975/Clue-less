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
        suggestion = {}
        suggestion['room'] = self.get_room().serialize()
        suggestion['weapon'] = self.get_weapon().serialize()
        suggestion['character'] = self.get_character().serialize()
        return json.dumps(suggestion)

    def deserialize(payload):
        suggestion = json.loads(payload)
        room = Card.deserialize(suggestion['room'])
        weapon = Card.deserialize(suggestion['weapon'])
        character = Card.deserialize(suggestion['character'])
        return Suggestion(room, weapon, character)

    def __str__(self):
        return self.get_character().get_name() + ", with the " + \
        self.get_weapon().get_name() + ", in the " + self.get_room().get_name()
