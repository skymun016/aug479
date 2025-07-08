#!/usr/bin/env python3
"""
构建macOS应用程序
使用py2app将Python GUI应用打包为原生macOS应用
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    try:
        import py2app
        print("✅ py2app 已安装")
    except ImportError:
        print("❌ py2app 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "py2app"], check=True)
        print("✅ py2app 安装完成")

def create_setup_py():
    """创建setup.py文件"""
    print("📝 创建setup.py...")
    
    setup_content = '''
from setuptools import setup

APP = ['gui_app.py']
DATA_FILES = [
    ('', ['modify_plugin.py']),
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app_icon.icns',
    'plist': {
        'CFBundleName': 'Augment插件修改器',
        'CFBundleDisplayName': 'Augment插件修改器',
        'CFBundleIdentifier': 'com.augment.plugin-modifier',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleInfoDictionaryVersion': '6.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'LSMinimumSystemVersion': '10.14',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeExtensions': ['vsix'],
                'CFBundleTypeName': 'VSIX Plugin File',
                'CFBundleTypeRole': 'Editor',
                'LSHandlerRank': 'Owner',
            }
        ],
    },
    'packages': ['tkinter'],
    'includes': ['queue', 'threading', 'pathlib'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
'''
    
    with open('setup.py', 'w') as f:
        f.write(setup_content)
    
    print("✅ setup.py 创建完成")

def create_app_icon():
    """创建应用图标"""
    print("🎨 创建应用图标...")
    
    # 创建一个简单的图标文件（实际项目中应该使用专业设计的图标）
    icon_script = '''
import tkinter as tk
from tkinter import Canvas
import os

# 创建一个简单的图标
root = tk.Tk()
root.withdraw()

# 这里应该放置实际的图标创建代码
# 由于复杂性，我们暂时跳过图标创建
print("⚠️  图标创建跳过，使用默认图标")
'''
    
    # 如果没有图标文件，创建一个占位符
    if not os.path.exists('app_icon.icns'):
        print("⚠️  未找到图标文件，将使用默认图标")

def build_app():
    """构建应用"""
    print("🔨 开始构建macOS应用...")
    
    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # 构建应用
    try:
        subprocess.run([sys.executable, 'setup.py', 'py2app'], check=True)
        print("✅ 应用构建完成")
        
        # 检查构建结果
        app_path = Path('dist/gui_app.app')
        if app_path.exists():
            print(f"🎉 应用已创建: {app_path.absolute()}")
            print(f"📦 应用大小: {get_dir_size(app_path):.1f} MB")
            return app_path
        else:
            print("❌ 应用构建失败")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return None

def get_dir_size(path):
    """获取目录大小（MB）"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

def create_dmg(app_path):
    """创建DMG安装包"""
    print("📦 创建DMG安装包...")
    
    dmg_name = "Augment插件修改器-v1.0.dmg"
    
    try:
        # 创建临时目录
        temp_dir = Path("dmg_temp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        # 复制应用到临时目录
        shutil.copytree(app_path, temp_dir / app_path.name)
        
        # 创建应用程序文件夹的符号链接
        os.symlink('/Applications', temp_dir / 'Applications')
        
        # 创建DMG
        subprocess.run([
            'hdiutil', 'create', '-volname', 'Augment插件修改器',
            '-srcfolder', str(temp_dir),
            '-ov', '-format', 'UDZO',
            dmg_name
        ], check=True)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        print(f"✅ DMG创建完成: {dmg_name}")
        return dmg_name
        
    except subprocess.CalledProcessError as e:
        print(f"❌ DMG创建失败: {e}")
        return None

def create_installer_script():
    """创建安装脚本"""
    print("📜 创建安装说明...")
    
    install_guide = '''# Augment插件修改器 - 安装指南

## 🚀 快速安装

### 方法1: 使用DMG安装包（推荐）
1. 双击 `Augment插件修改器-v1.0.dmg`
2. 将应用拖拽到 Applications 文件夹
3. 在 Launchpad 中找到并启动应用

### 方法2: 直接使用应用
1. 解压下载的文件
2. 双击 `gui_app.app` 启动应用
3. 如果遇到安全提示，请在系统偏好设置中允许运行

## 🔧 使用方法

1. **选择插件文件**: 点击"浏览"选择要修改的.vsix插件文件
2. **设置输出目录**: 选择修改后文件的保存位置（默认为桌面）
3. **配置修改选项**: 选择要执行的修改操作
4. **开始修改**: 点击"开始修改"按钮
5. **获取结果**: 修改完成后在输出目录找到新的插件文件

## ⚙️ 修改功能

- ✅ 删除第4种登录方式 (AugmentProxy)
- ✅ 将poolhub登录改为池子登录  
- ✅ 清理所有警告文字
- ✅ 保持代码混淆和功能完整性

## 🛠️ 系统要求

- macOS 10.14 或更高版本
- 支持Intel和Apple Silicon处理器

## ❓ 常见问题

**Q: 应用无法打开，提示"无法验证开发者"**
A: 右键点击应用 → 选择"打开" → 在弹出对话框中点击"打开"

**Q: 修改后的插件无法安装**
A: 确保原始插件文件完整，重新运行修改工具

**Q: 找不到输出文件**
A: 检查输出目录设置，默认保存在桌面的"Modified_Plugins"文件夹

## 📞 技术支持

如遇到问题，请检查应用内的操作日志，或联系技术支持。

---
*Augment插件修改器 v1.0 - 让插件使用更简洁*
'''
    
    with open('INSTALL_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(install_guide)
    
    print("✅ 安装说明创建完成")

def main():
    """主函数"""
    print("🍎 Augment插件修改器 - macOS应用构建工具")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists('gui_app.py'):
        print("❌ 请在包含gui_app.py的目录中运行此脚本")
        sys.exit(1)
    
    try:
        # 1. 检查依赖
        check_dependencies()
        
        # 2. 创建setup.py
        create_setup_py()
        
        # 3. 创建图标
        create_app_icon()
        
        # 4. 构建应用
        app_path = build_app()
        if not app_path:
            sys.exit(1)
        
        # 5. 创建DMG（可选）
        print("\n是否创建DMG安装包？(y/n): ", end="")
        if input().lower() in ['y', 'yes']:
            dmg_path = create_dmg(app_path)
        
        # 6. 创建安装说明
        create_installer_script()
        
        print("\n" + "=" * 50)
        print("🎉 构建完成！")
        print(f"📱 应用位置: {app_path.absolute()}")
        print("📋 安装说明: INSTALL_GUIDE.md")
        print("\n💡 提示:")
        print("- 双击应用即可运行")
        print("- 首次运行可能需要在系统偏好设置中允许")
        print("- 可以将应用拖拽到Applications文件夹")
        
    except KeyboardInterrupt:
        print("\n❌ 构建被用户取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 构建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
