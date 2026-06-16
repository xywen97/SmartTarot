# 📦 安装指南

本文档提供详细的环境配置和安装步骤。

---

## 📋 系统要求

### 必需
- **Python**: 3.9 或更高版本
- **pip**: Python 包管理器

### 推荐
- **macOS / Linux**: 原生支持
- **Windows**: WSL2 或 Git Bash

---

## 🚀 快速安装

### 1. 克隆项目（如果还没有）

```bash
git clone <your-repo-url>
cd TarotCards
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows (Git Bash):
source venv/Scripts/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写必要配置：

```bash
# API 配置
POLOAI_API_KEY=sk-your-api-key-here
POLOAI_BASE_URL=https://poloai.top
MODEL=claude-opus-4-8

# 服务配置
DEBUG=True
CORS_ORIGINS=http://localhost:8080,http://localhost:3000,http://127.0.0.1:8080
```

### 5. 启动应用

```bash
./START.sh
```

浏览器会自动打开 `http://localhost:8080`

---

## 📦 依赖说明

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| Flask | 3.0.0 | Web 框架 |
| Flask-CORS | 4.0.0 | 跨域支持 |
| anthropic | 0.25.1 | Claude AI SDK |
| python-dotenv | 1.0.0 | 环境变量管理 |

### 可选依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| gunicorn | 21.2.0 | 生产环境 WSGI 服务器 |

---

## 🔧 详细配置

### 环境变量说明

#### 必需配置

```bash
# Claude API 配置
POLOAI_API_KEY=sk-xxx        # 你的 API Key（必需）
POLOAI_BASE_URL=https://xxx  # API 地址（必需）
MODEL=claude-opus-4-8        # 模型名称（必需）
```

#### 可选配置

```bash
# 开发模式
DEBUG=True                   # 调试模式（生产环境改为 False）

# CORS 配置
CORS_ORIGINS=http://localhost:8080,http://localhost:3000
                            # 允许的前端地址（用逗号分隔）
```

### 获取 API Key

1. 访问 [PoloAI](https://poloai.top)（或你的 API 提供商）
2. 注册/登录账号
3. 生成 API Key
4. 复制到 `.env` 文件

---

## 🐛 故障排除

### 问题 1: 找不到 Python 命令

**症状**:
```
command not found: python3
```

**解决方案**:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# 检查安装
python3 --version
```

### 问题 2: pip 安装失败

**症状**:
```
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### 问题 3: 虚拟环境激活失败

**症状**:
```
venv/bin/activate: No such file or directory
```

**解决方案**:
```bash
# 确保虚拟环境已创建
python3 -m venv venv

# 如果使用 Windows Git Bash
python -m venv venv
source venv/Scripts/activate
```

### 问题 4: 端口已被占用

**症状**:
```
Address already in use: Port 5001
```

**解决方案**:
```bash
# 查找占用端口的进程
lsof -ti:5001

# 停止该进程
kill -9 <PID>

# 或使用停止脚本
./STOP.sh
```

### 问题 5: CORS 错误

**症状**:
```
Access to fetch has been blocked by CORS policy
```

**解决方案**:
1. 检查 `.env` 中的 `CORS_ORIGINS` 配置
2. 确保前端地址在允许列表中
3. 重启后端服务

### 问题 6: API Key 无效

**症状**:
```
authentication_error: Invalid API Key
```

**解决方案**:
1. 检查 `.env` 文件中的 `POLOAI_API_KEY`
2. 确认 API Key 有效且未过期
3. 检查是否有多余的空格或引号

---

## 🔍 验证安装

### 检查 Python 版本
```bash
python3 --version
# 应该显示: Python 3.9.x 或更高
```

### 检查依赖安装
```bash
pip list | grep -E "Flask|anthropic|python-dotenv"
# 应该显示已安装的包
```

### 测试后端
```bash
# 启动后端
python3 run.py

# 新终端测试
curl http://localhost:5001/health
# 应该返回: {"status":"ok","message":"Tarot API is running"}
```

### 测试前端
```bash
# 访问前端
open http://localhost:8080
# 或在浏览器中手动打开
```

---

## 🌐 生产环境部署

### 使用 gunicorn

```bash
# 安装 gunicorn（如果还没有）
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:5001 backend.app:create_app()
```

### 使用 Nginx（推荐）

```nginx
# /etc/nginx/sites-available/tarot
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        root /path/to/TarotCards/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 环境变量配置

生产环境 `.env`:
```bash
DEBUG=False
CORS_ORIGINS=https://your-domain.com
POLOAI_API_KEY=sk-prod-xxx
```

---

## 🔄 更新应用

```bash
# 拉取最新代码
git pull

# 更新依赖
pip install -r requirements.txt --upgrade

# 重启服务
./STOP.sh
./START.sh
```

---

## 💡 开发提示

### 使用虚拟环境的好处

1. ✅ 隔离项目依赖
2. ✅ 避免版本冲突
3. ✅ 方便团队协作
4. ✅ 便于部署

### 推荐的开发工具

- **VS Code**: 轻量级编辑器，支持 Python
- **PyCharm**: 专业 Python IDE
- **Postman**: API 测试工具
- **iTerm2**: 增强版终端（macOS）

### 代码风格

项目使用 PEP 8 代码风格，推荐安装：

```bash
pip install black flake8
```

---

## 📞 获取帮助

如果遇到问题：

1. 查看 [故障排除](#-故障排除) 章节
2. 检查 [详细文档](./docs/INDEX.md)
3. 查看后端日志：`/tmp/tarot-backend.log`
4. 查看前端日志：`/tmp/tarot-frontend.log`

---

**安装时间**: ~5 分钟  
**难度**: ⭐⭐☆☆☆（简单）  
**更新时间**: 2026-06-16

🌙 祝你安装顺利！✨
