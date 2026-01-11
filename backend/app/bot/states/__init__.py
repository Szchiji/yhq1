"""
对话状态定义
"""
from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    """表单填写状态"""
    selecting_menu = State()  # 选择菜单
    answering = State()  # 回答问题
    confirming = State()  # 确认提交
