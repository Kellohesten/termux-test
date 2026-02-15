#!/usr/bin/env python3
"""
Маршруты для аутентификации пользователей
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

# Создаем Blueprint для маршрутов аутентификации
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    # Если пользователь уже авторизован, отправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Ищем пользователя в базе
        user = User.query.filter_by(username=username).first()
        
        # Проверяем пароль
        if not user or not user.check_password(password):
            flash('Пожалуйста, проверьте логин и пароль', 'error')
            return redirect(url_for('auth.login'))
        
        # Авторизуем пользователя
        login_user(user, remember=remember)
        flash('Вы успешно вошли!', 'success')
        
        # Перенаправляем на страницу, которую хотел посетить пользователь
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('tasks.index'))
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Валидация
        errors = []
        
        # Проверяем, существует ли пользователь
        if User.query.filter_by(username=username).first():
            errors.append('Пользователь с таким именем уже существует')
        
        if User.query.filter_by(email=email).first():
            errors.append('Пользователь с таким email уже существует')
        
        if password != password_confirm:
            errors.append('Пароли не совпадают')
        
        if len(password) < 6:
            errors.append('Пароль должен быть не менее 6 символов')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html', username=username, email=email)
        
        # Создаем нового пользователя
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))