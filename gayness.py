import asyncio
import random
import pickle
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, BotCommand, FSInputFile
from aiogram.filters import Command
import logging
import os
from dotenv import load_dotenv
from db import load_db

load_dotenv()
load_db()

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет!\nЯ брейнрот бот!\nСоболезную что вы решили написать мне, сегодня вы стали немного тупее чем раньше")


@dp.message(Command('help'))
async def send_help(message: types.Message):
    await message.answer("Пришли /rot чтобы получить брейнрот фразу или /pic чтобы посмотреть на итальянских животных "
                         "и уменьшить свой уровень умственного здоровья. Чтобы посмотреть свой прогресс используй "
                         "/stats\n\nМы следим за твоим IQ, брейнроты не"
                         "бесплатные, с каждой командой ты все больше походишь на овощ..... (/iq)")


@dp.message(Command('rot'))
async def send_rot(message: types.Message):
    add_user(message.from_user.id)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE users SET iq = iq-1 where id = ?", (message.from_user.id,))
        cursor.execute(f"UPDATE users SET rot_count = COALESCE(rot_count, 0) + 1 where id = ?", (message.from_user.id,))

        conn.commit()
        await message.answer(f"{get_random_verb()} {get_random_verb()}")
    finally:
        conn.close()


@dp.message(Command('pic'))
async def send_rot(message: types.Message):
    add_user(message.from_user.id)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE users SET iq = iq-5 where id = ?", (message.from_user.id,))
        cursor.execute(f"UPDATE users SET pic_count = COALESCE(pic_count, 0) + 1 where id = ?", (message.from_user.id,))
        conn.commit()
        await message.answer_photo(
            photo=FSInputFile(f'images/{random.choice(os.listdir("images"))}', filename='italian rot'))
    finally:
        conn.close()


@dp.message(Command('stats'))
async def send_stats(message: types.Message):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT iq, rot_count, pic_count FROM users where id = ?', (message.from_user.id,))
        result = cursor.fetchone()
        await message.answer(f'Посмотрим чего ты добился:\n\n🧠 - Твой IQ сейчас {result[0]}, ты уже отупел на {100 - result[0]}\n💬 - Прочитано {result[1]} брейнрот фраз\n🐊 - Просмотрено {result[2]} итальянских животных')
    except TypeError as e:
        await message.answer('Кажется ты еще не отупел, попробуй /pic или /rot')
    finally:
        conn.close()

@dp.message(Command('iq'))
async def check_iq(message: types.Message):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT iq FROM users where id = ?', (message.from_user.id,))
        result = cursor.fetchone()
        await message.answer(f'Твой IQ сейчас {result[0]}, ты уже отупел на {100 - result[0]}, за подробностями /stats')
    except TypeError as e:
        await message.answer('Кажется ты еще не отупел, попробуй /pic или /rot')
    finally:
        conn.close()


@dp.message(Command('iq_reset'))
async def check_iq(message: types.Message):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE users SET iq = 100 where id = ?", (message.from_user.id,))
        conn.commit()
        result = cursor.fetchone()
        await message.answer(f'Ну допустим ты пропил колесики, твой IQ восстановлен до 100')
        return result[0] if result else None
    finally:
        conn.close()


@dp.message()
async def non_command(message: types.Message):
    await message.answer('Ты че баклан дефективный? Это не команда, юзай /help')


async def main():
    print('bot started')

    await dp.start_polling(bot)


def get_random_verb():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT verb FROM verbs ORDER BY RANDOM() LIMIT 1')
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


def add_user(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO users (id, iq) VALUES (?, ?)', (user_id, 100,))
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())
