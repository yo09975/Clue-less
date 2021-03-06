"""playerlist.py"""
from src.player import Player
from src.playerstatus import PlayerStatus
from src.network.singleton import Singleton
from src.card import Card, CardType
import os
import json

class PlayerList(metaclass=Singleton):
    """Represents all Players in the game.

    PlayerList class in the Game Management Subsystem. Stores all Player
    objects in a list that is stored globally to allow for tracing of game
    information such as turn sequencing, player location, etc. This class
    is a Singleton.
    """

    # List of Player objects representing the Player order
    _player_list = []
    # Maximum number of players in the game
    __MAX_PLAYERS = 6

    def add_player(self, player: Player):
        """Accepts a Player object to add to the end of the list"""
        if len(self._player_list) == self.__MAX_PLAYERS:
            raise IndexError(f'Attempted to add more than {self.__MAX_PLAYERS} players')
        self._player_list.append(player)

    def get_next_turn(self, current: int) -> Player:
        """Returns the next active Player in the list"""
        if (current < len(self._player_list)) and (current > -1):
            i = 1
            while i < len(self._player_list):
                """Creating index and adjusting to remain in bounds"""
                search_index = (current + i) % len(self._player_list)
                player = self.get_player_by_index(search_index)
                if player.get_status() == PlayerStatus.ACTIVE:
                    return player
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
                player = self.get_player_by_index(search_index)
                if (player.get_status() == PlayerStatus.ACTIVE) or \
                   (player.get_status() == PlayerStatus.LOST):
                    return self._player_list[search_index]
                i += 1
            return None
        else:
            raise ValueError()

    def get_players(self) -> list:
        """Returns a List of all Players"""
        return self._player_list

    def get_player(self, card_id: str) -> Player:
        """
        Searches the PlayerList for the Player object associated with a given
        card_id string and returns it
        """
        for player in self._player_list:
            if card_id == player.get_card_id():
                player_index = self._player_list.index(player)
                return self._player_list[player_index]
        return None

    def get_player_by_index(self, index: int) -> Player:
        return self._player_list[index]

    def clear(self):
        self._player_list = []

    def setup(self):
            # Read cards datafile and initialize Deck
            dir = os.path.dirname(__file__)
            filename = os.path.join(dir, '../data/cards.json')

            with open(filename) as data_file:
                card_data = json.load(data_file)

            for c in card_data['cards']:
                if c['type'] == 'suspect':
                    card = Card(c['card_id'], CardType.SUSPECT)
                    player = Player(card)
                    player.set_location(c['start'])
                    try:
                        self.add_player(player)
                    except IndexError:
                        # PlayerList was already initialized
                        pass


    def __len__(self):
        return len(self._player_list)

    def serialize(self):
        """ Convert a Move to JSON """
        playerlist={}
        for player in self._player_list:
            playerlist[player.get_card_id()] = {}
            playerlist[player.get_card_id()]['uuid'] = player.get_uuid()
            playerlist[player.get_card_id()]['card'] = player.get_character().serialize()
        return json.dumps(playerlist)

    def deserialize(payload):
        """ Convert a JSON string to a Player List """
        pl = PlayerList()
        pl.clear()

        playerlist = json.loads(payload)
        for key in playerlist:
            newplayer = Player(Card.deserialize(playerlist[key]['card']))
            newplayer.set_uuid(playerlist[key]['uuid'])
            pl.add_player(newplayer)
        return pl
