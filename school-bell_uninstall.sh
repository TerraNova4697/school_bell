#!/bin/bash


LOG_DIR=/var/log/school_bell/

echo "Deleting school-bell app components..."
sudo rm -rf /usr/share/school_bell
echo "School Bell app components deleted."

read -p "Do you wish to delete logs: $LOG_DIR? (y/n): " ANSWER
# Удаляем пробелы и приводим к нижнему регистру
ANSWER=$(echo "$ANSWER" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
case "$ANSWER" in
    y)
        if [ -d "$LOG_DIR" ]; then
            echo "Deleting logs..."
            sudo rm -rf "$LOG_DIR"
            echo "Logs deleted."
        else
            echo "ℹ️ Папка логов не найдена: $LOG_DIR"
        fi
        ;;
    n)
        echo "Skipping logs."
        ;;
    *)
        echo "Unknown answer. Skipping logs."
        ;;
esac

echo "Stopping app services..."
sudo systemctl stop cuba-school-bell.service
sudo systemctl disable cuba-school-bell.service

sudo systemctl stop ps-killer.service
sudo systemctl disable ps-killer.service
echo "App services stopped."

echo "Deleting app services..."
sudo rm /etc/systemd/system/cuba-school-bell.service
sudo rm /etc/systemd/system/ps-killer.service
sudo systemctl daemon-reload
echo "App services deleted."


echo "School Bell App deleted."