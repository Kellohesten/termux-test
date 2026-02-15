#!/usr/bin/env python3
"""
Конфигурация приложения
Настройки загружаются из переменных окружения или файла .env
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Config:
    """Базовый класс конфигурации"""
    
    # Секретный ключ для сессий
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Настройки базы данных
    # Приоритет: переменная окружения -> локальная БД в instance
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Папка для instance-specific данных
    INSTANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    # В разработке можно использовать локальную БД в папке проекта
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev.db')

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    # В продакшене ожидаем DATABASE_URL из окружения
    pass

# Выбираем конфигурацию в зависимости от окружения
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}