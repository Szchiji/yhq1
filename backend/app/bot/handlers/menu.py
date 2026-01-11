"""
菜单处理器
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ...database import async_session_maker
from ...models.menu import Menu
from ...models.flow import Flow
from ..states import FormStates
from ..keyboards import create_options_keyboard

router = Router()


@router.message(F.text)
async def handle_menu_selection(message: types.Message, state: FSMContext):
    """处理菜单选择"""
    async with async_session_maker() as session:
        # 提取按钮文本（去除图标）
        text = message.text
        # 移除可能的 emoji 图标
        text_parts = text.split(maxsplit=1)
        menu_name = text_parts[-1] if text_parts else text
        
        # 查找匹配的菜单
        result = await session.execute(
            select(Menu).where(
                Menu.name == menu_name,
                Menu.is_active == True
            )
        )
        menu = result.scalar_one_or_none()
        
        if not menu or not menu.flow_id:
            return
        
        # 获取关联的流程
        flow_result = await session.execute(
            select(Flow)
            .options(selectinload(Flow.steps))
            .where(Flow.id == menu.flow_id, Flow.is_active == True)
        )
        flow = flow_result.scalar_one_or_none()
        
        if not flow or not flow.steps:
            await message.answer("❌ 该功能暂未配置")
            return
        
        # 保存流程信息到状态
        await state.update_data(
            flow_id=flow.id,
            steps=[(step.id, step.question, step.step_type, step.options, step.is_required) 
                   for step in sorted(flow.steps, key=lambda x: x.order)],
            current_step=0,
            answers=[]
        )
        
        # 设置状态并开始第一个问题
        await state.set_state(FormStates.answering)
        
        # 发送第一个问题
        data = await state.get_data()
        step_id, question, step_type, options, is_required = data["steps"][0]
        
        # 根据步骤类型创建相应的键盘
        if step_type in ["single_choice", "multiple_choice"]:
            keyboard = create_options_keyboard(options, step_type == "multiple_choice")
            await message.answer(question, reply_markup=keyboard)
        else:
            await message.answer(question, reply_markup=types.ReplyKeyboardRemove())
