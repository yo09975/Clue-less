"""player.py."""
from enum import Enum
from hand import Hand
from card import Card
from location import Location


class Player(object):
    """Represents a player in the game.

    Player class in the Game Management Subsystem. The object that represents
    each Player that is stored in teh active game's PlayerList.

    Attributes:
    _player_hand - Hand object that contains teh initial Cards dealt to the
                   Player
    _character - A Card object representing the Player's character
    _status - A flag representing the status of the Player
    _token - String representing a unique Player identifier
    _current_location - Player's current location on the gameboard
    _previous_location - Player's previous location on the gameboard
    _was_transferred - Boolean representing if the Player was moved to current
                       Location via a suggestion

    """

    def __init__(self, card: Card):
        """Constructor"""
        # print('Constructor in Player class')
        self._player_hand = None
        self._character = card
        self._status = None
        self._token = None
        self._current_location = None
        self._previous_location = None
        self._was_transferred = None

    def set_hand(self, hand: Hand):
        """Creates the Player's initial Hand of Cards"""
        self._player_hand = hand

    def get_hand(self) -> Hand:
        """Return's the Player's Hand of Cards"""
        return self._player_hand

    def set_character(self, character: Card):
        """Accepts a Card to set a Player's character"""
        self._character = character

    def get_character(self) -> Card:
        """Returns a Card representing a Player's character"""
        return self._character

    def set_status(self, status: Enum):
        """Changes the status of the Player"""
        # print('set_status method in Player class')
        self._status = status

    def get_status(self) -> Enum:
        """Returns an Enum representing the Player's current status"""
        # print('get_status method in Player class')
        return self._status

    def set_location(self, location: Location):
        """Sets the Location to where the Player is on the gameboard"""
        # print('set_location method in Player class')
        self._previous_location = self._current_location
        self._current_location = location

    def get_current_location(self) -> Location:
        """Return the Player's current Location"""
        return self._current_location

    def get_previous_location(self) -> Location:
        """Return the Player's previous Location"""
        return self._previous_location

    def set_token(self, token: str):
        """Accepts a String to set the Player's unique token"""
        self._token = token

    def get_token(self) -> str:
        """Returns a String representing the Player's unique token"""
        return self._token

    def set_was_transferred(self, transferred: bool):
        """Accepts a Boolean and sets if the Player was transferred via
        suggestion"""
        self._was_transferred = transferred

    def get_was_transferred(self) -> bool:
        """Returns a Boolean on whether the Player was moved to the current
        Location via a Suggestion"""
        return self._was_transferred
