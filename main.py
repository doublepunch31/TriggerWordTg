import asyncio
import logging
import re
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE_NUMBER, FORWARD_TO, TRIGGER_WORDS, TARGETS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def make_pattern(words):
    """Create regex pattern for trigger words"""
    if not words:
        return None
    pattern = r"\b(" + "|".join(re.escape(w) for w in words) + r")\b"
    return re.compile(pattern, re.IGNORECASE)

def get_topic_id(msg):
    """Extract topic ID from message"""
    if hasattr(msg, 'reply_to') and msg.reply_to:
        return msg.reply_to.reply_to_top_id or msg.reply_to.reply_to_msg_id
    return None

async def main():
    client = TelegramClient("user_session", API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    
    # Parse targets
    chats = []
    chat_topics = {}  # {chat_id: [topic_ids] or None}
    
    for target in TARGETS:
        if isinstance(target, dict):
            chat_id = target['chat']
            topics = target.get('topics')
            chats.append(chat_id)
            chat_topics[chat_id] = topics
        else:
            chats.append(target)
            chat_topics[target] = None
    
    trigger = make_pattern(TRIGGER_WORDS)
    
    @client.on(events.NewMessage(chats=chats))
    async def handler(event):
        msg = event.message
        chat_id = event.chat_id
        
        # Check topic filter
        allowed_topics = chat_topics.get(chat_id)
        if allowed_topics:
            topic_id = get_topic_id(msg)
            if topic_id not in allowed_topics:
                return
        
        # Check trigger words
        if trigger and not trigger.search(msg.text or ""):
            return
        
        # Forward message
        await client.forward_messages(FORWARD_TO, msg)
        logging.info(f"Forwarded message from chat {chat_id}")
    
    logging.info(f"Monitoring {len(chats)} chat(s) for: {TRIGGER_WORDS}")
    logging.info(f"Forwarding to: {FORWARD_TO}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopped")