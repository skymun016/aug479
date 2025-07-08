#!/bin/bash

echo "🍎 构建Augment插件修改器 - macOS应用"
echo "=========================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

echo "✅ Python3 环境检查通过"

# 创建应用目录结构
APP_NAME="Augment插件修改器.app"
APP_DIR="$APP_NAME/Contents"
MACOS_DIR="$APP_DIR/MacOS"
RESOURCES_DIR="$APP_DIR/Resources"

echo "📁 创建应用目录结构..."

# 清理旧的应用
if [ -d "$APP_NAME" ]; then
    rm -rf "$APP_NAME"
fi

# 创建目录
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# 创建Info.plist
echo "📝 创建Info.plist..."
cat > "$APP_DIR/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Augment插件修改器</string>
    <key>CFBundleIdentifier</key>
    <string>com.augment.plugin-modifier</string>
    <key>CFBundleName</key>
    <string>Augment插件修改器</string>
    <key>CFBundleDisplayName</key>
    <string>Augment插件修改器</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>vsix</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>VSIX Plugin File</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
            <key>LSHandlerRank</key>
            <string>Owner</string>
        </dict>
    </array>
</dict>
</plist>
EOF

# 创建启动脚本
echo "🚀 创建启动脚本..."
cat > "$MACOS_DIR/Augment插件修改器" << 'EOF'
#!/bin/bash

# 获取应用包路径
APP_PATH="$(dirname "$0")/../.."
RESOURCES_PATH="$APP_PATH/Contents/Resources"

# 切换到资源目录
cd "$RESOURCES_PATH"

# 启动Python应用
python3 gui_app.py
EOF

# 给启动脚本添加执行权限
chmod +x "$MACOS_DIR/Augment插件修改器"

# 复制Python文件到Resources目录
echo "📦 复制应用文件..."
cp gui_app.py "$RESOURCES_DIR/"
cp modify_plugin.py "$RESOURCES_DIR/"

# 创建简单的图标（使用系统默认图标）
echo "🎨 设置应用图标..."
# 这里可以添加自定义图标，暂时使用系统默认

# 创建启动器脚本（用于开发测试）
echo "🔧 创建开发启动器..."
cat > "run_app.sh" << 'EOF'
#!/bin/bash
echo "🚀 启动Augment插件修改器..."
open "Augment插件修改器.app"
EOF

chmod +x "run_app.sh"

# 创建安装说明
echo "📚 创建使用说明..."
cat > "README_APP.md" << 'EOF'
# Augment插件修改器 - macOS应用

## 🚀 使用方法

### 启动应用
1. 双击 `Augment插件修改器.app` 启动应用
2. 或者运行 `./run_app.sh` 脚本启动

### 如果遇到安全提示
1. 右键点击应用 → 选择"打开"
2. 在弹出的对话框中点击"打开"
3. 或者在系统偏好设置 → 安全性与隐私中允许运行

### 使用应用
1. **选择插件**: 点击"浏览"选择.vsix插件文件
2. **设置输出**: 选择修改后文件的保存位置
3. **开始修改**: 点击"开始修改"按钮
4. **获取结果**: 在输出目录找到修改后的插件

## 🔧 功能特性

- ✅ 图形化界面，操作简单
- ✅ 自动删除第4种登录方式
- ✅ 修改poolhub为池子登录
- ✅ 清理所有警告文字
- ✅ 实时显示操作日志
- ✅ 支持拖拽文件操作

## 📋 系统要求

- macOS 10.14 或更高版本
- Python 3.6 或更高版本
- tkinter 图形界面库（通常随Python安装）

## 🛠️ 安装到Applications

将 `Augment插件修改器.app` 拖拽到 `/Applications` 文件夹即可。

## ❓ 故障排除

**问题**: 应用无法启动
**解决**: 确保系统已安装Python3，运行 `python3 --version` 检查

**问题**: 提示"无法验证开发者"
**解决**: 右键点击应用选择"打开"，或在系统偏好设置中允许

**问题**: 修改失败
**解决**: 检查插件文件是否完整，查看应用内的错误日志

---
*享受简洁的插件修改体验！*
EOF

echo ""
echo "✅ macOS应用构建完成！"
echo ""
echo "📱 应用位置: $(pwd)/$APP_NAME"
echo "🚀 启动方式: 双击应用或运行 ./run_app.sh"
echo "📚 使用说明: README_APP.md"
echo ""
echo "💡 提示:"
echo "- 首次运行可能需要在系统偏好设置中允许"
echo "- 可以将应用拖拽到Applications文件夹"
echo "- 应用需要Python3环境支持"
echo ""
echo "🎉 构建完成！"
