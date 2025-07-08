#!/bin/bash

echo "🍎 Augment插件修改器 - 一键构建macOS应用"
echo "=============================================="

# 检查当前目录
if [ ! -f "gui_app.py" ]; then
    echo "❌ 请在包含gui_app.py的automation目录中运行此脚本"
    exit 1
fi

# 检查Python环境
echo "🔍 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    echo "💡 建议使用Homebrew安装: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python版本: $PYTHON_VERSION"

# 检查tkinter
echo "🔍 检查tkinter库..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ tkinter 可用"
else
    echo "❌ tkinter 不可用"
    echo "💡 请安装tkinter: brew install python-tk"
    exit 1
fi

# 构建应用
echo ""
echo "🔨 开始构建应用..."
./build_simple_app.sh

if [ $? -eq 0 ]; then
    echo ""
    echo "🧪 测试应用..."
    
    # 检查应用是否创建成功
    if [ -d "Augment插件修改器.app" ]; then
        echo "✅ 应用创建成功"
        
        # 询问是否立即测试
        echo ""
        read -p "是否立即启动应用进行测试？(y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🚀 启动应用..."
            open "Augment插件修改器.app"
            
            echo ""
            echo "📋 测试清单:"
            echo "1. 应用是否正常启动？"
            echo "2. 界面是否正确显示？"
            echo "3. 文件选择功能是否正常？"
            echo "4. 输出目录设置是否正常？"
            echo "5. 日志显示是否正常？"
            echo ""
            echo "💡 如果测试通过，应用就可以使用了！"
        fi
        
        # 创建分发包
        echo ""
        read -p "是否创建分发包？(y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "📦 创建分发包..."
            
            DIST_NAME="Augment插件修改器-v1.0-macOS"
            
            # 清理旧的分发包
            if [ -d "$DIST_NAME" ]; then
                rm -rf "$DIST_NAME"
            fi
            
            # 创建分发目录
            mkdir "$DIST_NAME"
            
            # 复制应用
            cp -R "Augment插件修改器.app" "$DIST_NAME/"
            
            # 复制说明文件
            cp README_APP.md "$DIST_NAME/"
            
            # 创建快速启动脚本
            cat > "$DIST_NAME/启动应用.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
open "Augment插件修改器.app"
EOF
            chmod +x "$DIST_NAME/启动应用.command"
            
            # 创建安装说明
            cat > "$DIST_NAME/安装说明.txt" << 'EOF'
Augment插件修改器 - 安装说明

🚀 快速开始:
1. 双击"启动应用.command"或直接双击应用
2. 如果遇到安全提示，右键选择"打开"

📱 安装到应用程序:
将"Augment插件修改器.app"拖拽到Applications文件夹

⚙️ 系统要求:
- macOS 10.14+
- Python 3.6+

❓ 问题反馈:
查看README_APP.md获取详细说明
EOF
            
            # 创建压缩包
            echo "🗜️ 创建压缩包..."
            zip -r "$DIST_NAME.zip" "$DIST_NAME" > /dev/null
            
            echo "✅ 分发包创建完成:"
            echo "📁 目录: $DIST_NAME/"
            echo "📦 压缩包: $DIST_NAME.zip"
            echo ""
            echo "💡 可以将压缩包分享给其他用户使用"
        fi
        
    else
        echo "❌ 应用创建失败"
        exit 1
    fi
else
    echo "❌ 构建失败"
    exit 1
fi

echo ""
echo "🎉 所有操作完成！"
echo ""
echo "📋 文件清单:"
echo "- Augment插件修改器.app (macOS应用)"
echo "- README_APP.md (使用说明)"
echo "- run_app.sh (启动脚本)"
if [ -d "$DIST_NAME" ]; then
    echo "- $DIST_NAME/ (分发目录)"
    echo "- $DIST_NAME.zip (分发压缩包)"
fi
echo ""
echo "🚀 使用方法:"
echo "1. 双击应用启动"
echo "2. 选择插件文件"
echo "3. 点击开始修改"
echo "4. 获取修改后的插件"
echo ""
echo "💡 享受简洁的插件修改体验！"
