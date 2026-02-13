#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Установка Termux Uptime Bot"

# Обновление пакетов
pkg update && pkg upgrade -y

# Установка необходимых пакетов
pkg install -y python git openssh termux-api

# Установка Python библиотек
pip install flask pyTelegramBotAPI requests python-telegram-bot

# Генерация SSH ключа для CI/CD
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
    echo -e "\n🔑 Ваш ПУБЛИЧНЫЙ ключ (добавьте в GitHub Secrets):\n"
    cat ~/.ssh/id_rsa.pub
fi

# Создание скрипта автозапуска
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-uptime-bot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/termux-uptime-bot
git pull
python webka.py &
EOF

chmod +x ~/.termux/boot/start-uptime-bot.sh

echo "✅ Установка завершена!"
echo "📱 Локальный доступ: http://localhost:5000"