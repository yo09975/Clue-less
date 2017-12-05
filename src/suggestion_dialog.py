"""suggestion_dialog.py."""

from src.dialog import Dialog
from src.picker import Picker
from src.card import Card
from src.cardtype import CardType
import pygame
import os
import json

class SuggestionDialog(Dialog):
    def __init__(self, x, y):
        super(SuggestionDialog, self).__init__(x, y)
        # Initialize pickers
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/cards.json')

        with open(filename) as data_file:
            card_data = json.load(data_file)

        # Build separate card decks
        characters = []
        weapons = []
        rooms = []

        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card = Card(c['name'], CardType.SUSPECT, c['key'])
                characters.append(card)
            elif c['type'] == 'weapon':
                card = Card(c['name'], CardType.WEAPON, c['key'])
                weapons.append(card)
            else:
                card = Card(c['name'], CardType.ROOM, c['key'])
                rooms.append(card)

        # Build pickers
        self._character_picker = Picker(characters, 110 + self._coords[0], 45 + self._coords[1])
        self._room_picker = Picker(rooms, 350 + self._coords[0], 45 + self._coords[1])
        self._weapon_picker = Picker(weapons, 590 + self._coords[0], 45 + self._coords[1])
        # Add pickers to view
        self.add_view(self._character_picker)
        self.add_view(self._room_picker)
        self.add_view(self._weapon_picker)

        # Set up button logic
        def confirm(args):
            room = args['r'].get_selected()
            character = args['c'].get_selected()
            weapon = args['w'].get_selected()
            sugg_dialog = args['d']

            if room and character and weapon:
                print(room, character, weapon)
                sugg_dialog.set_is_visible(False)
                # TODO Send off suggestion message
        def cancel(args):
            sugg_dialog = args['d']
            sugg_dialog.set_is_visible(False)

        self._top_button.set_on_click(confirm, {'r': self._room_picker, \
            'c': self._character_picker, \
            'w': self._weapon_picker, \
            'd': self })


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
