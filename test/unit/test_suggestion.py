
from src.suggestion import Suggestion
from src.cardtype import CardType
from src.card import Card

room = Card('room', CardType.ROOM, 'room')
weapon = Card('weapon', CardType.WEAPON, 'weapon')
susp = Card('susp', CardType.SUSPECT, 'susp')
sugg = Suggestion(room, weapon, susp)

def test_serialization():
    payload = sugg.serialize()
    assert type(payload) is str
    sugg2 = Suggestion.deserialize(payload)
    assert type(sugg2) is Suggestion
    payload2 = sugg2.serialize()
    assert payload == payload2

def test_to_string():
    assert str(sugg) == 'susp, with the weapon, in the room'
