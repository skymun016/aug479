# 🚀 快速开始指南

## 一键修改新版本插件

### 方法1: 简单修改（推荐新手）

```bash
# 1. 将新版本插件放到automation目录
cp augment.vscode-augment-0.498.0.vsix automation/

# 2. 进入automation目录
cd automation

# 3. 运行修改脚本
python modify_plugin.py augment.vscode-augment-0.498.0.vsix
```

### 方法2: 完整工作流（推荐高级用户）

```bash
# 一键完成修改+Git提交+GitHub推送
python auto_workflow.py augment.vscode-augment-0.498.0.vsix \
  -r /path/to/your/repo \
  -g https://github.com/skymun016/aug479.git
```

## 📋 输出结果

修改完成后，你会得到：
- `modified_plugin/augment.vscode-augment-0.498.0-modified.vsix` - 修改后的插件
- `pojieban498/` - 解压后的项目目录（如果使用完整工作流）
- `RELEASE_NOTES.md` - 发布说明

## ⚡ 超快速命令

```bash
# Windows一键运行
modify_plugin.bat your-plugin.vsix

# macOS/Linux一键运行
./modify_plugin.sh your-plugin.vsix
```

## 🔄 处理新版本的标准流程

1. **下载新版本插件**
2. **运行自动化工具**
3. **安装修改后的插件**
4. **享受清洁的登录体验**

就这么简单！🎉
