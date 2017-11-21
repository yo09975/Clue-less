"""gamestate.py."""

from src.player import Player
from src.playerlist import PlayerList
from src.card import Card
from src.cardtype import CardType
from src.gamestatus import GameStatus
from src.suggestion import Suggestion


class GameState(object):
    """Contains all required information about a game.

    GameState class in the Game Management Subsystem.  GameState class will
    be used to contain everything that is needed in a game. A loop will
    iterate through players in the game and allow them to perform turns
    until some sort of game over flag is flipped.

    _solution - Instance of Suggestion object containing winning game solution
    _state - Enum value representing the current state of the game
    _current_player - Index of player in PlayerList whose turn it is

    """

    def __init__(self):
        """Constructor"""
        # print('Constructor in GameState class')
        self._solution = None
        self._state = GameStatus.LOBBY
        self._current_player = 0

        # Read cards datafile and initialize Deck
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/cards.json')

        with open(filename) as data_file:
            card_data = json.load(data_file)

        # Initialize all locations without neighbors
        cards = []
        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card_type = CardType.SUSPECT
            elif c['type'] == 'weapon':
                card_type = CardType.WEAPON
            else:
                card_type = CardType.ROOM
            card = Card(c['name'], card_type, c['key'])

            # Initialize a new player and their location, add to PlayerList
            if c['type'] == 'suspect':
                player = Player(card)
                player.set_location(c['start'])

                player_list = PlayerList()
                player_list.add_player(player)

            # Add card to list for addition to Deck later
            cards.append(card)

        self.deck = Deck(cards)

    def next_turn(self) -> Player:
        """Returns the Player object who is the next player to take a turn"""
        # print('next_turn method in GameState class')
        p_list = PlayerList()
        next_player = p_list.get_next_turn(self._current_player)
        self._current_player = p_list.get_players().index(next_player)
        return next_player

    def get_state(self) -> GameStatus:
        """Returns the current state of the game"""
        # print('get_state method in GameState class')
        return self._state

    def set_state(self, state: GameStatus):
        """Accepts an Enum to set the state of the game"""
        # print('set_state method in GameState class')
        self._state = state

    def get_solution(self) -> Suggestion:
        """Returns a Suggestion object representing the game's solution"""
        # print('get_solution method in GameState class')
        return self._solution

    def set_solution(self, solution: Suggestion):
        """Accepts a Suggestion object to set the game's solution"""
        # print('set_solution method in GameState class')
        self._solution = solution

    def get_current_player(self) -> int:
        """Returns an Integer representing the player whose turn it is"""
        # print('get_current_player method in GameState class')
        return self._current_player

    def set_current_player(self, player_index: int):
        """Accepts an integer to set the current player"""
        # print('set_current_player method in GameState class')
        self._current_player = player_index
