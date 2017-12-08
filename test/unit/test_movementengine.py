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
from src.gamestate import GameState
# Create two cards from the data in the data file
player_list = PlayerList()
gs = GameState()
scarlet_card = Card('Miss Scarlet', CardType.SUSPECT, 'Miss Scarlet')
mustard_card = Card('Colonel Mustard', CardType.SUSPECT, 'Colonel Mustard')
scarlet_player = player_list.get_player(scarlet_card.get_id())
scarlet_player.set_status(PlayerStatus.ACTIVE)
mustard_player = player_list.get_player(mustard_card.get_id())
mustard_player.set_status(PlayerStatus.ACTIVE)

me = MovementEngine()

_4x0 = me._board.get_location("4x0")
_4x1 = me._board.get_location("4x1")
_5x1 = me._board.get_location("5x1")
_3x1 = me._board.get_location("3x1")
_6x2 = me._board.get_location("6x2")

def test_serialize_move():
    """ Test that serializing a Move object gives the correct string """
    move = Move(scarlet_player.get_card_id(), _4x0._key)
    move_serial = move.serialize()
    assert move_serial.find(f'"character": "Miss Scarlet", "destination": "{_4x0._key}"') != -1

def test_deserialize_move():
    """ Test that deserializing a Move string gives the correct object """
    move = Move(scarlet_player.get_card_id(), _4x0._key)
    move_serial = move.serialize()
    move_deserialized = Move.deserialize(move_serial)
    assert move_deserialized.get_character_id() == move.get_character_id()
    assert move_deserialized.get_destination() == move.get_destination()

def test_detect_illegal_move():
    """Ask the Movement Engine to check move to non-neighbor."""
    scarlet_player.set_location(_4x0._key)
    mustard_player.set_location(_6x2._key)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x0").get_occupant_count() == 1
    assert me._board.get_location("6x2").get_occupant_count() == 1

    move = Move(scarlet_player.get_card_id(), _5x1._key)

    assert not me.is_valid_move(move)


def test_detect_move_to_occupied_passage():
    """Ask the Movement Engine to check a move to an occupied passage."""
    # Move character to passage blocking Miss Scarlet
    move = Move(mustard_player.get_card_id(), _4x1._key)
    assert me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("4x0").get_occupant_count() == 1

    # Check validity of moving Miss Scarlett to newly occupied passage
    move2 = Move(scarlet_player.get_card_id(), _4x1._key)
    assert not me.is_valid_move(move2)


def test_detect_move_to_unoccupied_passage():
    """Ask the Movement Engine to check a valid move."""
    # Move character out of Miss Scarlet's way
    move = Move(mustard_player.get_card_id(), _5x1._key)
    assert me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("5x1").get_occupant_count() == 1
    assert me._board.get_location("4x0").get_occupant_count() == 1

    # Check validity of moving Miss Scarlett to newly unoccupied passage
    move2 = Move(scarlet_player.get_card_id(), _4x1._key)
    assert me.is_valid_move(move2)


def test_detect_move_to_occupied_room():
    """Ask the Movement Engine to check validity of move to occupied room."""
    # Move Miss Scarlet out of her starting point
    move = Move(scarlet_player.get_card_id(), _4x1._key)
    assert me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("5x1").get_occupant_count() == 1

    # Check validity of moving Miss Scarlet to Lounge
    move2 = Move(scarlet_player.get_card_id(), _5x1._key)
    assert me.is_valid_move(move2)


def test_detect_move_to_unoccupied_room():
    """Ask the Movemetn Engine to check validity of move to empty room."""
    # Move player out of Lounge
    move = Move(mustard_player.get_card_id(), _3x1._key)
    assert me.do_move(move)

    # Sanity check - characters are in locations
    assert me._board.get_location("4x1").get_occupant_count() == 1
    assert me._board.get_location("3x1").get_occupant_count() == 1

    # Check validity of moving Miss Scarlet to Lounge
    move2 = Move(scarlet_player.get_card_id(), _5x1._key)
    assert me.is_valid_move(move2)
    assert me.do_move(move2)


def test_execute_non_neighbor_move():
    """Ensure MovementEngine.do_move() works when someone is suggested."""
    hall_occ = me._board.get_location("3x1").get_occupant_count()
    move = Move(scarlet_player.get_card_id(), _3x1._key)

    assert not me.is_valid_move(move)

    assert me.do_move(move)
    new_hall_occ = me._board.get_location("3x1").get_occupant_count()
    assert new_hall_occ == hall_occ + 1
