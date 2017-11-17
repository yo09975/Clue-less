"""playerlist.py"""
from src.player import Player


class PlayerList:
    """Represents all Players in the game.

    PlayerList class in the Game Management Subsystem. Stores all Player
    objects in a list that is stored globally to allow for tracjing of game
    information such as turn sqeuencing, player location, etc. This class
    is a Singleton.
    """

    _player_list = []
    """List of Player objects representing the Player order"""

    class __impl:
        """Implementation of the Singleton class"""

    __instance = __impl()
    """The private class attribute holding the "one and only instance"""

    def get_instance(self):
        """Returns the instance of PlayerList"""
        return self.__instance

    def add_player(self, player: Player):
        """Accepts a Player object to add to the end of the list"""
        self._player_list.append(player)

    def get_next_turn(self, current: int) -> Player:
        """Returns the next active Player in the list"""
        if (current < len(self._player_list)) and (current > -1):
            next_player = (current + 1) % len(self._player_list)
            return self._player_list[next_player]
        else:
            return None

    def get_next_player(self, after_player: Player) -> Player:
        """Accepts a Player object and returns Player that is next"""
        if after_player in self._player_list:
            current_index = self._player_list.index(after_player)
            next_player = (current_index + 1) % len(self._player_list)
            return self._player_list[next_player]
        else:
            return None

    def get_players(self) -> list:
        """Returns a List of all Players"""
        return self._player_list

    def get_player(self, uuid: str) -> Player:
        """Accepts a UUID and returns the corresponding Player object"""
        for player in self._player_list:
            if uuid == player.get_token():
                player_index = self._player_list.index(player)
                return self._player_list[player_index]
        return None
