# Telegram Message Forwarder

Auto-forwards messages containing trigger words from specific Telegram chats to another chat.

## Setup

1. Install dependencies:
```bash
pip install telethon python-dotenv
```

2. Create `.env` file with your credentials:
```properties
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+1234567890
FORWARD_TO=@yourusername
```

Get API credentials from: https://my.telegram.org/apps

3. Find chat IDs to monitor:
```bash
python discover.py
```

4. Edit `config.py` and add your target chats:
```python
TARGETS = [
    {'chat': -1003171709111, 'topics': [2]},  # with topics
    -1001234567890,  # whole chat
]
```

## Usage

Run the forwarder:
```bash
python main.py
```

Stop with `Ctrl+C`

## Config

- **TRIGGER_WORDS**: Words to look for (case-insensitive)
- **FORWARD_TO**: Where to send messages (`me`, `@username`, or chat ID)
- **TARGETS**: Chats to monitor (with optional topic filters)
