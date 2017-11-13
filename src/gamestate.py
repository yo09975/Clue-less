"""gamestate.py."""

from player import Player
from card import Card
from cardtype import CardType
from enum import Enum


class GameState(object):
    """Contains all required information about a game.

    GameState class in the Game Management Subsystem.  GameState class will
    be used to contain everything that is needed in a game. A loop will
    iterate through players in the game and allow them to perform turns
    until some sort of game over flag is flipped.

    solution - Instance of Suggestion object containing winning game solution
    state - Enum value representing the current state of the game
    current_player - Index of player in PlayerList whose turn it is

    """

    def __init__(self):
        """Constructor"""
        print('Constructor in GameState class')
        self.solution = None
        self.state = None
        self.current_player = None

    def next_turn(self) -> Player:
        """Returns the Player object who is the next player to take a turn"""
        print('next_turn method in GameState class')
        return Player(Card(
            'next_turn Player', CardType.SUSPECT, 'Player123'))

    def get_state(self) -> Enum:
        """Returns the current state of teh game"""
        print('get_state method in GameState class')
        return Enum('get_state')

    def set_state(self, state: Enum):
        """Accepts an Enum to set the state of the game"""
        print('set_state method in GameState class')

    def get_solution(self):
        """Returns a Suggestion object representing the game's solution"""
        print('get_solution method in GameState class')
        return 'SUGGESTION OBJECT'

    def set_solution(self, solution):
        """Accepts a Suggestion object to set the game's solution"""
        print('set_solution method in GameState class')

    def get_current_player(self):
        """Returns an Integer representing the player whose turn it is"""
        return 999
