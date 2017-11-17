"""test_cardtype.py"""
from src.cardtype import CardType


def test_enums():
    assert CardType.SUSPECT.value == 1
    assert CardType.ROOM.value == 2
    assert CardType.WEAPON.value == 3
