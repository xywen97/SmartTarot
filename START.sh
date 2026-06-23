#!/bin/bash

# 塔罗牌应用启动脚本

echo "🌙 启动 AI 塔罗占卜应用..."
echo ""

# 检查后端是否已运行
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ 后端已在运行"
else
    echo "🚀 启动后端服务..."
    cd "$(dirname "$0")"
    python3 run.py > /tmp/tarot-backend.log 2>&1 &
    sleep 1
    
    if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ 后端启动成功: http://localhost:5001"
    else
        echo "❌ 后端启动失败，请查看日志: /tmp/tarot-backend.log"
        exit 1
    fi
fi

# 检查前端是否已运行
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ 前端已在运行"
else
    echo "🚀 启动前端服务..."
    cd "$(dirname "$0")/frontend"
    python3 -m http.server 8080 > /tmp/tarot-frontend.log 2>&1 &
    sleep 1
    
    if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ 前端启动成功: http://localhost:8080"
    else
        echo "❌ 前端启动失败，请查看日志: /tmp/tarot-frontend.log"
        exit 1
    fi
fi

echo ""
echo "=== 🎉 系统已就绪 ==="
echo "🌐 前端地址: http://localhost:8080"
echo "🔌 后端地址: http://localhost:5001"
echo ""
echo "📝 提示："
echo "  - 后端日志: /tmp/tarot-backend.log"
echo "  - 前端日志: /tmp/tarot-frontend.log"
echo "  - 停止服务: ./STOP.sh"
echo ""
echo "🌙 现在可以在浏览器中使用塔罗占卜了！"
echo ""

# 自动打开浏览器
# sleep 1
# open "http://localhost:8080"