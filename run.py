#!/usr/bin/env python3
"""
Точка входа для запуска приложения
"""

from app import create_app
import os

# Создаем приложение (по умолчанию development режим)
app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    print(f"🚀 Запуск приложения...")
    print(f"📁 База данных: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"🌐 Открой в браузере: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)