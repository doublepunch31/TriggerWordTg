import asyncio
from telethon import TelegramClient, functions
from config import API_ID, API_HASH, PHONE_NUMBER

async def list_chats(client):
    """List all groups and channels"""
    print("\n" + "="*80)
    print(f"{'Chat ID':<20} {'Type':<12} {'Forum?':<8} {'Name'}")
    print("="*80)
    
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        
        if hasattr(entity, 'broadcast'):
            chat_type = "channel" if entity.broadcast else "supergroup"
            is_forum = getattr(entity, 'forum', False)
        elif entity.__class__.__name__ == "Chat":
            chat_type = "group"
            is_forum = False
        else:
            continue
        
        chat_id = dialog.id
        print(f"{chat_id:<20} {chat_type:<12} {str(is_forum):<8} {dialog.name}")
    print()

async def list_topics(client, chat_id):
    """List all topics in a forum chat"""
    try:
        entity = await client.get_entity(chat_id)
        
        if not getattr(entity, 'forum', False):
            print("This chat doesn't have topics enabled.")
            return
        
        result = await client(functions.channels.GetForumTopicsRequest(
            channel=entity, offset_date=None, offset_id=0, offset_topic=0, limit=100
        ))
        
        topics = result.topics
        if not topics:
            print("No topics found.")
            return
        
        print("\n" + "="*60)
        print(f"{'Topic ID':<15} {'Title'}")
        print("="*60)
        for topic in topics:
            print(f"{topic.id:<15} {topic.title}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")

async def main():
    client = TelegramClient("user_session", API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    
    while True:
        print("\n1 - List all chats")
        print("2 - List topics in a chat")
        print("0 - Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            await list_chats(client)
        elif choice == "2":
            chat_id = input("Enter chat ID: ").strip()
            try:
                chat_id = int(chat_id)
                await list_topics(client, chat_id)
            except ValueError:
                print("Invalid chat ID")
        elif choice == "0":
            break
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())