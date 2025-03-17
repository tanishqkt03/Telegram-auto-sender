from telethon.sync import TelegramClient

# Replace with your Telegram API credentials
API_ID = 0  # Your API ID
API_HASH = ""  # Your API Hash

# Start the Telethon client
client = TelegramClient("session_name", API_ID, API_HASH)

async def get_chat_ids():
    async with client:
        dialogs = await client.get_dialogs()  # Get recent chats
        for chat in dialogs:
            print(f"Chat Name: {chat.name} | Chat ID: {chat.id}")

with client:
    client.loop.run_until_complete(get_chat_ids())
