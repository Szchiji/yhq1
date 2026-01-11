"""
管理员处理器
"""
from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ...database import async_session_maker
from ...models.submission import Submission, SubmissionStatus
from ...models.user import User
from ...models.template import MessageTemplate, TemplateType
from ..bot import bot

router = Router()


@router.callback_query(F.data.startswith("approve:"))
async def handle_approve(callback: types.CallbackQuery):
    """处理审核通过"""
    submission_id = int(callback.data.split(":")[1])
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(Submission)
            .options(selectinload(Submission.answers))
            .where(Submission.id == submission_id)
        )
        submission = result.scalar_one_or_none()
        
        if not submission:
            await callback.answer("提交记录不存在")
            return
        
        if submission.status != SubmissionStatus.PENDING:
            await callback.answer("该提交已处理")
            return
        
        submission.status = SubmissionStatus.APPROVED
        await session.commit()
        
        # 获取用户
        user_result = await session.execute(
            select(User).where(User.id == submission.user_id)
        )
        user = user_result.scalar_one()
        
        # 获取通过消息模板
        template_result = await session.execute(
            select(MessageTemplate).where(
                MessageTemplate.template_type == TemplateType.APPROVED
            )
        )
        template = template_result.scalar_one_or_none()
        
        approved_text = template.content if template else "✅ 您的提交已通过审核！"
        approved_text = approved_text.replace("{report_id}", str(submission.id))
        
        # 通知用户
        try:
            await bot.send_message(user.telegram_id, approved_text)
        except Exception as e:
            print(f"发送给用户失败: {e}")
        
        await callback.message.edit_text(
            callback.message.text + "\n\n✅ *已通过*",
            parse_mode="Markdown"
        )
        await callback.answer("已通过审核")


@router.callback_query(F.data.startswith("reject:"))
async def handle_reject(callback: types.CallbackQuery):
    """处理审核拒绝"""
    submission_id = int(callback.data.split(":")[1])
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(Submission)
            .options(selectinload(Submission.answers))
            .where(Submission.id == submission_id)
        )
        submission = result.scalar_one_or_none()
        
        if not submission:
            await callback.answer("提交记录不存在")
            return
        
        if submission.status != SubmissionStatus.PENDING:
            await callback.answer("该提交已处理")
            return
        
        submission.status = SubmissionStatus.REJECTED
        await session.commit()
        
        # 获取用户
        user_result = await session.execute(
            select(User).where(User.id == submission.user_id)
        )
        user = user_result.scalar_one()
        
        # 获取拒绝消息模板
        template_result = await session.execute(
            select(MessageTemplate).where(
                MessageTemplate.template_type == TemplateType.REJECTED
            )
        )
        template = template_result.scalar_one_or_none()
        
        rejected_text = template.content if template else "❌ 抱歉，您的提交未通过审核。"
        rejected_text = rejected_text.replace("{report_id}", str(submission.id))
        
        # 通知用户
        try:
            await bot.send_message(user.telegram_id, rejected_text)
        except Exception as e:
            print(f"发送给用户失败: {e}")
        
        await callback.message.edit_text(
            callback.message.text + "\n\n❌ *已拒绝*",
            parse_mode="Markdown"
        )
        await callback.answer("已拒绝")
