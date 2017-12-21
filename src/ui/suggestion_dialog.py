"""suggestion_dialog.py."""

from src.ui.dialog import Dialog
from src.ui.picker import Picker
from src.card import Card
from src.cardtype import CardType
from src.suggestion import Suggestion
import pygame
import os
import json

class SuggestionDialog(Dialog):
    def __init__(self, x, y):
        super(SuggestionDialog, self).__init__(x, y)
        # Initialize pickers
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../../data/cards.json')

        with open(filename) as data_file:
            card_data = json.load(data_file)

        # Build separate card decks
        self._characters = []
        self._weapons = []
        self._rooms = []

        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card = Card(c['card_id'], CardType.SUSPECT)
                self._characters.append(card)
            elif c['type'] == 'weapon':
                card = Card(c['card_id'], CardType.WEAPON)
                self._weapons.append(card)
            else:
                card = Card(c['card_id'], CardType.ROOM)
                self._rooms.append(card)

        # Build pickers
        self._character_picker = Picker(self._characters, 110 + self._coords[0], 45 + self._coords[1])
        self._room_picker = Picker(self._rooms, 350 + self._coords[0], 45 + self._coords[1])
        self._weapon_picker = Picker(self._weapons, 590 + self._coords[0], 45 + self._coords[1])
        # Add pickers to view
        self.add_view(self._character_picker)
        self.add_view(self._room_picker)
        self.add_view(self._weapon_picker)


        def cancel(args):
            sugg_dialog = args['d']
            sugg_dialog.set_is_visible(False)

        # self._top_button.set_on_click(confirm, {'d': self })

        self._bottom_button.set_on_click(cancel, {'d': self })

        # set background image
        self._background_image = pygame.image.load('resources/suggestionselect.jpg')


    # Override draw method to include background image
    def draw(self, event, display):
        if (self._is_visible):
            display.blit(self._background_image, (self._coords[0], self._coords[1]))
        super(SuggestionDialog, self).draw(event, display)

    def set_is_visible(self, is_visible):
        # If this is being set as visible, clear all selections
        if is_visible:
            self._character_picker.deselect_all_except(-1)
            self._room_picker.deselect_all_except(-1)
            self._weapon_picker.deselect_all_except(-1)
        super(SuggestionDialog, self).set_is_visible(is_visible)

    def get_suggestion(self):
        room = self._room_picker.get_selected()
        weapon = self._weapon_picker.get_selected()
        character = self._character_picker.get_selected()

        if room and character and weapon:
            return Suggestion(room, weapon, character)
        else:
            return None

    def set_room_id(self, room_card_id):
        self._room_picker.enable_all()
        for i, c in enumerate(self._rooms):
            if c.get_id() != room_card_id:
                self._room_picker.disable_button(i)
