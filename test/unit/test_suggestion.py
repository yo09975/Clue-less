""" test_suggestion.py """
import pytest
from src.suggestion import Suggestion
from src.cardtype import CardType
from src.card import Card

room = Card('room', CardType.ROOM, 'room')
weapon = Card('weapon', CardType.WEAPON, 'weapon')
susp = Card('susp', CardType.SUSPECT, 'susp')

def test_create_valid_suggestion():
    suggestion_valid = Suggestion(room, weapon, susp)
    assert type(suggestion_valid) is Suggestion
    assert suggestion_valid.get_room() == room
    assert suggestion_valid.get_weapon() == weapon
    assert suggestion_valid.get_character() == susp

def test_create_invalid_suggestion():
    with pytest.raises(ValueError):
        suggestion_invalid = Suggestion(room, room, weapon)

def test_serialization():
    suggestion_valid = Suggestion(room, weapon, susp)
    payload = suggestion_valid.serialize()
    assert type(payload) is str
    sugg2 = Suggestion.deserialize(payload)
    assert type(sugg2) is Suggestion
    payload2 = sugg2.serialize()
    assert payload == payload2

def test_to_string():
    suggestion_valid = Suggestion(room, weapon, susp)
    assert str(suggestion_valid) == 'susp, with the weapon, in the room'
