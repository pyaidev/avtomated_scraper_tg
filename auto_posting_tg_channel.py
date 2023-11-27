from telethon.sync import TelegramClient
import time

api_id = '' # Вставьте свой api_id
api_hash = ''  # Вставьте свой api_hash
name = 'session'
phone_number = '+' # Вставьте свой номер телефона
channel_username = ''  # Вставьте свой канал (без @)

message_interval_list = ["HELLO", "HI", "HOW ARE YOU", "I AM FINE", "OKAY", "BYE"] # Список сообщений, которые будут отправляться в канал

# Create a Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))

    prev_message = None

    try:
        while True:
            print("Started!")
            for i in message_interval_list:
                if prev_message:
                    await client.delete_messages(channel_username, prev_message)

                # Send new message
                sent_message = await client.send_message(channel_username, i)
                prev_message = sent_message.id

                time.sleep(300)

    except KeyboardInterrupt:
        print("Stopped!")
with client:
    client.loop.run_until_complete(main())
