#!/bin/bash

# 随笔添加脚本 - 风云播客
# 使用方法: ./add-essay.sh "标题" "日期"

if [ $# -ne 2 ]; then
    echo "使用方法: ./add-essay.sh \"标题\" \"日期\""
    echo "例如: ./add-essay.sh \"今日感悟\" \"2026-04-01\""
    exit 1
fi

TITLE="$1"
DATE="$2"

# 创建临时随笔文件
cat > /tmp/new_essay.html << EOF
        <article class="essay">
            <h2>${TITLE}</h2>
            <p class="date">${DATE}</p>
            <p>在这里写下您的随笔内容...</p>
            <p>可以写多个段落，每个段落用 &lt;p&gt; 标签包围。</p>
            <p>支持使用 &lt;strong&gt;加粗&lt;/strong&gt; 和 &lt;em&gt;斜体&lt;/em&gt; 标签。</p>
        </article>
EOF

# 插入到随笔页面的正确位置
# 备份原文件
cp essays.html essays.html.backup

# 找到插入位置并插入新随笔
sed -i '/<!-- 新随笔插入位置 -->/r /tmp/new_essay.html' essays.html

echo "✅ 随笔模板已创建！"
echo "📝 请编辑 essays.html 文件，在临时随笔处填写您的内容"
echo "🚀 编辑完成后运行: git add . && git commit -m \"添加随笔: ${TITLE}\" && git push origin master"

# 清理临时文件
rm -f /tmp/new_essay.html