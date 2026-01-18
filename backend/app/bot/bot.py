"""
Telegram Bot 主程序
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .handlers import start, menu, submission, admin
from ..config import settings

# 初始化 Bot
bot = Bot(token=settings.BOT_TOKEN)

# 初始化 Dispatcher
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def setup_handlers():
    """注册所有处理器"""
    # 注册开始命令处理器
    dp.include_router(start.router)
    
    # 注册菜单处理器
    dp.include_router(menu.router)
    
    # 注册提交处理器
    dp.include_router(submission.router)
    
    # 注册管理员处理器
    dp.include_router(admin.router)


# 设置处理器
setup_handlers()
