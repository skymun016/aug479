# Augment插件自动修改工具

这是一个自动化工具，用于快速处理新版本Augment插件的登录选项修改和警告文字清理。

## 🎯 功能特性

- ✅ 自动删除第4种登录方式（AugmentProxy登录）
- ✅ 将"poolhub登录"改为"池子登录"
- ✅ 清理所有"花钱"、"举报"相关的警告文字
- ✅ 保持代码混淆风格和功能完整性
- ✅ 自动重新打包为VSIX文件
- ✅ 支持Windows、macOS、Linux

## 📋 系统要求

- Python 3.6+
- 原版Augment插件VSIX文件

## 🚀 快速开始

### Windows用户

1. 将新版本的插件文件放到`automation`目录
2. 双击运行`modify_plugin.bat`
3. 按提示输入插件文件路径

```batch
# 示例
modify_plugin.bat augment.vscode-augment-0.498.0.vsix
```

### macOS/Linux用户

1. 给脚本添加执行权限：
```bash
chmod +x modify_plugin.sh
```

2. 运行脚本：
```bash
./modify_plugin.sh augment.vscode-augment-0.498.0.vsix
```

### 直接使用Python脚本

```bash
# 基本用法
python modify_plugin.py augment.vscode-augment-0.498.0.vsix

# 指定输出目录
python modify_plugin.py augment.vscode-augment-0.498.0.vsix -o my_output_dir
```

## 📁 文件结构

```
automation/
├── modify_plugin.py      # 主要的Python修改脚本
├── modify_plugin.bat     # Windows批处理脚本
├── modify_plugin.sh      # macOS/Linux Shell脚本
├── README.md            # 使用说明
└── modified_plugin/     # 默认输出目录
```

## 🔧 工作流程

1. **解压插件**: 自动解压VSIX文件到临时目录
2. **定位文件**: 查找`extension/out/extension.js`文件
3. **执行修改**: 
   - 删除第4种登录选项
   - 修改第3种登录选项名称
   - 清理所有警告文字
4. **重新打包**: 将修改后的文件重新打包为VSIX
5. **清理临时文件**: 自动清理工作目录

## 📝 修改详情

### 登录选项修改
- **原始**: 4种登录方式 `[o,c,u,g]`
- **修改后**: 3种登录方式 `[o,c,u]`

### 文字清理
- 删除所有包含"花钱"、"举报"的警告文字
- 将"poolhub登录"改为"池子登录"
- 保持混淆代码的格式

## 🛠️ 高级用法

### 批量处理多个版本

```bash
# 处理多个插件文件
for file in *.vsix; do
    python modify_plugin.py "$file" -o "batch_output"
done
```

### 自定义修改规则

如需修改其他内容，可以编辑`modify_plugin.py`中的`modify_login_options`方法。

## ⚠️ 注意事项

1. **备份原文件**: 工具会自动创建`.backup`备份文件
2. **版本兼容性**: 主要针对0.497.0版本设计，其他版本可能需要调整正则表达式
3. **文件权限**: 确保有足够的文件读写权限
4. **杀毒软件**: 某些杀毒软件可能会误报，请添加白名单

## 🔍 故障排除

### 常见问题

**Q: 提示"未找到extension.js文件"**
A: 检查VSIX文件是否完整，或者插件结构是否发生变化

**Q: 修改后的插件无法安装**
A: 确保原始插件文件完整，重新运行修改工具

**Q: Python脚本无法运行**
A: 检查Python版本（需要3.6+），安装必要的依赖

### 调试模式

如需查看详细的修改过程，可以修改脚本中的日志级别。

## 📞 技术支持

如遇到问题，请检查：
1. Python版本和环境
2. 插件文件完整性
3. 文件权限设置
4. 系统兼容性

## 🔄 版本更新

当Augment插件发布新版本时：
1. 下载新版本VSIX文件
2. 运行此工具进行修改
3. 如果修改失败，可能需要更新正则表达式规则

---

**注意**: 此工具仅用于学习和研究目的，请遵守相关法律法规。
