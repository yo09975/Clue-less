"""gamestate.py."""

from src.player import Player
from src.playerlist import PlayerList
from src.card import Card
from src.cardtype import CardType
from src.gamestatus import GameStatus
from src.suggestion import Suggestion
from src.deck import Deck
from src.playerstatus import PlayerStatus
from src.network.servernetworkinterface import ServerNetworkInterface as SNI
from src.network.message import Message
from src.network.message import MessageType
import os
import json


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

        self.suspect_deck = Deck([])
        self.weapon_deck = Deck([])
        self.room_deck = Deck([])

        player_list = PlayerList()

        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card = Card(c['card_id'], CardType.SUSPECT)
                self.suspect_deck.add_card(card)
                player = Player(card)
                player.set_location(c['start'])
                try:
                    player_list.add_player(player)
                except IndexError:
                    # PlayerList was already initialized
                    pass
            elif c['type'] == 'weapon':
                card = Card(c['card_id'], CardType.WEAPON)
                self.weapon_deck.add_card(card)
            else:
                card = Card(c['card_id'], CardType.ROOM)
                self.room_deck.add_card(card)

    def start(self):
        """Start game by shuffling, dealing the solution, dealing cards."""

        # Init decks and shuffle
        self.suspect_deck.shuffle()
        self.weapon_deck.shuffle()
        self.room_deck.shuffle()

        # Deal solution
        room_sol = self.room_deck.deal()
        weapon_sol = self.weapon_deck.deal()
        suspect_sol = self.suspect_deck.deal()
        self._solution = Suggestion(room_sol, weapon_sol, suspect_sol)

        # Combine sorted cards into one deck and shuffle
        self._deck = self.suspect_deck + self.weapon_deck + self.room_deck
        self._deck.shuffle()

        # Deal cards to players
        while self._deck.get_cards():
            dealt_card = self._deck.deal()
            player = self.next_turn()
            hand = player.get_hand()
            hand.add_card(dealt_card)
            player.set_hand(hand)

        # Send each player their dealt cards (Hand)
        pl = PlayerList()
        sni = SNI()
        for p in pl.get_players():
            if p.get_status() == PlayerStatus.ACTIVE:
                msg_payload = p.get_hand().serialize()
                to_uuid = p.get_uuid()
                sni.send_message(to_uuid, Message(
                    sni.get_uuid(), MessageType.PLAYER_HAND, msg_payload))

        # Reset self._current_player
        self._current_player = len(pl) - 1
        first_player = self.next_turn()

    def next_turn(self) -> Player:
        """Returns the Player object who is the next player to take a turn"""
        # print('next_turn method in GameState class')
        p_list = PlayerList()
        next_player = p_list.get_next_turn(self._current_player)
        if next_player is not None:
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
