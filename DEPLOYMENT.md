# 部署指南

## 目录

1. [本地开发部署](#本地开发部署)
2. [Docker 部署](#docker-部署)
3. [Railway 部署](#railway-部署)
4. [配置说明](#配置说明)
5. [故障排查](#故障排查)

---

## 本地开发部署

### 前置要求

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### 步骤 1: 克隆仓库

```bash
git clone <repository-url>
cd yhq1
```

### 步骤 2: 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的配置：

```env
# Telegram Bot Token (从 @BotFather 获取)
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# 管理员的 Telegram 用户 ID (从 @userinfobot 获取)
ADMIN_CHAT_IDS=123456789,987654321

# 数据库连接 (本地开发)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/telegram_bot

# Redis 连接
REDIS_URL=redis://localhost:6379/0

# JWT 密钥 (生成随机字符串)
SECRET_KEY=your-random-secret-key-min-32-characters

# 管理员账号
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# CORS 设置
CORS_ORIGINS=http://localhost:3000
```

### 步骤 3: 启动数据库

启动 PostgreSQL 和 Redis：

```bash
# 使用 Docker (推荐)
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

创建数据库：

```bash
docker exec -it postgres psql -U postgres -c "CREATE DATABASE telegram_bot;"
```

### 步骤 4: 启动后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 http://localhost:8000 运行

查看 API 文档: http://localhost:8000/docs

### 步骤 5: 启动前端

打开新终端：

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 http://localhost:3000 运行

### 步骤 6: 访问应用

- 前端: http://localhost:3000
- 后端: http://localhost:8000
- API 文档: http://localhost:8000/docs

默认管理员账号：
- 用户名: `admin`
- 密码: `admin123` (或您在 .env 中设置的密码)

---

## Docker 部署

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 快速启动

1. 复制并配置 `.env` 文件：

```bash
cp .env.example .env
# 编辑 .env 文件，至少需要设置 BOT_TOKEN
```

2. 启动所有服务：

```bash
docker-compose up -d
```

3. 查看日志：

```bash
docker-compose logs -f
```

4. 访问应用：

- 前端: http://localhost
- 后端: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 停止服务

```bash
docker-compose down
```

### 重启服务

```bash
docker-compose restart
```

### 查看运行状态

```bash
docker-compose ps
```

---

## Railway 部署

### 方法 1: 一键部署

点击下方按钮一键部署到 Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### 方法 2: 手动部署

#### 步骤 1: 创建 Railway 项目

1. 访问 [Railway.app](https://railway.app)
2. 注册/登录账号
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择您的仓库

#### 步骤 2: 添加数据库服务

1. 点击 "New" → "Database" → "Add PostgreSQL"
2. 点击 "New" → "Database" → "Add Redis"

#### 步骤 3: 配置环境变量

在后端服务中添加以下环境变量：

**必需变量:**

```
BOT_TOKEN=你的Telegram_Bot_Token
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=生成一个随机密钥
ADMIN_USERNAME=admin
ADMIN_PASSWORD=你的管理员密码
ADMIN_CHAT_IDS=你的Telegram用户ID
```

**可选变量:**

```
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.railway.app
MAX_FILE_SIZE=10485760
```

#### 步骤 4: 部署

Railway 会自动检测 Dockerfile 并开始部署。

等待部署完成（通常需要 3-5 分钟）。

#### 步骤 5: 获取域名

部署完成后：

1. 点击后端服务
2. 进入 "Settings" → "Networking"
3. 点击 "Generate Domain"
4. 记录生成的域名

#### 步骤 6: 配置 Webhook

Railway 会自动配置 Telegram Webhook。如果需要手动配置：

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_DOMAIN>/webhook/telegram"
```

#### 步骤 7: 部署前端（可选）

1. 在项目中添加新服务
2. 选择相同的 GitHub 仓库
3. 设置根目录为 `frontend`
4. Railway 会自动检测并部署

---

## 配置说明

### 获取 Telegram Bot Token

1. 在 Telegram 中搜索 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令
3. 按提示输入机器人名称和用户名
4. BotFather 会返回您的 Bot Token

示例:
```
Done! Congratulations on your new bot. You will find it at t.me/your_bot.
You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

### 获取 Telegram 用户 ID

1. 在 Telegram 中搜索 [@userinfobot](https://t.me/userinfobot)
2. 发送任意消息
3. 机器人会返回您的用户 ID

示例:
```
Your user ID is: 123456789
```

### 生成 SECRET_KEY

使用 Python 生成随机密钥：

```python
import secrets
print(secrets.token_urlsafe(32))
```

或使用 OpenSSL：

```bash
openssl rand -hex 32
```

### 环境变量说明

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| BOT_TOKEN | ✅ | Telegram Bot Token | `123456:ABC-DEF...` |
| ADMIN_CHAT_IDS | ✅ | 管理员 Telegram ID (逗号分隔) | `123456789,987654321` |
| DATABASE_URL | ✅ | PostgreSQL 连接字符串 | `postgresql+asyncpg://...` |
| REDIS_URL | ✅ | Redis 连接字符串 | `redis://localhost:6379/0` |
| SECRET_KEY | ✅ | JWT 密钥 | 随机字符串 (至少 32 字符) |
| ADMIN_USERNAME | ✅ | 管理员用户名 | `admin` |
| ADMIN_PASSWORD | ✅ | 管理员密码 | 强密码 |
| DEBUG | ❌ | 调试模式 | `False` (生产环境) |
| CORS_ORIGINS | ❌ | 允许的跨域来源 | `*` 或具体域名 |
| MAX_FILE_SIZE | ❌ | 最大文件大小 (字节) | `10485760` (10MB) |

---

## 故障排查

### 问题 1: Bot 没有响应

**症状**: 在 Telegram 中向 Bot 发送消息，但没有任何响应。

**可能原因**:

1. BOT_TOKEN 配置错误
2. Webhook 未正确设置
3. 后端服务未运行

**解决方案**:

```bash
# 检查 Bot Token 是否正确
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe

# 检查 Webhook 状态
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo

# 重新设置 Webhook
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_DOMAIN>/webhook/telegram"

# 检查后端日志
docker-compose logs -f backend
```

### 问题 2: 无法登录管理后台

**症状**: 输入正确的用户名和密码后仍然无法登录。

**可能原因**:

1. 数据库未正确初始化
2. 默认管理员账号未创建

**解决方案**:

```bash
# 查看后端日志
docker-compose logs backend

# 重启后端服务
docker-compose restart backend

# 检查数据库连接
docker-compose exec postgres psql -U postgres -d telegram_bot -c "SELECT * FROM admins;"
```

### 问题 3: 数据库连接失败

**症状**: 后端启动失败，日志显示数据库连接错误。

**可能原因**:

1. DATABASE_URL 配置错误
2. PostgreSQL 服务未启动
3. 数据库不存在

**解决方案**:

```bash
# 检查 PostgreSQL 服务
docker-compose ps postgres

# 重启 PostgreSQL
docker-compose restart postgres

# 手动创建数据库
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE telegram_bot;"

# 检查 DATABASE_URL 格式
# 正确格式: postgresql+asyncpg://用户名:密码@主机:端口/数据库名
```

### 问题 4: 前端无法连接后端

**症状**: 前端页面显示网络错误或无法加载数据。

**可能原因**:

1. 后端服务未启动
2. CORS 配置错误
3. API 地址配置错误

**解决方案**:

```bash
# 检查后端服务状态
docker-compose ps backend

# 检查 CORS 设置
# 在 .env 中设置: CORS_ORIGINS=http://localhost:3000

# 检查前端 API 配置
# 确保 frontend/src/api/request.js 中的 baseURL 正确

# 测试后端 API
curl http://localhost:8000/health
```

### 问题 5: 文件上传失败

**症状**: 在 Telegram 中上传图片或文件时失败。

**可能原因**:

1. 文件大小超过限制
2. 存储空间不足
3. 文件权限问题

**解决方案**:

```bash
# 调整文件大小限制
# 在 .env 中设置: MAX_FILE_SIZE=20971520  # 20MB

# 检查磁盘空间
df -h

# 检查上传目录权限
ls -la /tmp/uploads
```

### 问题 6: Railway 部署失败

**症状**: Railway 部署过程中出现错误。

**可能原因**:

1. 环境变量未正确配置
2. 构建超时
3. 依赖安装失败

**解决方案**:

1. 检查 Railway 构建日志
2. 确保所有必需的环境变量都已设置
3. 检查 requirements.txt 和 package.json 中的依赖版本
4. 尝试手动触发重新部署

### 获取帮助

如果以上方法都无法解决问题：

1. 查看完整的错误日志
2. 在 GitHub Issues 中搜索类似问题
3. 提交新的 Issue，包含：
   - 详细的错误描述
   - 相关日志
   - 系统环境信息
   - 已尝试的解决方法

---

## 安全建议

1. ✅ **修改默认密码**: 首次登录后立即修改 admin 密码
2. ✅ **使用强密码**: 管理员密码至少 12 字符，包含大小写字母、数字和特殊字符
3. ✅ **保护环境变量**: 不要将 .env 文件提交到 Git
4. ✅ **限制 CORS**: 在生产环境中将 CORS_ORIGINS 设置为特定域名
5. ✅ **定期备份**: 定期备份 PostgreSQL 数据库
6. ✅ **启用 HTTPS**: 在生产环境中始终使用 HTTPS
7. ✅ **监控日志**: 定期检查应用日志，发现异常行为

---

## 性能优化

### 数据库优化

```sql
-- 为常用查询添加索引
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_created_at ON submissions(created_at);
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
```

### Redis 缓存

考虑为以下数据添加缓存：
- 菜单列表
- 活跃流程
- 消息模板

### 文件存储

对于生产环境，建议使用对象存储服务（如 AWS S3、阿里云 OSS）存储用户上传的文件。

---

更多信息请参考主 README.md 文件。
