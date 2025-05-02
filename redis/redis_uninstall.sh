#!/bin/bash


set -e

DAEMON_FILE=/etc/systemd/system/redis-server.service
CONF_DIR=/etc/redis
SOURCE_DIR=/opt/redis

echo "Stopping Redis service..."
if systemctl list-unit-files | grep -q '^redis-server.service'; then
    sudo systemctl stop redis-server.service
    sudo systemctl disable redis-server.service
    echo "Stopped Redis service."
else
    echo "Redis service not found. Skipping stop/disable."
fi

echo "Deleting redis daemon..."
if [ -f "$DAEMON_FILE" ]; then
    sudo rm /etc/systemd/system/redis-server-service
    sudo systemctl daemon-reload
    echo "Redis daemon deleted."
else 
    echo "Unit file not found. Skipping service file removing."
fi

echo "Deleting Redis installation & conf dirs..."
if [ -d "$CONF_DIR" ]; then
    sudo rm -rf /opt/redis
fi

if [ -d "$SOURCE_DIR" ]; then
    sudo rm -rf /etc/redis
fi
echo "Deleted Redis installation dir."

echo "Redis successfully uninstalled."
