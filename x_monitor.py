#!/usr/bin/env python3
"""
X-Monitor MVP
Twitter/X 热点监控 - 全类别抓取
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

# 搜索配置（来自 docs/x-search-tips.md）
SEARCH_QUERIES = {
    "global_ai": {
        "name": "🌐 全球AI科技",
        "query": '"AI" OR "ChatGPT" OR "Claude" OR "Gemini" OR "OpenAI" OR "Anthropic" lang:en min_faves:3000 within_time:12h -is:retweet',
        "limit": 10
    },
    "cn_ai": {
        "name": "🇨🇳 中文AI圈",
        "query": '"AI" OR "提示词" OR "大模型" OR "ChatGPT" lang:zh-cn min_faves:300 within_time:12h -is:retweet',
        "limit": 10
    },
    "cn_viral": {
        "name": "🔥 中文万赞神贴",
        "query": "lang:zh-cn min_faves:10000 -is:retweet within_time:24h",
        "limit": 5
    },
    "jp_trending": {
        "name": "🇯🇵 日区热门",
        "query": "lang:ja min_faves:500 within_time:4h -is:retweet",
        "limit": 8
    },
    "tech_insights": {
        "name": "📊 技术干货",
        "query": "lang:en min_faves:5000 filter:links within_time:12h -is:retweet",
        "limit": 8
    },
    "visual": {
        "name": "🖼️ 带图热门",
        "query": "filter:images lang:zh-cn min_faves:500 within_time:12h -is:retweet",
        "limit": 6
    }
}

def run_bird_search(query, limit=10):
    """运行bird搜索"""
    auth_token = os.environ.get('AUTH_TOKEN', '').strip()
    ct0 = os.environ.get('CT0', '').strip()
    
    if not auth_token or not ct0:
        return []
    
    cmd = [
        'bird', 'search', query,
        '-n', str(limit),
        '--auth-token', auth_token,
        '--ct0', ct0,
        '--plain'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return parse_tweets(result.stdout)
    except Exception as e:
        print(f"Error: {e}")
    return []

def parse_tweets(output):
    """解析bird输出"""
    tweets = []
    current = {}
    
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('@'):
            if current:
                tweets.append(current)
            current = {'user': line, 'content': '', 'date': '', 'url': ''}
        elif line.startswith('date:'):
            current['date'] = line.replace('date:', '').strip()
        elif line.startswith('url:'):
            current['url'] = line.replace('url:', '').strip()
        elif line and not line.startswith('─') and not line.startswith('PHOTO') and not line.startswith('VIDEO'):
            current['content'] += line + ' '
    
    if current:
        tweets.append(current)
    
    return tweets

def generate_html(data, output_dir):
    """生成HTML页面"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H:%M')
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X-Monitor | AI热点监控</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: #0f0f23;
            color: #e0e0e0;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem 1rem;
            text-align: center;
            border-bottom: 1px solid #2a2a4a;
        }}
        .header h1 {{
            font-size: 1.8rem;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .header .meta {{
            color: #888;
            font-size: 0.9rem;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 1rem;
        }}
        .category {{
            margin-bottom: 2rem;
            background: #1a1a2e;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #2a2a4a;
        }}
        .category-header {{
            background: linear-gradient(90deg, #2a2a4a 0%, #1a1a2e 100%);
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-bottom: 1px solid #2a2a4a;
        }}
        .tweet {{
            padding: 1rem 1.5rem;
            border-bottom: 1px solid #2a2a4a;
            transition: background 0.2s;
        }}
        .tweet:hover {{
            background: #252542;
        }}
        .tweet:last-child {{
            border-bottom: none;
        }}
        .tweet-user {{
            color: #00d4ff;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }}
        .tweet-content {{
            color: #e0e0e0;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }}
        .tweet-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #888;
        }}
        .tweet-link {{
            color: #7b2cbf;
            text-decoration: none;
        }}
        .tweet-link:hover {{
            text-decoration: underline;
        }}
        .empty {{
            padding: 2rem;
            text-align: center;
            color: #666;
        }}
        .nav {{
            position: sticky;
            top: 0;
            background: rgba(15, 15, 35, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-bottom: 1px solid #2a2a4a;
            z-index: 100;
        }}
        .nav-links {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .nav-link {{
            color: #888;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            transition: all 0.2s;
        }}
        .nav-link:hover, .nav-link.active {{
            color: #00d4ff;
            background: #2a2a4a;
        }}
        @media (max-width: 600px) {{
            .header h1 {{ font-size: 1.4rem; }}
            .container {{ padding: 0.5rem; }}
            .tweet {{ padding: 0.8rem 1rem; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>🤖 X-Monitor</h1>
        <div class="meta">AI科技热点监控 | {date_str} {time_str} 更新</div>
    </header>
    
    <nav class="nav">
        <div class="nav-links">
            <a href="#global_ai" class="nav-link">🌐 全球AI</a>
            <a href="#cn_ai" class="nav-link">🇨🇳 中文AI</a>
            <a href="#cn_viral" class="nav-link">🔥 万赞</a>
            <a href="#jp_trending" class="nav-link">🇯🇵 日区</a>
            <a href="#tech_insights" class="nav-link">📊 干货</a>
            <a href="#visual" class="nav-link">🖼️ 带图</a>
        </div>
    </nav>
    
    <main class="container">
"""
    
    # 生成各分类内容
    for key, config in SEARCH_QUERIES.items():
        tweets = data.get(key, [])
        html += f'<section class="category" id="{key}">\n'
        html += f'<div class="category-header">{config["name"]}</div>\n'
        
        if tweets:
            for tweet in tweets[:config['limit']]:
                content = tweet.get('content', '')[:300]
                if len(tweet.get('content', '')) > 300:
                    content += '...'
                
                html += '<div class="tweet">\n'
                html += f'<div class="tweet-user">{tweet.get("user", "")}</div>\n'
                html += f'<div class="tweet-content">{content}</div>\n'
                html += '<div class="tweet-meta">\n'
                html += f'<span>{tweet.get("date", "")}</span>\n'
                if tweet.get('url'):
                    html += f'<a href="{tweet["url"]}" target="_blank" class="tweet-link">查看原文 →</a>\n'
                html += '</div>\n'
                html += '</div>\n'
        else:
            html += '<div class="empty">暂无数据</div>\n'
        
        html += '</section>\n'
    
    html += """
    </main>
    
    <footer style="text-align: center; padding: 2rem; color: #666; font-size: 0.85rem;">
        <p>X-Monitor MVP | 自动抓取 · 每小时更新</p>
        <p style="margin-top: 0.5rem;">🤖 by NAVI</p>
    </footer>
</body>
</html>
"""
    
    # 保存文件
    output_path = Path(output_dir) / 'index.html'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding='utf-8')
    print(f"✅ HTML已生成: {output_path}")

def main():
    """主函数"""
    print("🚀 X-Monitor MVP 开始抓取...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 创建输出目录
    output_dir = Path('/tmp/x-monitor/docs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 抓取所有类别
    all_data = {}
    for key, config in SEARCH_QUERIES.items():
        print(f"\n🔍 抓取: {config['name']}")
        tweets = run_bird_search(config['query'], config['limit'])
        all_data[key] = tweets
        print(f"   找到 {len(tweets)} 条推文")
    
    # 保存JSON数据
    data_file = output_dir / 'data.json'
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.now().isoformat(),
            'data': all_data
        }, f, ensure_ascii=False, indent=2)
    print(f"\n💾 数据已保存: {data_file}")
    
    # 生成HTML
    generate_html(all_data, output_dir)
    
    print("\n✅ 完成!")

if __name__ == '__main__':
    main()
