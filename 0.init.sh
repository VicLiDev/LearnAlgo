#!/bin/bash
# 初始化脚本 - 仅在使用 tools 模块时需要执行

set -e

echo "=== LearnAI Tools 初始化 ==="
echo ""
echo "此脚本仅需在以下情况执行："
echo "  - 新电脑首次使用"
echo "  - 需要使用 tools 中的模块（如 matplotlib 中文显示）"
echo ""
echo "如果只是运行普通的 demo 文件（不依赖 tools 模块），则无需执行。"
echo ""

read -p "是否继续初始化？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 进入 tools 目录安装包
cd "$(dirname "$0")/tools"
pip install -e .

# 清除 matplotlib 字体缓存
rm -rf ~/.cache/matplotlib

echo ""
echo "✓ 初始化完成"
