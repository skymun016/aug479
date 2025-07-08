#!/usr/bin/env python3
"""
Augment插件修改器 - macOS可视化应用
一个简单易用的图形界面工具，用于修改Augment插件
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import queue
import time
from modify_plugin import PluginModifier

class PluginModifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Augment插件修改器 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置应用图标和样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 用于线程间通信的队列
        self.log_queue = queue.Queue()
        self.check_queue()
        
        # 当前选择的文件
        self.selected_file = None
        self.output_dir = Path.home() / "Desktop" / "Modified_Plugins"
        
    def setup_styles(self):
        """设置应用样式"""
        style = ttk.Style()
        style.theme_use('aqua')  # macOS原生样式
        
        # 自定义样式
        style.configure('Title.TLabel', font=('SF Pro Display', 18, 'bold'))
        style.configure('Subtitle.TLabel', font=('SF Pro Display', 12))
        style.configure('Success.TLabel', foreground='#28a745')
        style.configure('Error.TLabel', foreground='#dc3545')
        
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🔧 Augment插件修改器", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="快速修改Augment插件登录选项和清理警告文字", style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="📁 选择插件文件", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="插件文件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state='readonly')
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.browse_btn = ttk.Button(file_frame, text="浏览...", command=self.browse_file)
        self.browse_btn.grid(row=0, column=2)
        
        # 输出目录选择
        output_frame = ttk.LabelFrame(main_frame, text="📂 输出设置", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="输出目录:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.output_var = tk.StringVar(value=str(self.output_dir))
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, state='readonly')
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.output_btn = ttk.Button(output_frame, text="选择...", command=self.browse_output)
        self.output_btn.grid(row=0, column=2)
        
        # 修改选项
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ 修改选项", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.remove_4th_var = tk.BooleanVar(value=True)
        self.cleanup_warnings_var = tk.BooleanVar(value=True)
        self.modify_poolhub_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="删除第4种登录方式 (AugmentProxy)", 
                       variable=self.remove_4th_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="将poolhub登录改为池子登录", 
                       variable=self.modify_poolhub_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="清理所有警告文字", 
                       variable=self.cleanup_warnings_var).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 15))
        
        self.modify_btn = ttk.Button(button_frame, text="🚀 开始修改", 
                                   command=self.start_modification, style='Accent.TButton')
        self.modify_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ 清空日志", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_output_btn = ttk.Button(button_frame, text="📂 打开输出目录", 
                                        command=self.open_output_dir)
        self.open_output_btn.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=7, column=0, columnspan=3)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="📋 操作日志", padding="10")
        log_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(15, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 初始化日志
        self.log("欢迎使用Augment插件修改器！")
        self.log("请选择要修改的插件文件(.vsix)，然后点击开始修改。")
        
    def browse_file(self):
        """浏览选择插件文件"""
        file_path = filedialog.askopenfilename(
            title="选择Augment插件文件",
            filetypes=[("VSIX文件", "*.vsix"), ("所有文件", "*.*")],
            initialdir=Path.home() / "Downloads"
        )
        
        if file_path:
            self.selected_file = Path(file_path)
            self.file_var.set(file_path)
            self.log(f"已选择文件: {self.selected_file.name}")
            
    def browse_output(self):
        """选择输出目录"""
        dir_path = filedialog.askdirectory(
            title="选择输出目录",
            initialdir=self.output_dir
        )
        
        if dir_path:
            self.output_dir = Path(dir_path)
            self.output_var.set(dir_path)
            self.log(f"输出目录设置为: {self.output_dir}")
            
    def log(self, message):
        """添加日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_queue.put(log_message)
        
    def check_queue(self):
        """检查日志队列并更新界面"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # 每100ms检查一次
        self.root.after(100, self.check_queue)
        
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清空")
        
    def open_output_dir(self):
        """打开输出目录"""
        if self.output_dir.exists():
            os.system(f"open '{self.output_dir}'")
        else:
            messagebox.showwarning("警告", "输出目录不存在")
            
    def start_modification(self):
        """开始修改插件"""
        if not self.selected_file:
            messagebox.showerror("错误", "请先选择插件文件")
            return
            
        if not self.selected_file.exists():
            messagebox.showerror("错误", "选择的文件不存在")
            return
            
        # 在新线程中执行修改
        thread = threading.Thread(target=self.modify_plugin_thread)
        thread.daemon = True
        thread.start()
        
    def modify_plugin_thread(self):
        """在后台线程中修改插件"""
        try:
            # 更新界面状态
            self.root.after(0, self.set_processing_state, True)
            
            self.log("开始修改插件...")
            self.log(f"文件: {self.selected_file.name}")
            
            # 创建输出目录
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建修改器
            modifier = PluginModifier(self.selected_file, self.output_dir)
            
            # 执行修改
            self.log("正在解压插件...")
            modifier.extract_plugin()
            
            self.log("正在查找extension.js文件...")
            js_file = modifier.find_extension_js()
            
            self.log("正在修改登录选项...")
            modifier.modify_login_options(js_file)
            
            self.log("正在重新打包插件...")
            output_file = modifier.repack_plugin()
            
            self.log("正在清理临时文件...")
            modifier.cleanup()
            
            self.log(f"✅ 修改完成！")
            self.log(f"输出文件: {output_file.name}")
            
            # 显示成功消息
            self.root.after(0, lambda: messagebox.showinfo(
                "成功", 
                f"插件修改完成！\n\n输出文件: {output_file.name}\n输出目录: {self.output_dir}"
            ))
            
        except Exception as e:
            self.log(f"❌ 修改失败: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"修改失败:\n{str(e)}"))
            
        finally:
            # 恢复界面状态
            self.root.after(0, self.set_processing_state, False)
            
    def set_processing_state(self, processing):
        """设置处理状态"""
        if processing:
            self.modify_btn.configure(state='disabled', text="正在修改...")
            self.browse_btn.configure(state='disabled')
            self.output_btn.configure(state='disabled')
            self.progress.start()
            self.status_var.set("正在处理...")
        else:
            self.modify_btn.configure(state='normal', text="🚀 开始修改")
            self.browse_btn.configure(state='normal')
            self.output_btn.configure(state='normal')
            self.progress.stop()
            self.status_var.set("就绪")

def main():
    # 创建主窗口
    root = tk.Tk()
    
    # 设置macOS特定的样式
    if sys.platform == "darwin":
        # 使用系统字体
        root.option_add('*Font', 'SF Pro Display 12')
        
        # 设置窗口样式
        root.configure(bg='#f0f0f0')
    
    # 创建应用
    app = PluginModifierGUI(root)
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main()
