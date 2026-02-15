#!/usr/bin/env python3
"""
Инициализация Flask приложения
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Импортируем модели и db из отдельного файла
from app.models import db, User

# Создаем объекты расширений
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    """Фабрика приложения"""
    
    # Создаем экземпляр Flask
    app = Flask(__name__, 
                instance_path=os.path.join(os.path.dirname(__file__), '..', 'instance'),
                instance_relative_config=True)
    
    # Загружаем конфигурацию
    from config import config
    app.config.from_object(config[config_name])
    
    # Создаем instance папку, если её нет
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Инициализируем расширения с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Настройки Flask-Login
    login_manager.login_view = 'auth.login'  # куда редиректить неавторизованных
    login_manager.login_message = 'Пожалуйста, войдите чтобы увидеть эту страницу'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Регистрируем blueprints (маршруты)
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/')
    
    # Создаем таблицы БД при первом запуске (для разработки)
    with app.app_context():
        db.create_all()
        
        # Создаем тестового пользователя, если БД пустая (только для разработки)
        if User.query.count() == 0 and app.config.get('DEBUG', False):
            test_user = User(username='test', email='test@example.com')
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print('✅ Создан тестовый пользователь: test / test123')
    
    return app