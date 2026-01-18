"""
消息发送工具模块
"""
from typing import Optional
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from ...config import settings


async def send_to_admin(bot: Bot, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
    """发送消息给管理员"""
    
    admin_ids = settings.ADMIN_CHAT_IDS.split(",")
    for admin_id in admin_ids:
        if admin_id.strip():
            try:
                await bot.send_message(
                    int(admin_id.strip()), 
                    text, 
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"发送给管理员 {admin_id} 失败: {e}")
