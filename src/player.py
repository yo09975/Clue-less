"""player.py."""
from src.hand import Hand
from src.card import Card
from src.location import Location
from src.playerstatus import PlayerStatus
from src.cardtype import CardType


class Player(object):
    """Represents a player in the game.

    Player class in the Game Management Subsystem. The object that represents
    each Player that is stored in teh active game's PlayerList.

    Attributes:
    _player_hand - Hand object that contains teh initial Cards dealt to the
                   Player
    _character - A Card object representing the Player's character
    _status - A flag representing the status of the Player
    _card_id - String representing the Player's suspect card
    _uuid - Player's unique ID for messaging
    _current_location - Player's current location on the gameboard
    _previous_location - Player's previous location on the gameboard
    _was_transferred - Boolean representing if the Player was moved to current
                       Location via a suggestion

    """

    def __init__(self, card: Card):
        """Constructor"""
        # print('Constructor in Player class')
        if not card.get_type() == CardType.SUSPECT:
            raise ValueError('Player constructor requires a Suspect Card')
        else:
            self._player_hand = Hand([])
            self._character = card
            self._status = PlayerStatus.COMP
            self._card_id = self.get_character().get_id()
            self._uuid = None
            self._current_location = None
            self._previous_location = None
            self._was_transferred = False

    def __str__(self) -> str:
        player_str = 'Player is playing as: '
        return player_str + self.get_character().get_id()

    def __eq__(self, other):
        """ Overridden equality check """
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False
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

    def set_status(self, status: PlayerStatus):
        """Changes the status of the Player"""
        # print('set_status method in Player class')
        self._status = status

    def get_status(self) -> PlayerStatus:
        """Returns an Enum representing the Player's current status"""
        # print('get_status method in Player class')
        return self._status

    def set_location(self, location: str):
        if type(location) is not str:
            raise TypeError('set_location expects a string index of a location')
        """Sets the Location to where the Player is on the gameboard"""
        # print('set_location method in Player class')
        if self._previous_location is None:
            self._previous_location = location
        else:
            self._previous_location = self._current_location
        self._current_location = location

    def get_current_location(self) -> str:
        """Return the Player's current Location"""
        return self._current_location

    def get_previous_location(self) -> str:
        """Return the Player's previous Location"""
        return self._previous_location

    def set_card_id(self, card_id: str):
        """Accepts a String to set the Player's unique token"""
        self._card_id = card_id

    def get_card_id(self) -> str:
        """Returns a String representing the Player's unique token"""
        return self._card_id

    def set_uuid(self, uuid: str):
        self._uuid = uuid

    def get_uuid(self) -> str:
        return self._uuid

    def set_was_transferred(self, transferred: bool):
        """Accepts a Boolean and sets if the Player was transferred via
        suggestion"""
        self._was_transferred = transferred

    def get_was_transferred(self) -> bool:
        """Returns a Boolean on whether the Player was moved to the current
        Location via a Suggestion"""
        return self._was_transferred
