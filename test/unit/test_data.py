"""test_data.py.

Perform a sanity check on data resource files. Ensures that keys in one files
correspond to keys in other files when necessary.
"""
import os
import json

dir = os.path.dirname(__file__)

# Get card info in dictionary
filename = os.path.join(dir, '../../data/cards.json')

with open(filename) as data_file:
    card_data = json.load(data_file)

# Get location info in dictionary
filename = os.path.join(dir, '../../data/locations.json')
with open(filename) as data_file:
    location_data = json.load(data_file)


def test_verify_card_room_keys():
    """Ensure every room card has a key that matches key in locations.json."""
    # Iterate through all cards
    for c in card_data['cards']:
        if c['type'] == 'room':
            # If room card, check for corresponding location
            found_key = False
            for l in location_data['locations']:
                found_key = found_key or c['card_id'] == l['name']
            assert found_key


def test_verify_room_names():
    """Ensure every room has a name matching a card key."""
    # Iterate through all rooms
    for l in location_data['locations']:
        if l['type'] == 'room':
            # If room, check for corresponding card
            found_key = False
            for c in card_data['cards']:
                found_key = found_key or l['name'] == c['card_id']
            assert found_key


def test_verify_start_locations():
    """Make sure start locations add up.

    Check to make sure all suspect card start locations are actual locations
    and are marked as start locations in locations.json.
    """
    # Iterate through all cards
    for c in card_data['cards']:
        if c['type'] == 'suspect':
            # Make sure start location exists
            found_loc = False
            for l in location_data['locations']:
                print(c['start'], l)
                found_loc = found_loc or l['key'] == c['start']
                if l['key'] == c['start']:
                    print("hey")
                    assert l.get('init', False)

            if not found_loc:
                print(c['card_id'], found_loc)

            assert found_loc
