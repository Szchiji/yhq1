from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from database import db
from scheduler import schedule_task
import datetime

class Form(StatesGroup):
    waiting_for_content = State()
    waiting_for_media = State()
    waiting_for_buttons = State()
    waiting_for_interval = State()
    waiting_for_start_time = State()
    waiting_for_end_time = State()

async def cmd_start(message: types.Message):
    await message.answer("欢迎使用定时任务机器人！发送 /newtask 创建新任务，/tasks 查看任务。")

async def cmd_newtask(message: types.Message, state: FSMContext):
    await message.answer("请发送要定时发送的文字内容或上传图片/视频")
    await state.set_state(Form.waiting_for_content)

async def process_content(message: types.Message, state: FSMContext):
    data = {}
    if message.text:
        data["type"] = "text"
        data["content"] = message.text
        data["media_file_id"] = None
    elif message.photo:
        data["type"] = "photo"
        data["media_file_id"] = message.photo[-1].file_id
        data["content"] = message.caption or ""
    else:
        await message.answer("请发送文字或图片")
        return
    await state.update_data(task=data)
    await message.answer("是否需要添加按钮？发送按钮格式（按钮名1|url1;按钮名2|url2），发送“无”表示不添加按钮")
    await state.set_state(Form.waiting_for_buttons)

async def process_buttons(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task = data.get("task", {})
    if message.text.lower() == "无":
        task["buttons"] = None
    else:
        # 简单解析按钮
        buttons_raw = message.text.split(";")
        buttons = []
        for b in buttons_raw:
            parts = b.split("|")
            if len(parts) == 2:
                buttons.append({"text": parts[0], "url": parts[1]})
        task["buttons"] = json.dumps(buttons)
    await state.update_data(task=task)
    await message.answer("请输入定时发送间隔秒数（如 60 表示每60秒发送一次）")
    await state.set_state(Form.waiting_for_interval)

async def process_interval(message: types.Message, state: FSMContext):
    try:
        interval = int(message.text)
        if interval < 10:
            await message.answer("间隔太短，请输入 >=10 秒")
            return
    except:
        await message.answer("请输入有效数字")
        return
    data = await state.get_data()
    task = data.get("task", {})
    task["interval"] = interval
    await state.update_data(task=task)
    await message.answer("请输入定时任务开始时间（格式 2025-05-31 15:30），发送“现在”表示立即开始")
    await state.set_state(Form.waiting_for_start_time)

async def process_start_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task = data.get("task", {})
    if message.text.lower() == "现在":
        task["start_time"] = datetime.datetime.now().isoformat()
    else:
        try:
            dt = datetime.datetime.strptime(message.text, "%Y-%m-%d %H:%M")
            task["start_time"] = dt.isoformat()
        except:
            await message.answer("时间格式错误，请重新输入")
            return
    await state.update_data(task=task)
    await message.answer("请输入定时任务结束时间（格式 2025-05-31 17:30），发送“无”表示无限期")
    await state.set_state(Form.waiting_for_end_time)

async def process_end_time(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task = data.get("task", {})
    if message.text.lower() == "无":
        task["end_time"] = None
    else:
        try:
            dt = datetime.datetime.strptime(message.text, "%Y-%m-%d %H:%M")
            task["end_time"] = dt.isoformat()
        except:
            await message.answer("时间格式错误，请重新输入")
            return
    await state.update_data(task=task)
    # 保存任务
    await db.add_task(task)
    schedule_task(task)  # 立即调度
    await state.clear()
    await message.answer("任务创建成功！")

async def cmd_tasks(message: types.Message):
    rows = await db.get_tasks(message.chat.id)
    if not rows:
        await message.answer("没有找到定时任务。")
        return
    msg = "当前任务列表：\n"
    for r in rows:
        msg += f"ID: {r[0]}, 类型: {r[2]}, 间隔: {r[6]}秒\n"
    await message.answer(msg)

async def cmd_delete(message: types.Message):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("用法: /delete 任务ID")
        return
    task_id = int(parts[1])
    await db.delete_task(task_id)
    await message.answer(f"任务 {task_id} 已删除。")
