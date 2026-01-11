# API 文档

## 基础信息

- **Base URL**: `/api`
- **认证方式**: JWT Bearer Token
- **Content-Type**: `application/json`

## 认证

### 登录

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded
```

**请求体**:
```
username=admin&password=admin123
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 获取当前用户信息

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "role": "super_admin",
  "is_active": true,
  "telegram_id": null,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

### 注册新管理员

```http
POST /api/auth/register
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "username": "newadmin",
  "password": "securepassword",
  "role": "moderator",
  "telegram_id": 123456789
}
```

**响应**: 返回新创建的管理员信息

---

## 仪表盘

### 获取统计数据

```http
GET /api/dashboard/stats
Authorization: Bearer <token>
```

**响应**:
```json
{
  "total_users": 150,
  "today_users": 12,
  "total_submissions": 500,
  "today_submissions": 23,
  "pending_submissions": 15,
  "trend_data": [
    {"date": "2024-01-01", "count": 20},
    {"date": "2024-01-02", "count": 25}
  ]
}
```

---

## 菜单管理

### 获取菜单列表

```http
GET /api/menus/?skip=0&limit=100
Authorization: Bearer <token>
```

**响应**:
```json
[
  {
    "id": 1,
    "name": "报告问题",
    "icon": "📝",
    "order": 0,
    "flow_id": 1,
    "is_active": true,
    "buttons_per_row": 2,
    "description": "报告问题或建议",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

### 创建菜单

```http
POST /api/menus/
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "name": "新菜单",
  "icon": "🎯",
  "order": 1,
  "flow_id": 2,
  "buttons_per_row": 2,
  "description": "菜单描述",
  "is_active": true
}
```

### 更新菜单

```http
PUT /api/menus/{menu_id}
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "name": "更新后的名称",
  "is_active": false
}
```

### 删除菜单

```http
DELETE /api/menus/{menu_id}
Authorization: Bearer <token>
```

---

## 流程管理

### 获取流程列表

```http
GET /api/flows/?skip=0&limit=100
Authorization: Bearer <token>
```

**响应**:
```json
[
  {
    "id": 1,
    "name": "问题报告流程",
    "description": "用户报告问题的流程",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null,
    "steps": [
      {
        "id": 1,
        "flow_id": 1,
        "order": 0,
        "question": "请描述您遇到的问题",
        "step_type": "text",
        "options": null,
        "is_required": true,
        "validation_rule": null,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
]
```

### 创建流程

```http
POST /api/flows/
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "name": "新流程",
  "description": "流程描述",
  "is_active": true,
  "steps": [
    {
      "order": 0,
      "question": "请选择问题类型",
      "step_type": "single_choice",
      "options": ["Bug", "功能建议", "其他"],
      "is_required": true
    },
    {
      "order": 1,
      "question": "请详细描述",
      "step_type": "text",
      "options": null,
      "is_required": true
    },
    {
      "order": 2,
      "question": "请上传截图（可选）",
      "step_type": "image",
      "options": null,
      "is_required": false
    }
  ]
}
```

### 更新流程

```http
PUT /api/flows/{flow_id}
Authorization: Bearer <token>
Content-Type: application/json
```

### 删除流程

```http
DELETE /api/flows/{flow_id}
Authorization: Bearer <token>
```

---

## 模板管理

### 获取模板列表

```http
GET /api/templates/
Authorization: Bearer <token>
```

**响应**:
```json
[
  {
    "id": 1,
    "name": "欢迎消息",
    "template_type": "welcome",
    "content": "👋 你好 {user_name}！欢迎使用机器人。",
    "language": "zh_cn",
    "variables": "{user_name}: 用户名称",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

### 创建模板

```http
POST /api/templates/
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "name": "自定义消息",
  "template_type": "welcome",
  "content": "欢迎 {user_name}！",
  "language": "zh_cn",
  "variables": "{user_name}: 用户名"
}
```

### 更新模板

```http
PUT /api/templates/{template_id}
Authorization: Bearer <token>
Content-Type: application/json
```

### 删除模板

```http
DELETE /api/templates/{template_id}
Authorization: Bearer <token>
```

---

## 审核管理

### 获取提交列表

```http
GET /api/submissions/?skip=0&limit=100&status=pending
Authorization: Bearer <token>
```

**查询参数**:
- `skip`: 跳过的记录数（分页）
- `limit`: 返回的记录数（分页）
- `status`: 筛选状态 (`pending`, `approved`, `rejected`, `replied`)

**响应**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "flow_id": 1,
    "status": "pending",
    "admin_id": null,
    "admin_note": null,
    "reply_message": null,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null,
    "processed_at": null,
    "answers": [
      {
        "id": 1,
        "submission_id": 1,
        "step_id": 1,
        "question": "请描述问题",
        "answer": "我遇到了登录问题",
        "file_id": null,
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
]
```

### 获取提交详情

```http
GET /api/submissions/{submission_id}
Authorization: Bearer <token>
```

### 更新提交

```http
PUT /api/submissions/{submission_id}
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "status": "approved",
  "admin_note": "已处理",
  "reply_message": "您的问题已解决"
}
```

### 批准提交

```http
POST /api/submissions/{submission_id}/approve
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "note": "审核通过"
}
```

### 拒绝提交

```http
POST /api/submissions/{submission_id}/reject
Authorization: Bearer <token>
Content-Type: application/json
```

**请求体**:
```json
{
  "note": "不符合要求"
}
```

---

## 用户管理

### 获取用户列表

```http
GET /api/users/?skip=0&limit=100&is_blocked=false
Authorization: Bearer <token>
```

**查询参数**:
- `skip`: 跳过的记录数
- `limit`: 返回的记录数
- `is_blocked`: 筛选是否被拉黑 (`true` / `false`)

**响应**:
```json
[
  {
    "id": 1,
    "telegram_id": 123456789,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "language": "zh_cn",
    "is_blocked": false,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### 获取用户统计

```http
GET /api/users/stats
Authorization: Bearer <token>
```

**响应**:
```json
{
  "total_users": 150,
  "active_users": 145,
  "blocked_users": 5
}
```

### 获取用户详情

```http
GET /api/users/{user_id}
Authorization: Bearer <token>
```

### 拉黑用户

```http
POST /api/users/{user_id}/block
Authorization: Bearer <token>
```

### 解除拉黑

```http
POST /api/users/{user_id}/unblock
Authorization: Bearer <token>
```

---

## 系统设置

### 获取系统设置

```http
GET /api/settings/
Authorization: Bearer <token>
```

**响应**:
```json
{
  "app_name": "Telegram 审核机器人系统",
  "admin_chat_ids": "123456789,987654321",
  "max_file_size": 10485760,
  "cors_origins": "*"
}
```

### 获取系统信息

```http
GET /api/settings/info
Authorization: Bearer <token>
```

**响应**:
```json
{
  "version": "1.0.0",
  "app_name": "Telegram 审核机器人系统"
}
```

---

## 错误响应

所有 API 在出错时都会返回统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

### HTTP 状态码

- `200 OK` - 请求成功
- `201 Created` - 创建成功
- `400 Bad Request` - 请求参数错误
- `401 Unauthorized` - 未授权（token 无效或未提供）
- `403 Forbidden` - 无权限
- `404 Not Found` - 资源不存在
- `500 Internal Server Error` - 服务器内部错误

---

## 数据类型

### 步骤类型 (StepType)

- `text` - 文本输入
- `single_choice` - 单选
- `multiple_choice` - 多选
- `image` - 图片上传
- `file` - 文件上传

### 提交状态 (SubmissionStatus)

- `pending` - 待审核
- `approved` - 已通过
- `rejected` - 已拒绝
- `replied` - 已回复

### 管理员角色 (AdminRole)

- `super_admin` - 超级管理员
- `admin` - 管理员
- `moderator` - 审核员
- `support` - 客服

### 模板类型 (TemplateType)

- `welcome` - 欢迎消息
- `submission_success` - 提交成功
- `approved` - 审核通过
- `rejected` - 审核拒绝
- `admin_notification` - 管理员通知

---

## 示例：使用 curl 调用 API

### 登录并获取 Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 使用 Token 获取数据

```bash
curl -X GET http://localhost:8000/api/dashboard/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 创建菜单

```bash
curl -X POST http://localhost:8000/api/menus/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "帮助",
    "icon": "❓",
    "order": 0,
    "is_active": true,
    "buttons_per_row": 2
  }'
```

---

## 完整 API 文档

部署后可以访问交互式 API 文档：

- Swagger UI: `http://your-domain/docs`
- ReDoc: `http://your-domain/redoc`

这些文档提供了完整的 API 定义、请求/响应示例，并可以直接在浏览器中测试 API。

---

更多信息请参考主 README.md 和 DEPLOYMENT.md 文件。
