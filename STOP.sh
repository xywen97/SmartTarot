#!/bin/bash

# 塔罗牌应用停止脚本

echo "🛑 停止 AI 塔罗占卜应用..."
echo ""

# 停止后端
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "停止后端服务..."
    lsof -ti:5001 | xargs kill -9
    echo "✅ 后端已停止"
else
    echo "⚠️  后端未运行"
fi

# 停止前端
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    echo "停止前端服务..."
    lsof -ti:8080 | xargs kill -9
    echo "✅ 前端已停止"
else
    echo "⚠️  前端未运行"
fi

echo ""
echo "✅ 所有服务已停止"
