#!/usr/bin/env python3

import os
import sys
import subprocess
import time
from datetime import datetime

VERSION = "1.0.0"
LAST_UPDATE = "2026-02-13"

def main():
    print(f"🤖 Termux Uptime Bot v{VERSION}")
    print(f"📅 Последнее обновление: {LAST_UPDATE}")
    print(f"🕐 Время запуска: {datetime.now()}")
    
    # Проверка обновлений при старте
    if os.environ.get('AUTO_UPDATE') == 'true':
        check_for_updates()
    
    # Запуск бота
    run_bot()

def check_for_updates():
    """Проверяет обновления на GitHub"""
    try:
        print("🔄 Проверка обновлений...")
        result = subprocess.run(['git', 'pull'], 
                              capture_output=True, text_text=True)
        if 'Already up to date' not in result.stdout:
            print("✅ Обновление установлено! Перезапуск...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            print("✅ Версия актуальна")
    except Exception as e:
        print(f"❌ Ошибка проверки обновлений: {e}")

def run_bot():
    """Запускает основную логику бота"""
    from flask import Flask, render_template_string, jsonify
    import threading
    import socket
    import re
    
    app = Flask(__name__)
    START_TIME = time.time()
    
    INDEX_HTML = '''...'''  # ваш HTML код
    
    @app.route('/')
    def index():
        return render_template_string(INDEX_HTML)
    
    @app.route('/api/uptime')
    def uptime():
        seconds = int(time.time() - START_TIME)
        return jsonify({'uptime': f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"})
    
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()