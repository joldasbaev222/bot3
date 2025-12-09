import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime

TOKEN = "8464056216:AAEwm5q5QGcQoiOsfE62qFUkP7NiSZbgaJk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

scheduler = AsyncIOScheduler()

@dp.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer(
        "⏰ Esletpe bot!\n"
        "Misal: /remind 18:30 suw ishiw "
    )

@dp.message(Command("remind"))
async def reminder_cmd(msg: types.Message):
    try:
        data = msg.text.split(maxsplit=2)
        if len(data) < 3:
            return await msg.answer("Format: /remind 18:30 tekst.")

        time_str = data[1]
        text = data[2]

        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        remind_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if remind_time < now:
            remind_time = remind_time.replace(day=now.day + 1)

        scheduler.add_job(
            send_reminder,
            trigger=DateTrigger(run_date=remind_time),
            args=[msg.chat.id, text]
        )

        await msg.answer(f"Esletpe saqlandi: {time_str}")

    except Exception as e:
        await msg.answer(f"Qatelik: {e}")

async def send_reminder(chat_id: int, text: str):
    await bot.send_message(chat_id, f"Esletpe:\n{text}")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print("I'm starting...")

