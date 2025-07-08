@echo off
chcp 65001 >nul
echo ========================================
echo    Augment插件自动修改工具 (Windows)
echo ========================================
echo.

if "%~1"=="" (
    echo 用法: %0 ^<插件文件路径^> [输出目录]
    echo.
    echo 示例:
    echo   %0 augment.vscode-augment-0.497.0.vsix
    echo   %0 augment.vscode-augment-0.497.0.vsix modified_plugins
    echo.
    pause
    exit /b 1
)

set PLUGIN_PATH=%~1
set OUTPUT_DIR=%~2

if "%OUTPUT_DIR%"=="" (
    set OUTPUT_DIR=modified_plugin
)

echo 🔧 正在处理插件: %PLUGIN_PATH%
echo 📁 输出目录: %OUTPUT_DIR%
echo.

python modify_plugin.py "%PLUGIN_PATH%" -o "%OUTPUT_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ 修改完成！
    echo 📂 请查看输出目录: %OUTPUT_DIR%
) else (
    echo.
    echo ❌ 修改失败！
)

echo.
pause
