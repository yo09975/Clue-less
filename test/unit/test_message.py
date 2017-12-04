from src.network.message import Message, MessageType
from uuid import uuid4

test_uuid = uuid4()
test_payload = 'test payload'
test_message_movement = Message(test_uuid, MessageType.MOVEMENT, test_payload)
test_message_suggestion = Message(test_uuid, MessageType.SUGGESTION, test_payload)
test_message_suggestion_response = Message(test_uuid, MessageType.SUGGESTION_RESP, test_payload)
test_message_accusation = Message(test_uuid, MessageType.ACCUSATION, test_payload)

def test_init():
	assert type(test_message_movement) is Message

def test_get_uuid():
	assert test_message_movement.get_uuid() == test_uuid
	assert test_message_suggestion.get_uuid() == test_uuid
	assert test_message_suggestion_response.get_uuid() == test_uuid
	assert test_message_accusation.get_uuid() == test_uuid

def test_get_msg_type():
	assert test_message_movement.get_msg_type() == MessageType.MOVEMENT
	assert test_message_suggestion.get_msg_type() == MessageType.SUGGESTION
	assert test_message_suggestion_response.get_msg_type() == MessageType.SUGGESTION_RESP
	assert test_message_accusation.get_msg_type() == MessageType.ACCUSATION

def test_get_payload():
	assert test_message_movement.get_payload() == test_payload
	assert test_message_suggestion.get_payload() == test_payload
	assert test_message_suggestion_response.get_payload() == test_payload
	assert test_message_accusation.get_payload() == test_payload