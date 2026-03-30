#!/bin/bash
# 设置定时任务脚本

echo "🚀 设置伊朗战争新闻定时更新脚本..."

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/fetch_iran_news.py"

# 检查Python脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ 错误：找不到 fetch_iran_news.py 脚本"
    exit 1
fi

echo "✅ 找到Python脚本：$PYTHON_SCRIPT"

# 确保Python脚本有执行权限
chmod +x "$PYTHON_SCRIPT"

# 创建日志目录
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "✅ 创建日志目录：$LOG_DIR"

# 生成crontab内容
CRON_JOB="0 16 * * * cd \"$SCRIPT_DIR\" && python3 \"$PYTHON_SCRIPT\" >> \"$LOG_DIR/iran_news.log\" 2>&1"

echo "📅 生成的定时任务："
echo "$CRON_JOB"

# 检查是否已有相同的定时任务
if crontab -l 2>/dev/null | grep -q "fetch_iran_news.py"; then
    echo "⚠️  警告：已存在 fetch_iran_news.py 的定时任务"
    
    read -p "是否要替换现有的定时任务？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 取消设置"
        exit 1
    fi
    
    # 导出现有crontab，排除包含fetch_iran_news.py的行
    crontab -l 2>/dev/null | grep -v "fetch_iran_news.py" | crontab -
fi

# 添加新的定时任务
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ 定时任务设置成功！"
echo ""
echo "📋 定时任务详情："
echo "   - 执行时间：每天16:00"
echo "   - 执行脚本：$PYTHON_SCRIPT"
echo "   - 日志文件：$LOG_DIR/iran_news.log"
echo ""
echo "🔧 管理命令："
echo "   - 查看定时任务：crontab -l"
echo "   - 删除定时任务：crontab -l | grep -v 'fetch_iran_news.py' | crontab -"
echo "   - 查看日志：tail -f $LOG_DIR/iran_news.log"
echo ""
echo "🧪 测试脚本："
echo "   手动运行：python3 $PYTHON_SCRIPT"
echo "   查看日志：cat $LOG_DIR/iran_news.log"

# 立即运行一次脚本进行测试
echo ""
echo "🧪 正在测试脚本..."
python3 "$PYTHON_SCRIPT"

if [ $? -eq 0 ]; then
    echo "✅ 脚本测试成功！"
    echo "🎉 自动化脚本设置完成！每天16:00将自动更新伊朗战争新闻。"
else
    echo "❌ 脚本测试失败，请检查日志：$LOG_DIR/iran_news.log"
fi