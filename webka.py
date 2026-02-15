#!/usr/bin/env python3
"""
Простое веб-приложение, показывающее время работы (uptime) процесса
"""

from flask import Flask, jsonify, render_template_string
import datetime
import time
import os
import platform
import socket

app = Flask(__name__)

# Время запуска приложения (фиксируется при старте)
start_time = time.time()
start_datetime = datetime.datetime.now()

# HTML шаблон прямо в коде (для простоты)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Uptime Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            width: 100%;
            max-width: 800px;
        }
        h1 {
            text-align: center;
            margin-top: 0;
            font-size: 2.5em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 20px;
        }
        .uptime {
            font-size: 3em;
            text-align: center;
            margin: 30px 0;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .info-card {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .info-label {
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
        }
        .info-value {
            font-size: 1.2em;
            font-weight: bold;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            opacity: 0.7;
        }
        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 10px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 20px;
        }
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🕒 Uptime Monitor</h1>
        
        <div class="uptime" id="uptime">
            {{ uptime }}
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <div class="info-label">Запущено</div>
                <div class="info-value">{{ start_time_str }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Версия Python</div>
                <div class="info-value">{{ python_version }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Хост</div>
                <div class="info-value">{{ hostname }}</div>
            </div>
            <div class="info-card">
                <div class="info-label">Платформа</div>
                <div class="info-value">{{ platform }}</div>
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="refresh-btn" onclick="location.reload()">🔄 Обновить</button>
        </div>
        
        <div class="footer">
            PID: {{ pid }} | Запросов: {{ request_count }}
        </div>
    </div>
    
    <script>
        // Автообновление каждые 5 секунд
        setTimeout(() => location.reload(), 1000);
    </script>
</body>
</html>
"""

# Счетчик запросов
request_counter = 0

def format_uptime(seconds):
    """Форматирует секунды в читаемый вид"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} д")
    if hours > 0 or days > 0:
        parts.append(f"{hours} ч")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes} мин")
    parts.append(f"{seconds} сек")
    
    return " ".join(parts)

@app.route('/')
def index():
    """Главная страница с аптаймом"""
    global request_counter
    request_counter += 1
    
    current_time = time.time()
    uptime_seconds = current_time - start_time
    
    return render_template_string(
        HTML_TEMPLATE,
        uptime=format_uptime(uptime_seconds),
        start_time_str=start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        python_version=platform.python_version(),
        hostname=socket.gethostname(),
        platform=platform.platform(),
        pid=os.getpid(),
        request_count=request_counter
    )

@app.route('/api')
def api():
    """API endpoint возвращает JSON с аптаймом"""
    uptime_seconds = time.time() - start_time
    
    return jsonify({
        'uptime_seconds': uptime_seconds,
        'uptime_human': format_uptime(uptime_seconds),
        'start_time': start_datetime.isoformat(),
        'pid': os.getpid(),
        'python_version': platform.python_version(),
        'hostname': socket.gethostname()
    })

@app.route('/health')
def health():
    """Health check для мониторинга"""
    return jsonify({'status': 'ok', 'uptime': time.time() - start_time})

if __name__ == '__main__':
    print(f"🚀 Сервер запущен!")
    print(f"📡 PID: {os.getpid()}")
    print(f"🌐 Адрес: http://0.0.0.0:5000")
    print(f"📊 Uptime будет считаться с {start_datetime}")
    print(f"🔍 Для проверки API: http://0.0.0.0:5000/api")
    print(f"⏹️ Остановка: Ctrl+C")
    
    # Запускаем сервер
    app.run(host='0.0.0.0', port=5000, debug=False)
