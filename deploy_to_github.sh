#!/bin/bash
# GitHub Pages 自动部署脚本

echo "🚀 风云播客网站 - GitHub Pages 部署脚本"
echo "====================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo -e "${RED}❌ 错误：请在网站根目录（包含index.html的目录）运行此脚本${NC}"
    exit 1
fi

echo -e "${BLUE}ℹ️  当前目录：$(pwd)${NC}"

# 获取GitHub用户名
read -p "${YELLOW}请输入您的GitHub用户名：${NC}" GITHUB_USERNAME

# 获取仓库名称（提供默认值）
read -p "${YELLOW}请输入仓库名称（默认：fengyun-podcast）：${NC}" REPO_NAME
REPO_NAME=${REPO_NAME:-fengyun-podcast}

# 仓库URL
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
PAGES_URL="https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/"

echo -e "${GREEN}✅ 仓库信息：${NC}"
echo -e "   用户名：${GITHUB_USERNAME}"
echo -e "   仓库名：${REPO_NAME}"
echo -e "   仓库URL：${REPO_URL}"
echo -e "   网站URL：${PAGES_URL}"

# 确认信息
read -p "${YELLOW}请确认以上信息是否正确？(y/n): ${NC}" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ 部署已取消${NC}"
    exit 1
fi

# 检查git配置
echo -e "${BLUE}🔍 检查Git配置...${NC}"
GIT_EMAIL=$(git config user.email 2>/dev/null)
GIT_NAME=$(git config user.name 2>/dev/null)

if [ -z "$GIT_EMAIL" ] || [ -z "$GIT_NAME" ]; then
    echo -e "${YELLOW}⚠️  Git配置不完整，正在配置...${NC}"
    read -p "${YELLOW}请输入您的Git邮箱：${NC}" INPUT_EMAIL
    read -p "${YELLOW}请输入您的Git姓名：${NC}" INPUT_NAME
    
    git config user.email "$INPUT_EMAIL"
    git config user.name "$INPUT_NAME"
    
    echo -e "${GREEN}✅ Git配置完成${NC}"
else
    echo -e "${GREEN}✅ Git配置已存在${NC}"
fi

# 检查是否已初始化git仓库
if [ ! -d ".git" ]; then
    echo -e "${BLUE}📦 初始化Git仓库...${NC}"
    git init
fi

# 添加所有文件
echo -e "${BLUE}📝 添加文件到Git...${NC}"
git add .

# 检查是否有变更
if git diff-index --quiet HEAD; then
    echo -e "${YELLOW}⚠️  没有新的变更需要提交${NC}"
else
    echo -e "${BLUE}💾 提交变更...${NC}"
    git commit -m "部署播客网站到GitHub Pages

$(date '+%Y年%m月%d日 %H:%M') - 自动部署

包含内容：
- 响应式播客网站
- 随笔文章展示
- 伊朗战争新闻自动更新
- 完整的文档和脚本"
fi

# 检查远程仓库
if git remote get-url origin &>/dev/null; then
    echo -e "${BLUE}🔄 更新远程仓库URL...${NC}"
    git remote set-url origin "$REPO_URL"
else
    echo -e "${BLUE}🔗 添加远程仓库...${NC}"
    git remote add origin "$REPO_URL"
fi

# 推送到GitHub
echo -e "${BLUE}🚀 推送到GitHub...${NC}"
if git push -u origin master; then
    echo -e "${GREEN}✅ 推送成功！${NC}"
else
    echo -e "${RED}❌ 推送失败！请检查：${NC}"
    echo -e "   1. GitHub用户名是否正确"
    echo -e "   2. 仓库是否已创建"
    echo -e "   3. 网络连接是否正常"
    echo -e "   4. 是否有推送权限"
    echo -e ""
    echo -e "${YELLOW}💡 手动创建仓库步骤：${NC}"
    echo -e "   1. 访问：https://github.com"
    echo -e "   2. 登录您的账号"
    echo -e "   3. 点击 'New repository'"
    echo -e "   4. 仓库名：${REPO_NAME}"
    echo -e "   5. 设置为 Public"
    echo -e "   6. 点击 'Create repository'"
    echo -e "   7. 创建后重新运行此脚本"
    exit 1
fi

# 显示后续步骤
echo ""
echo -e "${GREEN}🎉 部署成功！${NC}"
echo ""
echo -e "${BLUE}📋 后续步骤：${NC}"
echo ""
echo -e "1. ${YELLOW}访问GitHub仓库：${NC}"
echo -e "   ${REPO_URL}"
echo ""
echo -e "2. ${YELLOW}启用GitHub Pages：${NC}"
echo -e "   a) 点击仓库中的 'Settings'"
echo -e "   b) 在左侧菜单点击 'Pages'"
echo -e "   c) 在 'Source' 部分选择 'Deploy from a branch'"
echo -e "   d) Branch 选择 'master'"
echo -e "   e) 文件夹选择 '/ (root)'"
echo -e "   f) 点击 'Save'"
echo ""
echo -e "3. ${YELLOW}访问您的网站：${NC}"
echo -e "   ${PAGES_URL}"
echo -e "   注意：首次启用可能需要1-2分钟生效"
echo ""
echo -e "4. ${YELLOW}设置自动更新（可选）：${NC}"
echo -e "   运行：bash setup_cron.sh"
echo ""

# 生成GitHub Actions工作流文件（如果用户想要自动化更新）
echo -e "${BLUE}📄 创建GitHub Actions自动化更新文件...${NC}"
mkdir -p .github/workflows

cat > .github/workflows/update-news.yml << EOF
name: 更新伊朗战争新闻

on:
  schedule:
    - cron: '0 16 * * *'  # 每天16:00（UTC+8，对应北京时间0点，如需北京时间16点请改为 '0 8 * * *'）
  workflow_dispatch:    # 支持手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
    - name: 检出仓库
      uses: actions/checkout@v3
      
    - name: 设置Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install requests
        
    - name: 更新新闻
      run: python fetch_iran_news.py
      
    - name: 提交更改
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --staged --quiet || git commit -m "自动更新战争消息 $(date '+%Y-%m-%d %H:%M:%S')"
        git push
      continue-on-error: true

    - name: 部署到GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/master'
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: .
        publish_branch: gh-pages
        destination_dir: .
EOF

echo -e "${GREEN}✅ GitHub Actions工作流已创建${NC}"
echo ""
echo -e "${BLUE}ℹ️  关于自动化更新：${NC}"
echo -e "   - 每天16:00（北京时间）自动更新新闻"
echo -e "   - 可以手动触发更新"
echo -e "   - 需要将代码推送到gh-pages分支以生效"
echo ""

# 提交GitHub Actions工作流
git add .github/workflows/update-news.yml
git commit -m "添加GitHub Actions自动化更新工作流" 2>/dev/null || true
git push origin master 2>/dev/null || true

echo -e "${GREEN}🎊 所有操作完成！${NC}"
echo -e "${BLUE}感谢使用风云播客网站！${NC}"