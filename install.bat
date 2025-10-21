@echo off
echo Создание виртуального окружения...
python -m venv venv

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install --upgrade pip
pip install -r requirements.txt

echo Установка завершена!
echo Для запуска используйте run.bat
pause
