import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime
import pytz
import random

# 🔧 Настройки — вставь свои значения:
TOKEN = "8165898178:AAGGsk04KffMBLHArniF99ihcdz_kjUvJ_Y"   # токен от BotFather
CHAT_ID = 1898681878        # ID Наси
OWNER_ID = 8033093305       # твой ID

# ✅ Фразы похвалы
praise_phrases = [
    "Умничка, Нася 🌸",
    "Горжусь тобой, Нася ❤️",
    "Ты просто супер! 💊",
    "Так держать, Нася ☀️",
    "Моя лучшая девочка! 💖",
    "Ты не забыла! Молодец, Нася 😍",
]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_clicked = False

# 💬 Проверка, что бот отвечает и видит сообщения
@dp.message_handler()
async def echo_message(message: types.Message):
    print(f"Получено сообщение от {message.from_user.id}: {message.text}")
    await message.answer("Бот на связи! ✅")

# 🔔 Ежедневное напоминание
async def send_reminder():
    global user_clicked
    while True:
        now = datetime.now(pytz.timezone("Asia/Almaty"))
        if now.hour == 23 and now.minute == 0:
            user_clicked = False
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ Выпила", callback_data="taken"))
            await bot.send_message(CHAT_ID, "Нася, время выпить таблетку 💊", reply_markup=markup)

            # ждём 5 минут
            await asyncio.sleep(300)
            if not user_clicked:
                await bot.send_message(CHAT_ID, "⚠️ СРОЧНО ВЫПЕЙ ТАБЛЕТКУ, БОГДАШКА РУГАЕТ 💢")
                await bot.send_message(OWNER_ID, "❗ Нася не нажала на кнопку! Напомни ей!")
        await asyncio.sleep(60)

# 🩵 Обработка нажатия кнопки "Выпила"
@dp.callback_query_handler(lambda c: c.data == "taken")
async def process_callback(callback_query: types.CallbackQuery):
    global user_clicked
    user_clicked = True
    phrase = random.choice(praise_phrases)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, phrase)

# 🚀 При старте запускаем задачу-напоминалку
async def on_startup(_):
    asyncio.create_task(send_reminder())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
