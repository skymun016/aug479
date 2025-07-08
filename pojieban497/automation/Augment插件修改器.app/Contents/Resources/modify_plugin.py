#!/usr/bin/env python3
"""
Augment插件自动修改工具
用于快速处理新版本插件的登录选项修改和警告文字清理
"""

import os
import re
import sys
import shutil
import zipfile
import argparse
from pathlib import Path

class PluginModifier:
    def __init__(self, plugin_path, output_dir="modified_plugin"):
        self.plugin_path = Path(plugin_path)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path("temp_extract")
        
    def extract_plugin(self):
        """解压插件文件"""
        print(f"正在解压插件: {self.plugin_path}")
        
        # 清理临时目录
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        
        # 解压VSIX文件
        with zipfile.ZipFile(self.plugin_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        
        print("✅ 插件解压完成")
        
    def find_extension_js(self):
        """查找extension.js文件"""
        extension_js_path = self.temp_dir / "extension" / "out" / "extension.js"
        if not extension_js_path.exists():
            raise FileNotFoundError(f"未找到extension.js文件: {extension_js_path}")
        return extension_js_path
    
    def modify_login_options(self, js_file_path):
        """修改登录选项"""
        print("正在修改登录选项...")
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原文件
        backup_path = js_file_path.with_suffix('.js.backup')
        shutil.copy2(js_file_path, backup_path)
        
        # 修改1: 删除第4个登录选项（从[o,c,u,g]改为[o,c,u]）
        content = re.sub(
            r'await n\.window\["showQuickP"\+l\(0,0,81,"Q\$8w"\)\]\(\[o,c,u,g\],A\)',
            r'await n.window["showQuickP"+l(0,0,81,"Q$8w")]([o,c,u],A)',
            content
        )
        
        # 修改2: 清理poolhub登录的警告文字，改为"池子登录"
        content = re.sub(
            r'u\[f\(380,"[^"]*"\)\]=p\(399,346\),u\.id=p\(353,386\),u\[d\(0,-108,-127\)\+"n"\]=d\(0,-212,-270\)\+d\(0,-145,-154\)\+p\(330,401\)\+"你花了钱请及时举报!";',
            r'u[f(380,"[gfA")]=p(399,346),u.id=p(353,386),u[d(0,-108,-127)+"n"]=d(0,-212,-270)+d(0,-145,-154);',
            content
        )
        
        # 修改3: 清理AugmentProxy登录的警告文字
        content = re.sub(
            r'g\[f\(384,"[^"]*"\)\]="AugmentProxy 登录",g\.id=p\(297,321\),g\[p\(392,382\)\+"n"\]=d\(0,-97,-143\)\+d\(0,-158,-202\)\+l\(0,0,11,"[^"]*"\)\+"及时举报!";',
            r'g[f(384,"v@P4")]="AugmentProxy 登录",g.id=p(297,321),g[p(392,382)+"n"]="AugmentProxy 登录";',
            content
        )
        
        # 修改4: 通用清理所有"花钱"、"举报"相关文字
        content = re.sub(r'[^"]*花.*?钱.*?举报[^"]*', '', content)
        content = re.sub(r'[^"]*及时举报[^"]*', '', content)
        
        # 保存修改后的文件
        with open(js_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 登录选项修改完成")
        return True
    
    def repack_plugin(self):
        """重新打包插件"""
        print("正在重新打包插件...")
        
        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        
        # 生成新的文件名
        original_name = self.plugin_path.stem
        new_name = f"{original_name}-modified.vsix"
        output_path = self.output_dir / new_name
        
        # 打包为VSIX文件
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(self.temp_dir)
                    zip_ref.write(file_path, arc_name)
        
        print(f"✅ 插件重新打包完成: {output_path}")
        return output_path
    
    def cleanup(self):
        """清理临时文件"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        print("✅ 临时文件清理完成")
    
    def process(self):
        """执行完整的修改流程"""
        try:
            # 1. 解压插件
            self.extract_plugin()
            
            # 2. 查找extension.js文件
            js_file = self.find_extension_js()
            
            # 3. 修改登录选项
            self.modify_login_options(js_file)
            
            # 4. 重新打包
            output_path = self.repack_plugin()
            
            # 5. 清理临时文件
            self.cleanup()
            
            print(f"\n🎉 插件修改完成！")
            print(f"📁 输出文件: {output_path}")
            print(f"📋 修改内容:")
            print(f"   - 删除第4种登录方式（AugmentProxy）")
            print(f"   - 将poolhub登录改为池子登录")
            print(f"   - 清理所有警告文字")
            
            return output_path
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            self.cleanup()
            return None

def main():
    parser = argparse.ArgumentParser(description="Augment插件自动修改工具")
    parser.add_argument("plugin_path", help="插件文件路径 (.vsix)")
    parser.add_argument("-o", "--output", default="modified_plugin", help="输出目录")
    
    args = parser.parse_args()
    
    if not Path(args.plugin_path).exists():
        print(f"❌ 插件文件不存在: {args.plugin_path}")
        sys.exit(1)
    
    modifier = PluginModifier(args.plugin_path, args.output)
    result = modifier.process()
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
