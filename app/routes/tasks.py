#!/usr/bin/env python3
"""
Маршруты для работы с задачами
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Task
from datetime import datetime

# Создаем Blueprint для маршрутов задач
tasks_bp = Blueprint('tasks', __name__, template_folder='../templates/tasks')

@tasks_bp.route('/')
@login_required
def index():
    """Главная страница со списком задач"""
    # Получаем все задачи текущего пользователя
    tasks = current_user.tasks.order_by(Task.created_at.desc()).all()
    
    # Разделяем на выполненные и невыполненные
    active_tasks = [t for t in tasks if not t.completed]
    completed_tasks = [t for t in tasks if t.completed]
    
    return render_template('index.html', 
                         active_tasks=active_tasks,
                         completed_tasks=completed_tasks,
                         now=datetime.now())

@tasks_bp.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    """Добавление новой задачи"""
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        flash('Название задачи не может быть пустым', 'error')
        return redirect(url_for('tasks.index'))
    
    # Создаем новую задачу
    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    flash('Задача успешно добавлена', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    """Отметить задачу как выполненную/невыполненную"""
    task = Task.query.get_or_404(task_id)
    
    # Проверяем, что задача принадлежит текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет прав на это действие', 'error')
        return redirect(url_for('tasks.index'))
    
    task.completed = not task.completed
    db.session.commit()
    
    status = 'выполнена' if task.completed else 'возобновлена'
    flash(f'Задача "{task.title}" отмечена как {status}', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    """Удаление задачи"""
    task = Task.query.get_or_404(task_id)
    
    # Проверяем, что задача принадлежит текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет прав на это действие', 'error')
        return redirect(url_for('tasks.index'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash(f'Задача "{task.title}" удалена', 'info')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['POST'])
@login_required
def edit_task(task_id):
    """Редактирование задачи"""
    task = Task.query.get_or_404(task_id)
    
    # Проверяем, что задача принадлежит текущему пользователю
    if task.user_id != current_user.id:
        flash('У вас нет прав на это действие', 'error')
        return redirect(url_for('tasks.index'))
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        flash('Название задачи не может быть пустым', 'error')
        return redirect(url_for('tasks.index'))
    
    task.title = title
    task.description = description
    db.session.commit()
    
    flash('Задача обновлена', 'success')
    return redirect(url_for('tasks.index'))

# API endpoints для AJAX-запросов (на будущее)
@tasks_bp.route('/api/tasks')
@login_required
def api_get_tasks():
    """API: получить все задачи пользователя в JSON"""
    tasks = current_user.tasks.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def api_add_task():
    """API: добавить задачу через JSON"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=current_user.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201