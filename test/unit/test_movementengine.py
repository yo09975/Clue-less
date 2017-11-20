"""test_movementengine.py.

Ensure that the Movement Engine properly rejects and executes moves provided by
the Game Controller.

Beware!!! These tests are stateful. Modifying will likely
impact results of others.
"""

from src.movementengine import MovementEngine
from src.playerlist import PlayerList
from src.player import Player
from src.board import Board
from src.move import Move
from src.card import Card
from src.cardtype import CardType
from src.playerstatus import PlayerStatus

MIS_SCA_CARD = Card('Test Card 1 Name', CardType.SUSPECT, 'TEST111ID')
COL_MUS_CARD = Card('Test Card 2 Name', CardType.SUSPECT, 'TEST222ID')
MIS_SCA = Player(MIS_SCA_CARD)
MIS_SCA.set_status(PlayerStatus.ACTIVE)
COL_MUS = Player(COL_MUS_CARD)
COL_MUS.set_status(PlayerStatus.ACTIVE)
player_list = PlayerList()
player_list.add_player(MIS_SCA)
player_list.add_player(COL_MUS)

me = MovementEngine()

_4x0 = me._board.get_location("4x0")
_4x1 = me._board.get_location("4x1")
_5x1 = me._board.get_location("5x1")
_3x1 = me._board.get_location("3x1")
_6x2 = me._board.get_location("6x2")

def test_detect_illegal_move():
    """Ask the Movement Engine to check move to non-neighbor."""

    MIS_SCA.set_location(_4x0)
    COL_MUS.set_location(_6x2)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x0").get_occupant_count() == 1
    assert me._board.get_location("6x2").get_occupant_count() == 1

    move = Move(MIS_SCA.get_token(), _5x1._key)

    assert not me.is_valid_move(move)


def test_detect_move_to_occupied_passage():
    """Ask the Movement Engine to check a move to an occupied passage."""
    # Move character to passage blocking Miss Scarlet
    move = Move(COL_MUS.get_token(), _4x1._key)
    me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("4x0").get_occupant_count() == 1

    # Check validity of moving Miss Scarlett to newly occupied passage
    move2 = Move(MIS_SCA.get_token(), _4x1._key)
    assert not me.is_valid_move(move2)


def test_detect_move_to_unoccupied_passage():
    """Ask the Movement Engine to check a valid move."""
    # Move character out of Miss Scarlet's way
    move = Move(COL_MUS.get_token(), _5x1._key)
    me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("5x1").get_occupant_count() == 1
    assert me._board.get_location("4x0").get_occupant_count() == 1

    # Check validity of moving Miss Scarlett to newly unoccupied passage
    move2 = Move(MIS_SCA.get_token(), _4x1._key)
    assert me.is_valid_move(move2)


def test_detect_move_to_occupied_room():
    """Ask the Movement Engine to check validity of move to occupied room."""
    # Move Miss Scarlet out of her starting point
    move = Move(MIS_SCA.get_token(), _4x1._key)
    me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("5x1").get_occupant_count() == 1

    # Check validity of moving Miss Scarlet to Lounge
    move2 = Move(MIS_SCA.get_token(), _5x1._key)
    assert me.is_valid_move(move2)


def test_detect_move_to_unoccupied_room():
    """Ask the Movemetn Engine to check validity of move to empty room."""
    # Move player out of Lounge
    move = Move(COL_MUS.get_token(), _3x1._key)
    me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("3x1").get_occupant_count() == 1

    # Check validity of moving Miss Scarlet to Lounge
    move2 = Move(MIS_SCA.get_token(), _5x1._key)
    assert me.is_valid_move(move2)


def test_execute_non_neighbor_move():
    """Ensure MovementEngine.do_move() works when someone is suggested."""
    hall_occ = me._board.get_location("3x1").get_occupant_count()
    move = Move(MIS_SCA.get_token(), _3x1._key)

    assert me.is_valid_move(move)

    me.do_move(move)
    new_hall_occ = me._board.get_location("3x1").get_occupant_count()
    assert new_hall_occ == hall_occ + 1
