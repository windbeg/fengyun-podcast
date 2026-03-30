# 🚀 风云播客网站 - 快速部署指南

## 📋 部署前检查

✅ **已完成：**
- 网站基础框架
- 随笔内容整理
- 自动化脚本系统

✅ **当前状态：**
- 所有文件已准备就绪
- Git仓库已初始化
- 内容已提交到本地

## 🎯 部署目标

- **平台**：GitHub Pages（免费）
- **网址**：`https://yourname.github.io/fengyun-podcast/`
- **自动更新**：每天16点更新战争消息
- **手机适配**：完美响应式设计

## 🛠️ 部署方法

### 方法一：自动化脚本（推荐）

```bash
# 在网站目录运行
bash deploy_to_github.sh
```

**脚本会自动：**
- 引导您输入GitHub信息
- 配置Git设置
- 创建远程仓库连接
- 推送所有文件
- 生成自动化更新工作流

### 方法二：手动部署

如果您更喜欢手动操作：

#### 1. 创建GitHub仓库
- 访问 [github.com](https://github.com)
- 登录您的账号
- 点击 "New repository"
- 仓库名：`fengyun-podcast`
- 设为 Public
- 点击 "Create repository"

#### 2. 推送代码
```bash
# 进入网站目录
cd podcast-website

# 添加远程仓库（替换YOUR_USERNAME为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/fengyun-podcast.git

# 推送到GitHub
git push -u origin master
```

#### 3. 启用GitHub Pages
- 进入仓库的 "Settings" 页面
- 点击左侧菜单的 "Pages"
- Source 选择 "Deploy from a branch"
- Branch 选择 "master"
- 文件夹选择 "/ (root)"
- 点击 "Save"

#### 4. 访问网站
等待1-2分钟后，访问：
`https://YOUR_USERNAME.github.io/fengyun-podcast/`

## 🔄 设置自动更新（推荐）

### 选项A：本地定时任务

```bash
# 设置每天16点自动更新
bash setup_cron.sh
```

### 选项B：GitHub Actions（更推荐）

如果您已经使用了GitHub Actions工作流（包含在部署脚本中），新闻会自动每天更新，无需本地服务器。

## 📱 测试网站

部署完成后，请在手机上测试以下功能：

1. **首页加载**
   - 检查加载速度
   - 验证响应式布局

2. **随笔阅读**
   - 点击随笔链接
   - 验证阅读体验

3. **新闻页面**
   - 查看战争消息
   - 验证更新时间

4. **导航功能**
   - 测试返回按钮
   - 验证页面跳转

## 🎉 部署完成清单

- [ ] GitHub仓库已创建
- [ ] 文件已推送到GitHub
- [ ] GitHub Pages已启用
- [ ] 网站可以正常访问
- [ ] 手机测试通过
- [ ] 自动更新已设置

## 🔧 常见问题

### Q：网站访问显示404
**A：** 等待1-2分钟，GitHub Pages需要时间生效。检查仓库Settings中的Pages设置。

### Q：图片或样式不显示
**A：** 确保使用相对路径，检查文件权限。

### Q：自动更新不工作
**A：** 检查cron服务状态，查看日志文件：`cat iran_news.log`

### Q：想要自定义网站
**A：** 编辑以下文件：
- `index.html` - 首页内容和样式
- `fetch_iran_news.py` - 新闻搜索关键词
- `essays/` - 添加新随笔

## 📞 技术支持

如果遇到问题：

1. **查看日志**：`cat iran_news.log`
2. **检查状态**：`git status`
3. **测试脚本**：`python3 fetch_iran_news.py`
4. **重新部署**：`bash deploy_to_github.sh`

---

**最后更新：2026年3月30日**
**部署时间：$(date)**
```

现在我将运行部署脚本来演示整个流程：
<tool_call>exec
<arg_key>command</arg_key>
<arg_value>cd /home/admin/.openclaw/workspace/podcast-website && echo "=== 风云播客网站部署演示 ===" && echo ""