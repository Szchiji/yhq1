from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram import Bot
import json

scheduler = AsyncIOScheduler()
bot: Bot = None  # 下面会注入

async def send_scheduled_message(task):
    chat_id = task['chat_id']
    # 根据 type 发送不同消息
    if task['type'] == 'text':
        await bot.send_message(chat_id, task['content'])
    elif task['type'] == 'photo':
        await bot.send_photo(chat_id, task['media_file_id'], caption=task['content'])
    # 这里可扩展视频等其他类型
    # buttons 需要解析 JSON 生成 InlineKeyboardMarkup（略）

def schedule_task(task):
    # 从数据库取到的 task 是 tuple，转 dict 或自己定义模型
    # 这里只做简化演示
    interval = task[6]  # interval 秒数
    start_time = task[7]
    # 简化不考虑停止时间
    scheduler.add_job(send_scheduled_message, 'interval', seconds=interval, args=[{
        "chat_id": task[1],
        "type": task[2],
        "content": task[3],
        "media_file_id": task[4],
        "buttons": task[5],
        "interval": interval,
        "start_time": start_time,
        "end_time": task[8],
    }])

def start_scheduler():
    scheduler.start()
