import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

# Forward destination: 'me', @username, or chat ID (e.g., -1001234567890)
FORWARD_TO = os.getenv('FORWARD_TO', 'me')

# Trigger words (case-insensitive)
TRIGGER_WORDS = ['fridge', 'refrigerator', 'cooler', 'freezer']

# Chats to monitor: [chat_id, chat_id, ...] or [{'chat': chat_id, 'topics': [1, 2]}, ...]
TARGETS = [
    {'chat': -1003171709111, 'topics': [2]},
    {'chat': -1001137447265, 'topics': [44900]},
    {'chat': -1001519427119, 'topics': [1]},
]