from card import Card
from player import Player
from cardtype import CardType


class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(
                SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class PlayerList(object):
    """Represents all Players in the game.

    PlayerList class in the Game Management Subsystem. Stores all Player
    objects in a list that is stored globally to allow for tracjing of game
    information such as turn sqeuencing, player location, etc. This class
    is a Singleton.
    """

    __metaclass__ = SingletonType

    __instance = None
    """Instance of the Singleton class"""
    _player_list = None
    """List of PLayer objects representing the Player order"""

    def __init__(self):
        """Constructor"""

    def get_instance(self):
        """Returns the instance of PlayerList"""
        return self.__instance

    def add_player(self, player: Player):
        """Accepts a Player object to add to the end of the list"""
        _player_list.append(Player)

    def get_next_turn(self) -> Player:
        """Returns the next active Player in the list"""
        return Player(Card(
            'get_next_turn Player', CardType.SUSPECT, 'Player123'))

    def get_next_player(self, after_player: Player) -> Player:
        """Accepts a Player object and returns Player that is next"""
        return Player(Card(
            'get_next_player Player', CardType.SUSPECT, 'Player123'))

    def get_players(self) -> list:
        """Returns a List of all Players"""
        return _player_list

    def get_player(self, uuid: str) -> Player:
        """Accepts a UUID and returns the corresponding Player object"""
        return Player(Card(uuid, CardType.SUSPECT, 'Player123'))
