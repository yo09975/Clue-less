"""test_playerstatus.py"""
from src.playerstatus import PlayerStatus


def test_enums():
    assert PlayerStatus.COMP.value == 1
    assert PlayerStatus.ACTIVE.value == 2
    assert PlayerStatus.LOST.value == 3
