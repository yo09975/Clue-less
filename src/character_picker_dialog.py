"""suggestion_dialog.py."""

from src.dialog import Dialog
from src.card import Card
from src.cardtype import CardType
from src.character_picker import CharacterPicker
import pygame
import os
import json

class CharacterPickerDialog(Dialog):
    def __init__(self, x, y):
        super(CharacterPickerDialog, self).__init__(x, y)
        # Initialize pickers
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/cards.json')

        with open(filename) as data_file:
            card_data = json.load(data_file)

        # Build separate card decks
        characters = []

        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card = Card(c['name'], CardType.SUSPECT, c['key'])
                characters.append(card)

        # Build pickers
        self._character_picker = CharacterPicker(characters, 110 + self._coords[0], 50 + self._coords[1])

        self.add_view(self._character_picker)

        # Set up button logic
        def confirm(args):
            character = args['c'].get_selected()
            char_dialog = args['d']

            if character:
                print(character)
                char_dialog.set_is_visible(False)
                # TODO Send off suggestion message


        self._top_button.set_is_visible(False)
        self._bottom_button.set_on_click(confirm, {'c': self._character_picker, 'd': self })

        # set background image
        self._background_image = pygame.image.load('resources/characterselect.jpg')


    # Override draw method to include background image
    def draw(self, event, display):
        if (self._is_visible):
            display.blit(self._background_image, (self._coords[0], self._coords[1]))
        super(CharacterPickerDialog, self).draw(event, display)

    def set_is_visible(self, is_visible):
        # If this is being set as visible, clear all selections
        if is_visible:
            self._character_picker.deselect_all_except(-1)
        super(CharacterPickerDialog, self).set_is_visible(is_visible)
