"""
开始命令处理器
"""
from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select

from ...database import async_session_maker
from ...models.user import User, UserLanguage
from ...models.template import MessageTemplate, TemplateType
from ...models.menu import Menu
from ..keyboards import create_main_menu_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """处理 /start 命令"""
    async with async_session_maker() as session:
        # 检查用户是否存在
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        # 如果用户不存在，创建新用户
        if not user:
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language=UserLanguage.ZH_CN
            )
            session.add(user)
            await session.commit()
        
        # 检查用户是否被拉黑
        if user.is_blocked:
            await message.answer("❌ 您已被禁止使用本机器人")
            return
        
        # 获取欢迎消息模板
        template_result = await session.execute(
            select(MessageTemplate).where(
                MessageTemplate.template_type == TemplateType.WELCOME
            )
        )
        template = template_result.scalar_one_or_none()
        
        welcome_text = template.content if template else "👋 欢迎使用 Telegram 审核机器人！"
        
        # 替换变量
        welcome_text = welcome_text.replace("{user_name}", user.first_name or "用户")
        
        # 获取活跃菜单
        menus_result = await session.execute(
            select(Menu).where(Menu.is_active == True).order_by(Menu.order)
        )
        menus = menus_result.scalars().all()
        
        if menus:
            # 创建菜单键盘
            menu_list = [
                {"icon": menu.icon, "name": menu.name}
                for menu in menus
            ]
            buttons_per_row = menus[0].buttons_per_row if menus else 2
            keyboard = create_main_menu_keyboard(menu_list, buttons_per_row)
            
            await message.answer(welcome_text, reply_markup=keyboard)
        else:
            await message.answer(welcome_text)
