#!/bin/bash


set -e

if dpkg -l | grep -q redis-server; then
    echo "Удаление Redis, установленного через APT..."
    sudo systemctl stop redis-server || true
    sudo apt purge -y redis-server redis-tools
    sudo apt autoremove -y
    echo "APT-установка Redis удалена"
else
    echo "ℹ️ Redis не установлен через APT"
fi

if [ -d "/opt/redis" ]; then
    echo "Удаление Redis, установленного из исходников"
    sudo systemctl stop redis-server.service 2>/dev/null || true
    sudo systemctl disable redis-server.service 2>/dev/null || true
    sudo rm -f /etc/systemd/system/redis-server.service
    sudo systemctl daemon-reload

    sudo rm -rf /opt/redis
    echo "Удалена ручная установка Redis из /opt/redis"
else
    echo "Ручная установка Redis в /opt/redis не найдена"
fi

echo "Удаление завершено."
