"""
键盘生成工具
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def create_main_menu_keyboard(menus: List[dict], buttons_per_row: int = 2) -> ReplyKeyboardMarkup:
    """创建主菜单键盘"""
    keyboard = []
    row = []
    
    for menu in menus:
        icon = menu.get("icon", "")
        name = menu.get("name", "")
        button_text = f"{icon} {name}" if icon else name
        
        row.append(KeyboardButton(text=button_text))
        
        if len(row) >= buttons_per_row:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def create_options_keyboard(options: List[str], multiple: bool = False) -> ReplyKeyboardMarkup:
    """创建选项键盘"""
    keyboard = []
    
    for option in options:
        keyboard.append([KeyboardButton(text=option)])
    
    if multiple:
        keyboard.append([KeyboardButton(text="✅ 完成选择")])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def create_confirm_keyboard() -> ReplyKeyboardMarkup:
    """创建确认键盘"""
    keyboard = [
        [KeyboardButton(text="✅ 确认提交"), KeyboardButton(text="❌ 取消")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def create_admin_inline_keyboard(submission_id: int) -> InlineKeyboardMarkup:
    """创建管理员审核内联键盘"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ 通过", callback_data=f"approve:{submission_id}"),
            InlineKeyboardButton(text="❌ 拒绝", callback_data=f"reject:{submission_id}")
        ],
        [
            InlineKeyboardButton(text="💬 回复", callback_data=f"reply:{submission_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
