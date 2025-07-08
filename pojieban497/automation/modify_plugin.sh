#!/bin/bash

echo "========================================"
echo "   Augment插件自动修改工具 (macOS/Linux)"
echo "========================================"
echo

if [ $# -eq 0 ]; then
    echo "用法: $0 <插件文件路径> [输出目录]"
    echo
    echo "示例:"
    echo "  $0 augment.vscode-augment-0.497.0.vsix"
    echo "  $0 augment.vscode-augment-0.497.0.vsix modified_plugins"
    echo
    exit 1
fi

PLUGIN_PATH="$1"
OUTPUT_DIR="${2:-modified_plugin}"

echo "🔧 正在处理插件: $PLUGIN_PATH"
echo "📁 输出目录: $OUTPUT_DIR"
echo

python3 modify_plugin.py "$PLUGIN_PATH" -o "$OUTPUT_DIR"

if [ $? -eq 0 ]; then
    echo
    echo "✅ 修改完成！"
    echo "📂 请查看输出目录: $OUTPUT_DIR"
else
    echo
    echo "❌ 修改失败！"
fi

echo
