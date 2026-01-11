#!/bin/bash

# 快速部署脚本

echo "================================"
echo "Telegram 审核机器人 - 快速部署"
echo "================================"

# 检查是否存在 .env 文件
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件，从 .env.example 复制..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑它并填入正确的配置"
    exit 1
fi

echo "📦 启动 Docker 容器..."
docker-compose up -d

echo ""
echo "✅ 部署完成！"
echo ""
echo "访问地址:"
echo "  - 前端: http://localhost"
echo "  - 后端 API: http://localhost:8000"
echo "  - API 文档: http://localhost:8000/docs"
echo ""
echo "默认管理员账号:"
echo "  - 用户名: admin"
echo "  - 密码: admin123"
echo ""
echo "⚠️  请尽快修改默认密码！"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
