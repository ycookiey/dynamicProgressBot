@echo off
cd /d "%~dp0"
echo Dynamic Progress Bot を起動中...
echo.
echo ログファイル: bot.log
echo 終了するには Ctrl+C を押してください
echo.
python main.py
pause