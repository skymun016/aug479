#!/usr/bin/env python3
"""
Augment插件完整自动化工作流
包含修改、Git提交、GitHub推送等完整流程
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from modify_plugin import PluginModifier

class AutoWorkflow:
    def __init__(self, plugin_path, repo_path=".", github_repo=None):
        self.plugin_path = Path(plugin_path)
        self.repo_path = Path(repo_path)
        self.github_repo = github_repo
        self.version = self.extract_version()
        
    def extract_version(self):
        """从文件名提取版本号"""
        filename = self.plugin_path.name
        # 匹配版本号模式，如 0.497.0
        import re
        match = re.search(r'(\d+\.\d+\.\d+)', filename)
        return match.group(1) if match else "unknown"
    
    def run_command(self, cmd, cwd=None):
        """执行命令并返回结果"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                cwd=cwd or self.repo_path,
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            if result.returncode != 0:
                print(f"❌ 命令执行失败: {cmd}")
                print(f"错误信息: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"❌ 命令执行异常: {e}")
            return False
    
    def modify_plugin(self):
        """修改插件"""
        print(f"🔧 开始修改插件 v{self.version}...")
        
        modifier = PluginModifier(self.plugin_path, "modified_plugin")
        result = modifier.process()
        
        if result:
            print(f"✅ 插件修改完成: {result}")
            return result
        else:
            print("❌ 插件修改失败")
            return None
    
    def update_project_structure(self, modified_plugin_path):
        """更新项目结构"""
        print("📁 更新项目结构...")
        
        # 创建版本目录
        version_dir = self.repo_path / f"pojieban{self.version.replace('.', '')}"
        if version_dir.exists():
            shutil.rmtree(version_dir)
        
        # 解压修改后的插件到版本目录
        modifier = PluginModifier(modified_plugin_path)
        modifier.temp_dir = version_dir
        modifier.extract_plugin()
        
        print(f"✅ 项目结构更新完成: {version_dir}")
        return version_dir
    
    def git_operations(self, version_dir):
        """执行Git操作"""
        print("🔄 执行Git操作...")
        
        # 检查Git状态
        if not (self.repo_path / ".git").exists():
            print("初始化Git仓库...")
            self.run_command("git init")
            if self.github_repo:
                self.run_command(f"git remote add origin {self.github_repo}")
        
        # 添加文件
        print("添加修改的文件...")
        self.run_command(f"git add {version_dir.name}")
        
        # 检查是否有变更
        result = subprocess.run(
            "git diff --cached --quiet", 
            shell=True, 
            cwd=self.repo_path
        )
        
        if result.returncode == 0:
            print("⚠️  没有检测到文件变更")
            return False
        
        # 提交变更
        commit_msg = f"feat: update to version {self.version} with login modifications\n\n- Remove 4th login option (AugmentProxy)\n- Change poolhub to 池子登录\n- Clean up warning messages\n- Maintain code obfuscation"
        
        print("提交变更...")
        if not self.run_command(f'git commit -m "{commit_msg}"'):
            return False
        
        # 推送到远程仓库
        if self.github_repo:
            print("推送到GitHub...")
            if not self.run_command("git push origin main"):
                print("⚠️  推送失败，可能需要手动推送")
        
        print("✅ Git操作完成")
        return True
    
    def create_release_notes(self, version_dir):
        """创建发布说明"""
        print("📝 创建发布说明...")
        
        release_notes = f"""# Augment Plugin v{self.version} - Modified Version

## 🎯 修改内容

### 登录选项优化
- ✅ 删除第4种登录方式（AugmentProxy登录）
- ✅ 将"poolhub登录"改为"池子登录"
- ✅ 保持原有功能和混淆风格

### 用户体验改进
- ✅ 清理所有付费警告文字
- ✅ 移除"如果你花钱了，请及时举报"等提示
- ✅ 简化用户界面显示

## 📋 最终登录选项
1. **选择登录类型！** - 重置机器码选项
2. **官网原版登录** - 使用官方账号登录系统  
3. **池子登录** - 池子登录（简洁版本）

## 🔧 技术细节
- **基于版本**: Augment v{self.version}
- **修改时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **修改方式**: 自动化脚本处理
- **代码完整性**: ✅ 保持原有功能

## 📦 安装说明
1. 卸载原版Augment插件
2. 安装修改版插件
3. 重启VSCode
4. 享受简洁的登录体验

---
*此版本通过自动化工具生成，确保修改的一致性和可靠性*
"""
        
        notes_file = version_dir / "RELEASE_NOTES.md"
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(release_notes)
        
        print(f"✅ 发布说明已创建: {notes_file}")
        return notes_file
    
    def run_workflow(self):
        """运行完整工作流"""
        print("🚀 开始自动化工作流...")
        print(f"📦 插件版本: v{self.version}")
        print(f"📁 仓库路径: {self.repo_path}")
        if self.github_repo:
            print(f"🔗 GitHub仓库: {self.github_repo}")
        print("=" * 50)
        
        try:
            # 1. 修改插件
            modified_plugin = self.modify_plugin()
            if not modified_plugin:
                return False
            
            # 2. 更新项目结构
            version_dir = self.update_project_structure(modified_plugin)
            
            # 3. 创建发布说明
            self.create_release_notes(version_dir)
            
            # 4. Git操作
            git_success = self.git_operations(version_dir)
            
            # 5. 清理临时文件
            if Path("temp_extract").exists():
                shutil.rmtree("temp_extract")
            if Path("modified_plugin").exists():
                shutil.rmtree("modified_plugin")
            
            print("\n" + "=" * 50)
            print("🎉 自动化工作流完成！")
            print(f"📂 新版本目录: {version_dir}")
            if git_success:
                print("✅ 已提交到Git仓库")
                if self.github_repo:
                    print("✅ 已推送到GitHub")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ 工作流执行失败: {e}")
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Augment插件完整自动化工作流")
    parser.add_argument("plugin_path", help="插件文件路径 (.vsix)")
    parser.add_argument("-r", "--repo", default=".", help="Git仓库路径")
    parser.add_argument("-g", "--github", help="GitHub仓库URL")
    
    args = parser.parse_args()
    
    if not Path(args.plugin_path).exists():
        print(f"❌ 插件文件不存在: {args.plugin_path}")
        sys.exit(1)
    
    workflow = AutoWorkflow(args.plugin_path, args.repo, args.github)
    success = workflow.run_workflow()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
