# 风云播客网站

一个简洁的个人播客网站，分享生活随笔与伊朗战争每日最新消息。

## 🌟 特点

- ✅ **手机优先设计** - 完美适配手机阅读
- ✅ **静态网站** - 快速加载，安全可靠  
- ✅ **自动化更新** - 每天16:00自动获取伊朗战争最新消息
- ✅ **免费部署** - 使用GitHub Pages免费托管
- ✅ **响应式布局** - 电脑手机都能完美显示

## 📁 网站结构

```
podcast-website/
├── index.html                    # 首页
├── essays/                      # 随笔目录
│   ├── 2026-03-25.html         # 3月25日随笔
│   └── 2026-03-23.html         # 3月23日随笔
├── news/                        # 战争消息
│   └── index.html              # 最新战争消息
├── fetch_iran_news.py          # 自动化脚本
├── setup_cron.sh               # 定时任务设置脚本
└── README.md                   # 说明文档
```

## 🚀 快速开始

### 1. 手动更新新闻

```bash
# 进入网站目录
cd podcast-website

# 运行脚本获取最新新闻
python3 fetch_iran_news.py
```

### 2. 设置自动更新（推荐）

```bash
# 运行设置脚本
bash setup_cron.sh

# 脚本会自动：
# - 设置每天16:00的定时任务
# - 创建日志目录
# - 测试脚本运行
# - 显示管理命令
```

## 📱 网站预览

### 首页
- 网站标题和介绍
- 最新随笔列表
- 伊朗战争消息摘要
- 导航菜单

### 随笔页面
- 优美的大字体阅读体验
- 章节导航
- 响应式布局
- 返回首页按钮

### 战争消息页面
- 每日16:00自动更新
- 新闻来源标注
- 查看原文链接
- 免责声明

## 🛠️ 技术栈

- **前端**：纯HTML + CSS + JavaScript
- **后端**：Python 3 + Requests
- **搜索**：Tavily API（可选）
- **部署**：GitHub Pages
- **自动化**：Cron定时任务

## 📝 内容管理

### 添加新随笔

1. 在 `essays/` 目录创建新的HTML文件
2. 文件名格式：`YYYY-MM-DD.html`
3. 参考 `essays/2026-03-25.html` 的格式
4. 更新首页的随笔列表

### 配置搜索API

如果要使用Tavily API进行新闻搜索：

```bash
# 设置环境变量
export TAVILY_API_KEY="your_api_key_here"

# 或者在脚本中直接修改
```

如果没有API密钥，脚本会使用备用搜索方式。

## 📊 监控和日志

### 查看日志
```bash
# 实时查看日志
tail -f logs/iran_news.log

# 查看最近日志
cat logs/iran_news.log
```

### 管理定时任务
```bash
# 查看所有定时任务
crontab -l

# 删除新闻更新定时任务
crontab -l | grep -v 'fetch_iran_news.py' | crontab -

# 手动运行测试
python3 fetch_iran_news.py
```

## 🌍 部署到GitHub Pages

### 方法一：手动上传

1. 将整个 `podcast-website` 目录上传到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 选择根目录作为发布源
4. 访问：`https://yourusername.github.io/podcast-website/`

### 方法二：GitHub Actions（自动化）

```yaml
# .github/workflows/update-news.yml
name: 更新战争消息
on:
  schedule:
    - cron: '0 16 * * *'  # 每天16:00
  workflow_dispatch:      # 支持手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: 设置Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: 安装依赖
        run: pip install requests
      - name: 更新新闻
        run: python fetch_iran_news.py
      - name: 提交更改
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "自动更新战争消息 $(date '+%Y-%m-%d %H:%M')" || exit 0
          git push
```

## 🔧 自定义设置

### 修改网站标题
编辑 `index.html` 文件中的：
```html
<h1>风云播客</h1>
```

### 修改更新时间
编辑 `fetch_iran_news.py` 中的：
```python
# 修改这一行中的时间
search_queries = [
    "伊朗战争 最新消息 美伊冲突",
    # ...
]
```

### 添加新的新闻源
在 `fetch_iran_news.py` 的 `_search_with_tavily` 方法中添加新的搜索逻辑。

## 📞 支持

如果遇到问题：

1. 检查Python版本（需要Python 3.6+）
2. 查看日志文件 `logs/iran_news.log`
3. 手动运行脚本测试：`python3 fetch_iran_news.py`
4. 检查网络连接和API密钥（如果使用）

## 📄 许可证

本网站内容采用原创许可，代码部分采用MIT许可证。

---

**最后更新：2026年3月30日**