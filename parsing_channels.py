from telethon.sync import TelegramClient
import pandas as pd
import asyncio

async def main():
    name = ''
    api_id = ''
    api_hash = ""
    chat = ''
    data = []  # stores all our data in the format SENDER_ID, USERNAME, MESSAGE
    async with TelegramClient(name, api_id, api_hash) as client:
        async for message in client.iter_messages(chat):
            sender = await message.get_sender()
            if sender:
                username = sender.username
                username = username if username else ""  # Set to empty string if username is None
                print(sender)
                data.append([message.sender_id, username, message.text])

    df = pd.DataFrame(data, columns=['SENDER_ID', 'USERNAME', 'MESSAGE'])  # creates a new dataframe

    df.to_csv('filename.csv', encoding='utf-8', index=False)  # save to a CSV file

if __name__ == '__main__':
    asyncio.run(main())
