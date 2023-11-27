from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

API_TOKEN = 'your_token'
api_id = 'your_id'
api_hash = 'your_hash'
name = 'session'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот, который проверяет существует ли канал или Бан в телеграмме.\nПросто отправь ссылку на канал и я проверю его на существование.\nПример: https://t.me/channelname")

@dp.message_handler(Text(contains='https://t.me/'))
async def send_media(message: types.Message):
    link = message.text
    text = link.replace("https://t.me/", "")

    async with TelegramClient(name, api_id, api_hash) as client:  # Use async with here
        results = await client(functions.contacts.SearchRequest(
            q=text,
            limit=1
        ))

        if results.chats:
            await message.answer('Канал существует')
        else:
            try:
                req = await client(functions.contacts.ResolveUsernameRequest(username=text))
                await message.answer(f"Бан")
            except UsernameNotOccupiedError:
                await message.answer(f"Не существует")

@dp.message_handler()
async def handle_non_url_messages(message: types.Message):
    await message.answer("Я не понимаю, что ты написал. Пожалуйста, отправь ссылку на канал в формате https://t.me/channelname")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
