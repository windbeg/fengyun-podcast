#!/usr/bin/env python3
"""
每日16点自动获取伊朗战争最新消息
并更新到播客网站
"""

import requests
import json
import os
import sys
from datetime import datetime, timedelta
import re
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iran_news.log'),
        logging.StreamHandler()
    ]
)

class IranNewsFetcher:
    def __init__(self):
        self.website_dir = os.path.dirname(os.path.abspath(__file__))
        self.news_dir = os.path.join(self.website_dir, 'news')
        self.news_file = os.path.join(self.news_dir, 'iran-war-news.md')
        
        # 创建新闻目录
        os.makedirs(self.news_dir, exist_ok=True)
        
        # Tavily API配置
        self.tavily_api_key = os.getenv('TAVILY_API_KEY', '')
        if not self.tavily_api_key:
            logging.warning("TAVILY_API_KEY 环境变量未设置，将使用默认搜索方式")
        
    def search_news(self):
        """搜索伊朗战争相关新闻"""
        search_queries = [
            "伊朗战争 最新消息 美伊冲突",
            "Israel Iran war latest news",
            "中东局势 伊朗以色列 最新进展",
            "美伊冲突 最新动态"
        ]
        
        all_news = []
        
        for query in search_queries:
            try:
                if self.tavily_api_key:
                    news = self._search_with_tavily(query)
                else:
                    news = self._search_with_fallback(query)
                
                if news:
                    all_news.extend(news)
                    logging.info(f"搜索 '{query}' 成功，获得 {len(news)} 条新闻")
                    
            except Exception as e:
                logging.error(f"搜索 '{query}' 失败: {e}")
                continue
        
        return self._process_news(all_news)
    
    def _search_with_tavily(self, query):
        """使用Tavily API搜索新闻"""
        url = "https://api.tavily.com/search"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "query": query,
            "search_depth": "basic",
            "max_results": 5,
            "include_answer": True,
            "include_raw_content": False
        }
        
        if self.tavily_api_key:
            data["api_key"] = self.tavily_api_key
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            news_items = []
            
            if 'results' in result:
                for item in result['results']:
                    news_item = {
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'content': item.get('content', ''),
                        'published_date': item.get('published_date', ''),
                        'source': item.get('source', '')
                    }
                    news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            logging.error(f"Tavily搜索失败: {e}")
            return []
    
    def _search_with_fallback(self, query):
        """备用搜索方式（如果Tavily不可用）"""
        # 这里可以使用其他搜索API或预设的新闻摘要
        # 作为示例，返回一些模拟的新闻内容
        fallback_news = [
            {
                'title': '中东局势持续紧张',
                'content': '地区冲突仍在继续，各方寻求外交解决方案。',
                'source': '模拟新闻',
                'url': 'https://example.com'
            }
        ]
        return fallback_news
    
    def _process_news(self, news_items):
        """处理和过滤新闻内容"""
        if not news_items:
            return []
        
        # 去重和排序
        unique_news = []
        seen_titles = set()
        
        for item in news_items:
            title = item.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(item)
        
        # 过滤相关新闻
        keywords = ['伊朗', 'Israel', 'Iran', '中东', 'war', '冲突', 'war', '美伊']
        filtered_news = []
        
        for item in unique_news:
            title = item.get('title', '').lower()
            content = item.get('content', '').lower()
            
            if any(keyword in title or keyword in content for keyword in keywords):
                filtered_news.append(item)
        
        return filtered_news[:10]  # 最多保留10条新闻
    
    def generate_news_content(self, news_items):
        """生成新闻内容的HTML和Markdown"""
        if not news_items:
            return self._generate_empty_news()
        
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        
        # 生成HTML内容
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>伊朗战争最新消息 - 风云播客</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fafafa;
            padding: 1rem;
        }}
        
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        @media (min-width: 768px) {{
            .container {{
                max-width: 750px;
                margin: 2rem auto;
                padding: 2rem;
            }}
        }}
        
        h1 {{
            color: #333;
            font-size: 1.8rem;
            margin-bottom: 1rem;
            text-align: center;
        }}
        
        .update-time {{
            color: #666;
            font-size: 0.95rem;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #ff6b6b;
        }}
        
        .news-item {{
            background: #fff5f5;
            border-left: 4px solid #ff6b6b;
            padding: 1.2rem;
            margin-bottom: 1.5rem;
            border-radius: 0 8px 8px 0;
        }}
        
        .news-title {{
            color: #d63031;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }}
        
        .news-meta {{
            color: #636e72;
            font-size: 0.85rem;
            margin-bottom: 0.8rem;
        }}
        
        .news-content {{
            color: #2d3436;
            line-height: 1.8;
            margin-bottom: 1rem;
        }}
        
        .news-source {{
            color: #74b9ff;
            font-size: 0.85rem;
        }}
        
        .news-source a {{
            color: #74b9ff;
            text-decoration: none;
        }}
        
        .news-source a:hover {{
            text-decoration: underline;
        }}
        
        .back-to-index {{
            display: inline-block;
            margin-top: 2rem;
            padding: 0.8rem 1.5rem;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
        }}
        
        .back-to-index:hover {{
            background: #5a6fd8;
        }}
        
        .disclaimer {{
            background: #f1f3f4;
            padding: 1rem;
            border-radius: 6px;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #5f6368;
            border-left: 4px solid #dadce0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚔️ 伊朗战争最新消息</h1>
        <div class="update-time">最新更新：{current_time}</div>
"""
        
        # 添加新闻项
        for i, item in enumerate(news_items, 1):
            title = item.get('title', '无标题')
            content = item.get('content', '无内容')
            source = item.get('source', '未知来源')
            url = item.get('url', '')
            
            html_content += f"""
        <div class="news-item">
            <div class="news-title">{i}. {self._escape_html(title)}</div>
            <div class="news-meta">来源：{self._escape_html(source)}</div>
            <div class="news-content">{self._escape_html(content)}</div>
            <div class="news-source">
                {f'<a href="{url}" target="_blank">查看原文 →</a>' if url else ''}
            </div>
        </div>
"""
        
        html_content += """
        
        <div class="disclaimer">
            <strong>免责声明：</strong>本页面新闻内容由AI自动收集整理，仅供参考。如需准确信息，请查阅官方新闻源。
        </div>
        
        <a href="../index.html" class="back-to-index">← 返回首页</a>
    </div>
</body>
</html>
"""
        
        # 生成Markdown内容（用于备份）
        markdown_content = f"""# 伊朗战争最新消息

**最新更新：{current_time}**

---
"""
        
        for i, item in enumerate(news_items, 1):
            title = item.get('title', '无标题')
            content = item.get('content', '无内容')
            source = item.get('source', '未知来源')
            url = item.get('url', '')
            
            markdown_content += f"""
## {i}. {title}

**来源：** {source}

**内容：** {content}

{f'[查看原文]({url})' if url else ''}

---
"""
        
        markdown_content += """
> 免责声明：本页面新闻内容由AI自动收集整理，仅供参考。如需准确信息，请查阅官方新闻源。
"""
        
        return html_content, markdown_content
    
    def _generate_empty_news(self):
        """生成空新闻内容"""
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>伊朗战争最新消息 - 风云播客</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #fafafa;
            padding: 1rem;
        }}
        
        .container {{
            max-width: 750px;
            margin: 2rem auto;
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        h1 {{
            color: #333;
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }}
        
        .no-news {{
            color: #666;
            font-size: 1.2rem;
            margin: 2rem 0;
        }}
        
        .back-to-index {{
            display: inline-block;
            margin-top: 2rem;
            padding: 0.8rem 1.5rem;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚔️ 伊朗战争最新消息</h1>
        <div class="update-time">最新更新：{current_time}</div>
        <div class="no-news">
            📭 暂无相关新闻更新<br>
            请稍后再试或查看其他新闻源
        </div>
        <a href="../index.html" class="back-to-index">← 返回首页</a>
    </div>
</body>
</html>
"""
        
        return html_content, f"# 伊朗战争最新消息\n\n**最新更新：{current_time}**\n\n暂无相关新闻更新，请稍后再试。"
    
    def _escape_html(self, text):
        """转义HTML特殊字符"""
        if not text:
            return ""
        
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#39;')
        
        return text
    
    def update_main_page(self, news_summary):
        """更新首页的新闻摘要部分"""
        index_file = os.path.join(self.website_dir, 'index.html')
        
        if not os.path.exists(index_file):
            logging.warning("首页文件不存在")
            return
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找新闻部分并替换
            news_pattern = r'(<section class="section" id="news">.*?<div class="news-content">.*?</div>).*?</section>'
            replacement = f'<section class="section" id="news"><h2>⚔️ 伊朗战争消息</h2><div class="news-content">{news_summary}</div></section>'
            
            new_content = re.sub(news_pattern, replacement, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logging.info("首页新闻摘要已更新")
            else:
                logging.warning("未能找到首页新闻部分，未更新")
                
        except Exception as e:
            logging.error(f"更新首页失败: {e}")
    
    def save_news_files(self, html_content, markdown_content):
        """保存新闻文件"""
        try:
            # 保存HTML文件
            news_html_file = os.path.join(self.news_dir, 'index.html')
            with open(news_html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 保存Markdown文件
            with open(self.news_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logging.info(f"新闻文件已保存：{news_html_file}")
            
        except Exception as e:
            logging.error(f"保存新闻文件失败: {e}")
            raise
    
    def generate_news_summary(self, news_items):
        """生成首页新闻摘要"""
        if not news_items:
            return '<div class="news-update-time">最新更新：' + datetime.now().strftime('%Y年%m月%d日 %H:%M') + '</div><ul class="news-points"><li>暂无最新消息</li></ul>'
        
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        summary = f'<div class="news-update-time">最新更新：{current_time}</div><ul class="news-points">'
        
        for item in news_items[:5]:  # 只显示前5条
            title = item.get('title', '无标题')
            summary += f'<li>{self._escape_html(title)}</li>'
        
        summary += '</ul>'
        return summary
    
    def run(self):
        """主运行函数"""
        try:
            logging.info("开始获取伊朗战争最新消息...")
            
            # 搜索新闻
            news_items = self.search_news()
            
            if news_items:
                logging.info(f"成功获取 {len(news_items)} 条相关新闻")
                
                # 生成内容
                html_content, markdown_content = self.generate_news_content(news_items)
                
                # 保存文件
                self.save_news_files(html_content, markdown_content)
                
                # 更新首页摘要
                news_summary = self.generate_news_summary(news_items)
                self.update_main_page(news_summary)
                
                logging.info("伊朗战争新闻更新完成")
                
            else:
                logging.warning("未获取到相关新闻，生成空页面")
                html_content, markdown_content = self.generate_news_content([])
                self.save_news_files(html_content, markdown_content)
                
        except Exception as e:
            logging.error(f"获取新闻时发生错误: {e}")
            sys.exit(1)

def main():
    """主函数"""
    fetcher = IranNewsFetcher()
    fetcher.run()

if __name__ == "__main__":
    main()