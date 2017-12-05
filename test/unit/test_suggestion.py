
from src.suggestion import Suggestion
from src.cardtype import CardType
from src.card import Card


def test_serialization():
    room = Card('room', CardType.ROOM, 'room')
    weapon = Card('weapon', CardType.WEAPON, 'weapon')
    susp = Card('susp', CardType.SUSPECT, 'susp')
    sugg = Suggestion(room, weapon, susp)
    payload = sugg.serialize()
    sugg2 = Suggestion.deserialize(payload)
    payload2 = sugg2.serialize()
    assert payload == payload2
