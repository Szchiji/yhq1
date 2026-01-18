"""
提交处理器
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from datetime import datetime

from ...database import async_session_maker
from ...models.user import User
from ...models.submission import Submission, SubmissionAnswer, SubmissionStatus
from ...models.template import MessageTemplate, TemplateType
from ..states import FormStates
from ..keyboards import create_confirm_keyboard, create_options_keyboard, create_admin_inline_keyboard
from ..utils.messaging import send_to_admin

router = Router()


@router.message(FormStates.answering)
async def handle_answer(message: types.Message, state: FSMContext):
    """处理用户答案"""
    data = await state.get_data()
    current_step_index = data.get("current_step", 0)
    steps = data.get("steps", [])
    answers = data.get("answers", [])
    
    if current_step_index >= len(steps):
        return
    
    step_id, question, step_type, options, is_required = steps[current_step_index]
    
    # 处理不同类型的答案
    answer_text = ""
    file_id = None
    
    if step_type == "text":
        answer_text = message.text
    elif step_type == "single_choice":
        answer_text = message.text
        if options and answer_text not in options:
            await message.answer("❌ 请从提供的选项中选择")
            return
    elif step_type == "multiple_choice":
        if message.text == "✅ 完成选择":
            # 用户完成多选
            pass
        else:
            # 收集多选答案
            current_answers = data.get(f"multi_answer_{step_id}", [])
            if message.text in options:
                if message.text not in current_answers:
                    current_answers.append(message.text)
                await state.update_data({f"multi_answer_{step_id}": current_answers})
                await message.answer(f"已选择: {', '.join(current_answers)}\n继续选择或点击 '✅ 完成选择'")
                return
            else:
                await message.answer("❌ 请从提供的选项中选择")
                return
        answer_text = ", ".join(data.get(f"multi_answer_{step_id}", []))
    elif step_type == "image":
        if message.photo:
            file_id = message.photo[-1].file_id
            answer_text = "[图片]"
        else:
            await message.answer("❌ 请发送图片")
            return
    elif step_type == "file":
        if message.document:
            file_id = message.document.file_id
            answer_text = f"[文件: {message.document.file_name}]"
        else:
            await message.answer("❌ 请发送文件")
            return
    
    # 保存答案
    answers.append({
        "step_id": step_id,
        "question": question,
        "answer": answer_text,
        "file_id": file_id
    })
    
    # 移动到下一步
    current_step_index += 1
    
    if current_step_index < len(steps):
        # 还有更多问题
        await state.update_data(
            current_step=current_step_index,
            answers=answers
        )
        
        # 发送下一个问题
        step_id, question, step_type, options, is_required = steps[current_step_index]
        
        if step_type in ["single_choice", "multiple_choice"]:
            keyboard = create_options_keyboard(options, step_type == "multiple_choice")
            await message.answer(question, reply_markup=keyboard)
        else:
            await message.answer(question, reply_markup=types.ReplyKeyboardRemove())
    else:
        # 所有问题都回答完了，显示预览
        await state.update_data(answers=answers)
        
        # 生成预览文本
        preview_text = "📋 *请确认您的提交信息*\n\n"
        for answer in answers:
            preview_text += f"*{answer['question']}*\n{answer['answer']}\n\n"
        
        keyboard = create_confirm_keyboard()
        await message.answer(preview_text, reply_markup=keyboard, parse_mode="Markdown")
        await state.set_state(FormStates.confirming)


@router.message(FormStates.confirming)
async def handle_confirmation(message: types.Message, state: FSMContext):
    """处理确认"""
    if message.text == "✅ 确认提交":
        data = await state.get_data()
        
        async with async_session_maker() as session:
            # 获取用户
            user_result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = user_result.scalar_one()
            
            # 创建提交记录
            submission = Submission(
                user_id=user.id,
                flow_id=data["flow_id"],
                status=SubmissionStatus.PENDING
            )
            session.add(submission)
            await session.flush()
            
            # 保存答案
            for answer_data in data["answers"]:
                answer = SubmissionAnswer(
                    submission_id=submission.id,
                    step_id=answer_data["step_id"],
                    question=answer_data["question"],
                    answer=answer_data["answer"],
                    file_id=answer_data.get("file_id")
                )
                session.add(answer)
            
            await session.commit()
            
            # 获取提交成功模板
            template_result = await session.execute(
                select(MessageTemplate).where(
                    MessageTemplate.template_type == TemplateType.SUBMISSION_SUCCESS
                )
            )
            template = template_result.scalar_one_or_none()
            
            success_text = template.content if template else "✅ 提交成功！我们会尽快审核您的信息。"
            success_text = success_text.replace("{report_id}", str(submission.id))
            
            await message.answer(success_text, reply_markup=types.ReplyKeyboardRemove())
            
            # 发送给管理员
            admin_text = f"📨 *新的提交* (ID: {submission.id})\n\n"
            admin_text += f"👤 用户: {user.first_name or user.username}\n"
            admin_text += f"🆔 Telegram ID: {user.telegram_id}\n\n"
            
            for answer_data in data["answers"]:
                admin_text += f"*{answer_data['question']}*\n{answer_data['answer']}\n\n"
            
            keyboard = create_admin_inline_keyboard(submission.id)
            await send_to_admin(message.bot, admin_text)
        
        await state.clear()
    else:
        await message.answer("❌ 已取消提交", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
