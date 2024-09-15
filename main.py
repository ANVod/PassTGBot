import os
import json
import random
import string
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.utils import run_polling
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher()

# Хранилище паролей
passwords = {}

# Генерация случайного пароля
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для генерации и хранения паролей.\n"
                        "Отправь команду /newpassword, чтобы сгенерировать новый пароль.")

@dp.message(Command('newpassword'))
async def new_password(message: types.Message):
    password = generate_password()
    await message.reply(f"Ваш новый пароль: <code>{password}</code>\n"
                        "Пожалуйста, укажите ресурс, для которого этот пароль предназначен, используя команду /save.")

@dp.message(Command('save'))
async def save_password(message: types.Message):
    args = message.get_args().split()
    if len(args) != 2:
        await message.reply("Пожалуйста, используйте формат: /save <ресурс> <пароль>")
        return

    resource, password = args
    passwords[resource] = password

    # Сохранение в файл
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)

    await message.reply(f"Пароль для ресурса {resource} сохранён.")

@dp.message(Command('getpassword'))
async def get_password(message: types.Message):
    resource = message.get_args()
    if resource in passwords:
        await message.reply(f"Пароль для ресурса {resource}: <code>{passwords[resource]}</code>")
    else:
        await message.reply(f"Пароль для ресурса {resource} не найден.")

if __name__ == '__main__':
    run_polling(dp, skip_updates=True)
