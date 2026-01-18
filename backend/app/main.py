"""
FastAPI 主应用
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import Update

from .config import settings
from .database import init_db, async_session_maker
from .api import api_router
from .bot.core import bot, dp
from .bot.bot import setup_handlers  # Import handler setup function
from .models.user import Admin
from .models.template import MessageTemplate, TemplateType
from .auth import get_password_hash
from sqlalchemy import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 启动应用...")
    
    # 初始化数据库
    await init_db()
    print("✅ 数据库初始化完成")
    
    # 创建默认管理员账号
    async with async_session_maker() as session:
        result = await session.execute(
            select(Admin).where(Admin.username == settings.ADMIN_USERNAME)
        )
        admin = result.scalar_one_or_none()
        
        if not admin:
            admin = Admin(
                username=settings.ADMIN_USERNAME,
                password_hash=get_password_hash(settings.ADMIN_PASSWORD),
                role="super_admin"
            )
            session.add(admin)
            await session.commit()
            print(f"✅ 创建默认管理员: {settings.ADMIN_USERNAME}")
    
    # 创建默认消息模板
    async with async_session_maker() as session:
        templates = [
            {
                "name": "欢迎消息",
                "template_type": TemplateType.WELCOME,
                "content": "👋 你好 {user_name}！\n\n欢迎使用 Telegram 审核机器人系统。\n\n请从下方菜单选择您需要的功能。"
            },
            {
                "name": "提交成功",
                "template_type": TemplateType.SUBMISSION_SUCCESS,
                "content": "✅ 提交成功！\n\n您的提交ID: {report_id}\n\n我们会尽快审核您的信息，请耐心等待。"
            },
            {
                "name": "审核通过",
                "template_type": TemplateType.APPROVED,
                "content": "🎉 恭喜！您的提交(ID: {report_id})已通过审核！"
            },
            {
                "name": "审核拒绝",
                "template_type": TemplateType.REJECTED,
                "content": "❌ 抱歉，您的提交(ID: {report_id})未通过审核。\n\n如有疑问，请联系管理员。"
            }
        ]
        
        for template_data in templates:
            result = await session.execute(
                select(MessageTemplate).where(
                    MessageTemplate.template_type == template_data["template_type"]
                )
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                template = MessageTemplate(**template_data)
                session.add(template)
        
        await session.commit()
        print("✅ 创建默认消息模板")
    
    # 注册所有 Bot handlers
    setup_handlers()
    print("✅ 注册 Bot Handlers")
    
    # 设置 Webhook（在生产环境中）
    if not settings.DEBUG:
        webhook_url = f"{settings.CORS_ORIGINS}/webhook/telegram"
        await bot.set_webhook(webhook_url)
        print(f"✅ 设置 Webhook: {webhook_url}")
    else:
        await bot.delete_webhook()
        print("⚠️ 开发模式，未设置 Webhook")
    
    yield
    
    # 关闭时
    print("👋 关闭应用...")
    await bot.session.close()


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="企业版 Telegram 审核机器人系统",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Telegram Webhook 端点"""
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
