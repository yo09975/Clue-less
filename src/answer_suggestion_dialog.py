"""answer_suggestion_dialog.py."""

from src.dialog import Dialog
from src.picker import Picker
from src.card import Card
from src.cardtype import CardType
from src.message import Message
from src.message import MessageType

import pygame
import os
import json

class AnswerSuggestionDialog(Dialog):
    def __init__(self, x, y):
        super(AnswerSuggestionDialog, self).__init__(x, y)
        # Initialize pickers
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, '../data/cards.json')

        with open(filename) as data_file:
            card_data = json.load(data_file)

        # Build separate card decks
        self._characters = []
        self._weapons = []
        self._rooms = []

        for c in card_data['cards']:
            if c['type'] == 'suspect':
                card = Card(c['name'], CardType.SUSPECT, c['key'])
                self._characters.append(card)
            elif c['type'] == 'weapon':
                card = Card(c['name'], CardType.WEAPON, c['key'])
                self._weapons.append(card)
            else:
                card = Card(c['name'], CardType.ROOM, c['key'])
                self._rooms.append(card)

        def clear_other_pickers(args):
            other_picker_1 = args['o1']
            other_picker_1.deselect_all_except(-1)
            other_picker_2 = args['o2']
            other_picker_2.deselect_all_except(-1)

        # Build pickers
        self._character_picker = Picker(self._characters, 110 + self._coords[0], 45 + self._coords[1])
        self._room_picker = Picker(self._rooms, 350 + self._coords[0], 45 + self._coords[1])
        self._weapon_picker = Picker(self._weapons, 590 + self._coords[0], 45 + self._coords[1])

        self._character_picker.set_on_changed(clear_other_pickers, {'o1': self._room_picker, 'o2': self._weapon_picker})
        self._weapon_picker.set_on_changed(clear_other_pickers, {'o1': self._character_picker, 'o2': self._room_picker})
        self._room_picker.set_on_changed(clear_other_pickers, {'o1': self._character_picker, 'o2': self._weapon_picker})


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

            num_selected = 0
            if room:
                num_selected += 1
                chosen = self._suggestion.get_room()
            if character:
                num_selected += 1
                chosen = self._suggestion.get_character()
            if weapon:
                num_selected += 1
                chosen = self._suggestion.get_weapon()


            # Make sure only one card is selected
            if num_selected == 1:
                sugg_dialog.set_is_visible(False)
                sugg_dialog.set_success(True)
                # Send off suggestion answer
                cni = CNI()
                message = Message(cni.get_uuid(), MessageType.SUGGESTION_RESPONSE, chosen.serialize())
                cni.send_message(message)



        def cancel(args):
            sugg_dialog = args['d']
            sugg_dialog.set_is_visible(False)

        self._top_button.set_is_visible(False)
        self._bottom_button.set_on_click(confirm, {'r': self._room_picker, \
            'c': self._character_picker, \
            'w': self._weapon_picker, \
            'd': self })

        # set background image
        self._background_image = pygame.image.load('resources/suggestionanswer.jpg')


    # Override draw method to include background image
    def draw(self, event, display):
        if (self._is_visible):
            display.blit(self._background_image, (self._coords[0], self._coords[1]))
        super(AnswerSuggestionDialog, self).draw(event, display)

    def set_is_visible(self, is_visible):
        # If this is being set as visible, clear all selections
        if is_visible:
            self._character_picker.deselect_all_except(-1)
            self._character_picker.enable_all()
            self._room_picker.deselect_all_except(-1)
            self._room_picker.enable_all()
            self._weapon_picker.deselect_all_except(-1)
            self._weapon_picker.enable_all()
        super(AnswerSuggestionDialog, self).set_is_visible(is_visible)

    def set_player_hand(self, hand):

        for i, c in enumerate(self._rooms):
            found = False
            for h in hand.get_cards():
                if h.get_id() == c.get_id():
                    found = True
            if not found:
                self._room_picker.disable_button(i)

        for i, c in enumerate(self._characters):
            found = False
            for h in hand.get_cards():
                if h.get_id() == c.get_id():
                    found = True
            if not found:
                self._character_picker.disable_button(i)

        for i, c in enumerate(self._weapons):
            found = False
            for h in hand.get_cards():
                if h.get_id() == c.get_id():
                    found = True
            if not found:
                self._weapon_picker.disable_button(i)


    def set_suggestion(self, suggestion):
        self._suggestion = suggestion
        for i, c in enumerate(self._rooms):
            if suggestion.get_room().get_id() != c.get_id():
                self._room_picker.disable_button(i)
        for i, c in enumerate(self._characters):
            if suggestion.get_character().get_id() != c.get_id():
                self._character_picker.disable_button(i)
        for i, c in enumerate(self._weapons):
            if suggestion.get_weapon().get_id() != c.get_id():
                self._weapon_picker.disable_button(i)
