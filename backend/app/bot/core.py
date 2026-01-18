"""
Telegram Bot 核心对象
用于集中管理 bot 和 dispatcher 的初始化，避免循环依赖
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from ..config import settings

# 初始化 Bot
bot = Bot(token=settings.BOT_TOKEN)

# 初始化 Dispatcher
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
