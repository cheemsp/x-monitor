#!/bin/bash
# X-Monitor 服务器直跑 + 自动部署

set -e

echo "🚀 $(date '+%Y-%m-%d %H:%M:%S') 开始抓取..."

# 加载环境变量
export AUTH_TOKEN="ef1ec028a9708e004afc8375326f6c6802ea0a1b"
export CT0="784e0f617f2c593a526cb61988dc81e913382911d8771ad3fa1b1698551bab65732d1da5b9f2c54343539bcbdd654df601cb0926523b8c09095e515a5907bd8e26173c447441226bbde3b4eccedb69a8"

cd /root/.openclaw/workspace/x-monitor

# 运行抓取
python3 x_monitor.py

# 如果抓取成功，推送更新
if [ -f "docs/index.html" ]; then
    echo "📤 推送到GitHub..."
    git add docs/
    git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"
    git push origin master || echo "Push failed, will retry next time"
    echo "✅ 部署完成"
else
    echo "❌ 抓取失败，跳过部署"
fi

echo "🏁 $(date '+%Y-%m-%d %H:%M:%S') 完成"
