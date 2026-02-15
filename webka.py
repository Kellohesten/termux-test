#!/usr/bin/env python3

"""
Telegram Uptime Bot for Termux
Отвечает на вопрос, сколько работает
"""

import telebot
import time
from datetime import datetime
import os
import sys

# ============= НАСТРОЙКИ =============
TOKEN = "8366731711:AAHl4NHWDoJ8xUTvEFv1JOEd1J0dA2kzIg8"  # Вставь свой токен от @BotFather

# Время запуска бота
START_TIME = time.time()
START_DATETIME = datetime.now()

bot = telebot.TeleBot(TOKEN)

# ============= ФУНКЦИИ =============
def get_uptime():
    """Возвращает отформатированное время работы"""
    seconds = int(time.time() - START_TIME)
    
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if days > 0:
        return f"{days}д {hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

# ============= ОБРАБОТЧИКИ КОМАНД =============
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Приветственное сообщение"""
    welcome_text = """
🤖 *Telegram Uptime Bot*

Я простой бот, который считает, сколько времени прошло с моего запуска.

*Команды:*
/uptime — сколько я работаю TEST
/time — то же самое
/start — это сообщение

*Или просто спроси:* "сколько работаешь?"
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['uptime', 'time'])
def send_uptime(message):
    """Отправляет аптайм"""
    uptime = get_uptime()
    response = f"""
⏱ *Бот работает:* {uptime}

🕐 Запущен: {START_DATETIME.strftime('%d.%m.%Y %H:%M:%S')}
    """
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработка текстовых сообщений"""
    text = message.text.lower()
    
    # Отвечаем на вопросы о времени работы
    if any(word in text for word in ['сколько', 'работаешь', 'работает', 'запущен', 'время', 'uptime', 'аптайм']):
        uptime = get_uptime()
        response = f"""
Я работаю уже *{uptime}* 🕐

Запустился: {START_DATETIME.strftime('%d.%m.%Y %H:%M:%S')}
        """
        bot.reply_to(message, response, parse_mode='Markdown')
    
    # Отвечаем на приветствия
    elif any(word in text for word in ['привет', 'здравствуй', 'хай', 'hello', 'hi', 'прив']):
        bot.reply_to(message, "Привет! 👋\nУзнай мой аптайм — /uptime")
    
    # На всё остальное
    else:
        bot.reply_to(message, "Напиши /uptime чтобы узнать, сколько я работаю")

# ============= ЗАПУСК =============
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🤖 TELEGRAM UPTIME BOT")
    print("="*50)
    print(f"\n📅 Запущен: {START_DATETIME.strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"🆔 Бот: @{bot.user.username if bot.user else '...'}")
    print(f"\n🚀 Бот работает! Нажми Ctrl+C для остановки")
    print("="*50 + "\n")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
        print(f"⏱ Всего проработал: {get_uptime()}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
