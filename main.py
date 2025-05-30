import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, DOMAIN, WEBHOOK_PATH, WEBHOOK_URL
from database import db
from handlers import (
    cmd_start, cmd_newtask, process_content, process_buttons,
    process_interval, process_start_time, process_end_time,
    cmd_tasks, cmd_delete, Form
)
from scheduler import scheduler, start_scheduler, bot as scheduler_bot
from aiogram.fsm.context import FSMContext

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage, bot=bot)

scheduler_bot = bot  # 注入bot对象到 scheduler.py

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await db.connect()
    await bot.set_webhook(WEBHOOK_URL)
    start_scheduler()

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    await db.close()

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.process_update(update)
    return {"ok": True}

# 注册命令和消息处理
dp.message.register(cmd_start, commands=["start"])
dp.message.register(cmd_newtask, commands=["newtask"])
dp.message.register(cmd_tasks, commands=["tasks"])
dp.message.register(cmd_delete, commands=["delete"])

dp.message.register(process_content, Form.waiting_for_content)
dp.message.register(process_buttons, Form.waiting_for_buttons)
dp.message.register(process_interval, Form.waiting_for_interval)
dp.message.register(process_start_time, Form.waiting_for_start_time)
dp.message.register(process_end_time, Form.waiting_for_end_time)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
