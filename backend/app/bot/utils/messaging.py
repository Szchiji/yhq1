"""
消息发送工具模块
"""
from aiogram import Bot


async def send_to_admin(bot: Bot, text: str):
    """发送消息给管理员"""
    from ...config import settings
    
    admin_ids = settings.ADMIN_CHAT_IDS.split(",")
    for admin_id in admin_ids:
        if admin_id.strip():
            try:
                await bot.send_message(int(admin_id.strip()), text)
            except Exception as e:
                print(f"发送给管理员 {admin_id} 失败: {e}")
