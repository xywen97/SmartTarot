# 🌙 AI 塔罗占卜 - 重构版

基于 Python Flask + 原生前端的塔罗牌 AI 分析应用。

## ✨ 特性

- 🏗️ **前后端分离**：Python Flask 后端 + HTML/CSS/JS 前端
- 📁 **模块化设计**：代码组织清晰，易于维护和扩展
- 🎴 **完整塔罗牌库**：22 张大阿尔卡纳
- 🎲 **真随机抽牌**：使用 Python secrets 模块
- 🤖 **高质量 AI 解读**：Claude Opus 4.8，反巴纳姆 Prompt
- 🎨 **沉浸式 UI**：神秘主题，流畅动画
- 💾 **历史记录**：本地保存最近 100 次占卜
- 🔒 **安全性**：API Key 保护在后端，不暴露在前端
- 📱 **响应式**：完美适配桌面和移动设备

## 📦 项目结构

```
TarotCards/
├── backend/                  # Python 后端
│   ├── api/                  # API 路由
│   │   ├── reading.py       # 占卜 API
│   │   └── data.py          # 数据 API
│   ├── services/            # 业务逻辑
│   │   ├── tarot_service.py # 塔罗牌服务
│   │   ├── llm_service.py   # LLM 服务
│   │   └── random_service.py# 随机服务
│   ├── data/                # 数据文件
│   │   ├── tarot_deck.py   # 塔罗牌数据
│   │   ├── spreads.py      # 牌阵定义
│   │   └── prompts/        # Prompt 模板
│   ├── config.py           # 配置管理
│   ├── app.py              # Flask 应用
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   ├── index.html         # 主页面
│   ├── css/               # 样式文件
│   │   ├── variables.css  # CSS 变量
│   │   ├── base.css       # 基础样式
│   │   ├── layout.css     # 布局
│   │   ├── components.css # 组件
│   │   ├── animations.css # 动画
│   │   └── responsive.css # 响应式
│   └── js/                # JavaScript 模块
│       ├── main.js        # 主入口
│       ├── config.js      # 前端配置
│       ├── api/           # API 调用
│       ├── services/      # 前端服务
│       └── ui/            # UI 组件
├── .env                   # 环境变量
├── .gitignore            # Git 忽略
├── README.md             # 项目文档
└── run.py                # 启动脚本
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填写必要的配置：

```bash
POLOAI_API_KEY=sk-your-api-key-here
POLOAI_BASE_URL=https://poloai.top
MODEL=claude-opus-4-8
```

### 3. 启动后端服务

```bash
python3 run.py
```

后端将运行在 `http://localhost:5001`

### 4. 启动前端服务

打开新终端：

```bash
cd frontend
python3 -m http.server 8080
```

前端将运行在 `http://localhost:8080`

### 5. 开始使用

在浏览器中访问 `http://localhost:8080`

## 🔧 API 端点

### 占卜相关
- `POST /api/reading/draw` - 抽牌
- `POST /api/reading/interpret` - 获取解读（流式）

### 数据相关
- `GET /api/data/deck` - 获取塔罗牌库
- `GET /api/data/spreads` - 获取牌阵列表

### 系统
- `GET /health` - 健康检查
- `GET /` - API 信息

## 🎯 重构优势

相比单文件架构：

| 方面 | 单文件 | 重构后 |
|------|--------|--------|
| 可维护性 | ❌ 难以修改 | ✅ 模块清晰 |
| 扩展性 | ❌ 添加功能困难 | ✅ 易于扩展 |
| 安全性 | ❌ API Key 暴露 | ✅ 后端保护 |
| 代码组织 | ❌ 混在一起 | ✅ 职责分离 |
| 团队协作 | ❌ 难以协作 | ✅ 并行开发 |
| 测试 | ❌ 难以测试 | ✅ 易于测试 |

## 📝 添加新功能

### 添加新牌阵

编辑 `backend/data/spreads.py`，添加新的牌阵定义。

### 添加新牌

编辑 `backend/data/tarot_deck.py`，添加小阿尔卡纳牌数据。

### 调整 Prompt

编辑 `backend/data/prompts/*.txt` 文件。

### 添加新 API

在 `backend/api/` 目录创建新的蓝图文件。

## 🐛 故障排除

### 后端启动失败

检查 `.env` 文件是否正确配置。

### 前端连接失败

确保后端服务已启动，检查 `frontend/js/config.js` 中的 API_BASE_URL。

### CORS 错误

检查 `backend/config.py` 中的 CORS_ORIGINS 配置。

## 📄 许可证

MIT License

---

**愿塔罗之光照亮你的前路 🌙✨**
