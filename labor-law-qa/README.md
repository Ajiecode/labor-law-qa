# 劳动法智能问答系统

基于《劳动合同法》的智能法律咨询系统 - 毕业设计项目

## 项目简介

本系统是一个基于人工智能的法律咨询问答系统，采用RAG（检索增强生成）技术，结合大语言模型为用户提供专业的劳动法律咨询服务。

## 技术架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (HTML/CSS/JS)            │
├─────────────────────────────────────────────────┤
│                   后端 (Flask)                  │
│  ├── 用户管理 (注册/登录/JWT认证)              │
│  ├── 问答接口 (调用Dify API)                   │
│  └── 管理后台 (统计数据)                        │
├─────────────────────────────────────────────────┤
│                数据库 (SQLite)                 │
│  ├── 用户表                                     │
│  ├── 问答历史                                   │
│  └── 问题统计                                   │
├─────────────────────────────────────────────────┤
│              Dify (RAG + LLM)                  │
│  ├── 知识库 (劳动合同法)                        │
│  └── 工作流 (检索 + 生成)                       │
└─────────────────────────────────────────────────┘
```

## 功能模块

### 1. 用户模块
- 用户注册
- 用户登录 (JWT认证)
- 个人资料查看
- 密码修改

### 2. 问答模块
- 智能问答
- 对话历史记录
- 收藏功能
- 问题统计

### 3. 管理模块 (后台)
- 用户管理
- 问答统计
- 热门问题排行

### 4. 前端功能
- 法律目录导航
- 示例问题快捷提问
- 问答历史记录
- 移动端适配
- 加载动画

## 项目结构

```
labor-law-qa/
├── frontend/
│   └── index.html          # 前端页面
├── backend/
│   ├── app.py              # Flask应用入口
│   ├── extensions.py       # 数据库扩展
│   ├── requirements.txt    # Python依赖
│   ├── routes/
│   │   ├── auth.py         # 认证路由
│   │   ├── chat.py         # 问答路由
│   │   └── admin.py        # 管理路由
│   └── models/
│       └── __init__.py     # 数据模型
├── data/
│   └── labor_law.txt       # 劳动合同法文本
└── README.md               # 项目文档
```

## 快速部署

### 后端部署

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export DIFY_API_KEY=your_api_key  # Linux/Mac
set DIFY_API_KEY=your_api_key     # Windows

# 启动服务
python app.py
```

### 前端部署

将 `frontend/index.html` 部署到任意Web服务器或使用GitHub Pages。

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/auth/register | POST | 用户注册 |
| /api/auth/login | POST | 用户登录 |
| /api/auth/profile | GET | 获取用户信息 |
| /api/chat/ask | POST | 提问 |
| /api/chat/history | GET | 获取历史记录 |
| /api/chat/favorites | GET | 获取收藏 |
| /api/admin/stats | GET | 统计数据 |

## 数据库表

### users (用户表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String | 用户名 |
| email | String | 邮箱 |
| password_hash | String | 密码哈希 |
| role | String | 角色 (user/admin) |
| created_at | DateTime | 创建时间 |

### chat_history (问答历史)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| user_id | Integer | 用户ID |
| question | Text | 问题 |
| answer | Text | 回答 |
| is_favorite | Boolean | 是否收藏 |
| created_at | DateTime | 创建时间 |

### question_stats (问题统计)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| question_text | String | 问题内容 |
| count | Integer | 提问次数 |

## 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **后端**: Python, Flask
- **数据库**: SQLite
- **认证**: JWT
- **AI**: Dify (RAG + LLM)

## 毕业设计亮点

1. **完整的系统架构** - 前后端分离
2. **用户认证** - JWT令牌认证
3. **数据持久化** - SQLite数据库
4. **问答统计** - 问题热度分析
5. **收藏功能** - 重要问答收藏
6. **后台管理** - 管理员统计面板

## 界面预览

系统包含以下界面：
- 登录/注册页面
- 主问答页面
- 问答历史页面
- 个人中心
- 管理后台

## 扩展建议

- [ ] 添加问题分类标签
- [ ] 增加语音输入/输出
- [ ] 添加工具栏（复制、分享）
- [ ] 问题推荐功能
- [ ] 多语言支持

## 许可证

MIT License
