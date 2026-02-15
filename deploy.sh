#!/bin/bash

# Цвета для красивого вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Начинаем деплой...${NC}"

# Переходим в папку проекта
cd /root/MCC/termux-test || {
    echo -e "${RED}Папка проекта не найдена!${NC}"
    exit 1
}

# Сохраняем текущую версию (на всякий случай)
git rev-parse HEAD > .previous_version

# Тянем изменения
echo -e "${GREEN}Обновляем код из GitHub...${NC}"
git pull origin main

# Устанавливаем/обновляем зависимости
echo -e "${GREEN}Устанавливаем зависимости...${NC}"
pip3 install -r requirements.txt --upgrade

# Ищем и убиваем старый процесс бота
echo -e "${GREEN}Останавливаем старого бота...${NC}"
pkill -f webka.py
sleep 2

# Запускаем нового бота через screen
echo -e "${GREEN}Запускаем нового бота...${NC}"
screen -dmS termux-bot python3 webka.py

# Проверяем, запустился ли
sleep 3
if pgrep -f webka.py > /dev/null; then
    echo -e "${GREEN}✅ Бот успешно запущен!${NC}"
    echo -e "Подключиться к боту: screen -r termux-bot"
else
    echo -e "${RED}❌ Что-то пошло не так, бот не запустился${NC}"
fi
