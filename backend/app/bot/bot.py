"""
Telegram Bot 主程序
"""
from .core import bot, dp
from .handlers import start, menu, submission, admin


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


# 导出核心对象和设置函数
__all__ = ['bot', 'dp', 'setup_handlers']
