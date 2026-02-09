# X-Monitor 服务器直跑方案

## 🚀 架构

```
服务器定时任务 (每3小时)
    ↓
抓取X数据 (bird CLI)
    ↓
生成静态网站 (HTML)
    ↓
推送到GitHub → GitHub Pages自动部署
```

## ✅ 自动化程度

| 步骤 | 状态 |
|------|------|
| 抓取数据 | ✅ 自动 |
| 生成网站 | ✅ 自动 |
| 推送到GitHub | ✅ 自动 |
| GitHub Pages部署 | ✅ 自动 |
| 更新频率 | 每3小时 |

**人工干预：0%** - 完全自动化！

## 📁 文件说明

- `x_monitor.py` - 抓取脚本
- `run_and_deploy.sh` - 自动运行+部署脚本
- `docs/` - 生成的网站文件

## 🌐 访问地址

https://cheemsp.github.io/x-monitor

## ⏰ 更新频率

- **每3小时**自动抓取一次
- 抓取6个类别的热门内容
- 约30-40条推文

## 🔧 手动触发

如果需要立即更新：

```bash
cd /root/.openclaw/workspace/x-monitor
bash run_and_deploy.sh
```

## 📊 监控类别

1. 🌐 全球AI科技
2. 🇨🇳 中文AI圈
3. 🔥 中文万赞神贴
4. 🇯🇵 日区热门
5. 📊 技术干货
6. 🖼️ 带图热门

## 📝 更新日志

- 2026-02-09: 服务器直跑方案启用，完全自动化
