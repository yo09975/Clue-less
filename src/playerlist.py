"""playerlist.py"""
from src.player import Player
from src.playerstatus import PlayerStatus
import json


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
            i = 1
            while i < len(self._player_list):
                """Creating index and adjusting to remain in bounds"""
                search_index = (current + i) % len(self._player_list)
                if self._player_list[search_index].get_status(
                        ) == PlayerStatus.ACTIVE:
                    return self._player_list[search_index]
                i += 1
            return None
        else:
            raise IndexError()

    def get_next_player(self, after_player: Player) -> Player:
        """Accepts a Player object and returns Player that is next"""
        if after_player in self._player_list:
            current_index = self._player_list.index(after_player)
            i = 1
            while i < len(self._player_list):
                """Creating index and adjusting to remain in bounds"""
                search_index = (current_index + i) % len(self._player_list)
                if (self._player_list[search_index].get_status(
                        ) == PlayerStatus.ACTIVE) or (
                    self._player_list[search_index].get_status(
                        ) == PlayerStatus.LOST):
                    return self._player_list[search_index]
                i += 1
            return None
        else:
            raise ValueError()

    def get_players(self) -> list:
        """Returns a List of all Players"""
        return self._player_list

    def get_player(self, card_id: str) -> Player:
        """Accepts a UUID and returns the corresponding Player object"""
        for player in self._player_list:
            if card_id == player.get_card_id():
                player_index = self._player_list.index(player)
                return self._player_list[player_index]
        return None

    def serialize(self):
        board = {}
        # Serialize where all players' locatations

        for p in PlayerList._player_list:
            board[p.get_card_id()] = p.get_current_location()

        return json.dumps(board)


    def deserialize(self, payload):
        pl = PlayerList()
        # Deserialize here
        board = json.loads(payload)
        for p in board:
            if board[p] is None:
                continue
            pl.get_player(p).set_location(board[p])
