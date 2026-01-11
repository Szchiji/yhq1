"""
仪表盘 API 路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from ..database import get_db
from ..models.user import User, Admin
from ..models.submission import Submission, SubmissionStatus
from ..auth import get_current_active_admin

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_active_admin)
):
    """获取仪表盘统计数据"""
    today = datetime.utcnow().date()
    
    # 总用户数
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar()
    
    # 今日新增用户
    today_users_result = await db.execute(
        select(func.count(User.id)).where(
            func.date(User.created_at) == today
        )
    )
    today_users = today_users_result.scalar()
    
    # 总提交数
    total_submissions_result = await db.execute(select(func.count(Submission.id)))
    total_submissions = total_submissions_result.scalar()
    
    # 今日提交数
    today_submissions_result = await db.execute(
        select(func.count(Submission.id)).where(
            func.date(Submission.created_at) == today
        )
    )
    today_submissions = today_submissions_result.scalar()
    
    # 待审核数
    pending_result = await db.execute(
        select(func.count(Submission.id)).where(
            Submission.status == SubmissionStatus.PENDING
        )
    )
    pending_submissions = pending_result.scalar()
    
    # 最近7天的提交趋势
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    trend_result = await db.execute(
        select(
            func.date(Submission.created_at).label("date"),
            func.count(Submission.id).label("count")
        ).where(
            Submission.created_at >= seven_days_ago
        ).group_by(
            func.date(Submission.created_at)
        ).order_by(
            func.date(Submission.created_at)
        )
    )
    trend_data = [{"date": str(row.date), "count": row.count} for row in trend_result]
    
    return {
        "total_users": total_users,
        "today_users": today_users,
        "total_submissions": total_submissions,
        "today_submissions": today_submissions,
        "pending_submissions": pending_submissions,
        "trend_data": trend_data
    }
