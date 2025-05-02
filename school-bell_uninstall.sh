#!/bin/bash


LOG_DIR=/var/log/school_bell/

echo "Deleting school-bell app components..."
sudo rm -rf /usr/share/school_bell

for arg in "$@"; do
    if [ "$arg" == "--logs" ]; then
        echo "Deleting logs from $LOG_DIR..."
        if [ -d "$LOG_DIR" ]; then
            sudo rm -rf $LOG_DIR
            echo "Logs deleted."
        fi
        break
    fi
done

echo "Stopping app services..."
sudo systemctl stop cuba-school-bell.service
sudo systemctl disable cuba-school-bell.service

sudo systemctl stop ps-killer.service
sudo systemctl disable ps-killer.service

echo "Deleting app services..."
sudo rm /etc/systemd/system/cuba-school-bell.service
sudo rm /etc/systemd/system/ps-killer.service
sudo systemctl daemon-reload

echo "School Bell App deleted."