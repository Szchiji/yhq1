# Telegram 审核机器人系统

企业级 Telegram 审核机器人系统，包含机器人端和网页管理后台。

## 功能特性

### 🤖 Telegram Bot 端
- ✅ 自定义欢迎消息和菜单
- ✅ 对话式交互流程
- ✅ 支持多种问题类型（文本、单选、多选、图片、文件）
- ✅ 实时审核通知
- ✅ 内联按钮快速处理

### 💻 Web 管理后台
- ✅ 数据统计仪表盘
- ✅ 菜单管理
- ✅ 流程管理
- ✅ 消息模板管理
- ✅ 审核管理
- ✅ 用户管理
- ✅ 系统设置

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus + Pinia
- **后端**: Python FastAPI + aiogram 3.x
- **数据库**: PostgreSQL
- **缓存**: Redis
- **部署**: Docker + Railway

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 本地开发

#### 1. 克隆仓库

```bash
git clone <repository-url>
cd yhq1
```

#### 2. 配置环境变量

创建 `.env` 文件：

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
ADMIN_CHAT_IDS=123456789,987654321

# 数据库
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telegram_bot

# Redis
REDIS_URL=redis://localhost:6379/0

# 认证
SECRET_KEY=your-secret-key-change-this-to-random-string
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# CORS
CORS_ORIGINS=http://localhost:3000
```

#### 3. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端将在 http://localhost:8000 运行

#### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:3000 运行

### Docker 部署

使用 Docker Compose 一键启动所有服务：

```bash
# 设置环境变量
export BOT_TOKEN=your_bot_token
export ADMIN_CHAT_IDS=your_admin_telegram_id

# 启动服务
docker-compose up -d
```

访问:
- 前端: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## Railway 部署

### 一键部署到 Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### 手动部署步骤

1. **创建 Railway 项目**
   - 访问 [Railway.app](https://railway.app)
   - 创建新项目
   - 从 GitHub 导入仓库

2. **添加服务**
   - 添加 PostgreSQL 数据库
   - 添加 Redis
   - 添加本项目（后端）

3. **配置环境变量**

   必需的环境变量：
   ```
   BOT_TOKEN=你的Telegram_Bot_Token
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   SECRET_KEY=生成一个随机密钥
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=你的管理员密码
   ADMIN_CHAT_IDS=你的Telegram用户ID
   ```

4. **部署**
   - Railway 会自动检测 Dockerfile 并部署
   - 等待部署完成
   - 获取公网域名

5. **配置 Webhook**
   
   部署完成后，Telegram Bot 会自动设置 Webhook。

## 配置说明

### Telegram Bot Token

1. 与 [@BotFather](https://t.me/botfather) 对话
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称和用户名
4. 获取 Bot Token

### 获取 Telegram 用户 ID

1. 与 [@userinfobot](https://t.me/userinfobot) 对话
2. 发送任意消息
3. 获取你的用户 ID

### 管理员账号

默认管理员账号：
- 用户名: `admin`
- 密码: `admin123`

⚠️ **重要**: 首次登录后请立即修改默认密码！

## 使用指南

### 1. 登录管理后台

访问管理后台 URL，使用管理员账号登录。

### 2. 配置菜单

1. 进入「菜单管理」
2. 点击「新建菜单」
3. 设置菜单名称、图标、排序
4. 保存

### 3. 创建流程

1. 进入「流程管理」
2. 点击「新建流程」
3. 添加步骤：
   - 设置问题内容
   - 选择回答类型
   - 配置选项（如需要）
   - 设置是否必填
4. 保存流程
5. 在菜单管理中将菜单绑定到流程

### 4. 自定义消息模板

1. 进入「消息模板」
2. 编辑各类消息模板
3. 使用变量：
   - `{user_name}` - 用户名
   - `{report_id}` - 提交ID

### 5. 审核管理

1. 进入「审核管理」
2. 查看待审核列表
3. 点击「通过」或「拒绝」处理提交
4. 也可以直接在 Telegram 中点击内联按钮处理

## API 文档

部署后访问 `/docs` 查看完整的 API 文档。

示例: https://your-domain.railway.app/docs

## 项目结构

```
.
├── backend/                # 后端代码
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── bot/           # Telegram Bot
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── config.py      # 配置
│   │   ├── database.py    # 数据库
│   │   └── main.py        # 主应用
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── api/          # API 调用
│   │   ├── components/   # 组件
│   │   ├── router/       # 路由
│   │   ├── stores/       # 状态管理
│   │   ├── views/        # 页面
│   │   └── main.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── railway.toml
└── README.md
```

## 常见问题

### Q: Bot 没有响应？
A: 检查：
1. BOT_TOKEN 是否正确
2. Webhook 是否设置成功
3. 查看后端日志

### Q: 无法登录管理后台？
A: 检查：
1. 数据库是否正常运行
2. 默认管理员是否创建成功
3. 查看后端日志

### Q: 图片/文件上传失败？
A: 检查：
1. MAX_FILE_SIZE 配置
2. 存储空间是否充足
3. 文件权限设置

## 安全建议

1. ✅ 修改默认管理员密码
2. ✅ 使用强密码和随机 SECRET_KEY
3. ✅ 限制 CORS_ORIGINS 为特定域名
4. ✅ 定期备份数据库
5. ✅ 启用 HTTPS

## 许可证

MIT License

## 支持

如有问题或建议，请提交 Issue。

---

**Made with ❤️ for Telegram Bot Management**
