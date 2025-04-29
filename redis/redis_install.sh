#!/bin/bash

set -e


# Redis stable version download URL
URL="http://download.redis.io/redis-stable.tar.gz"
INSTALL_DIR="/opt/redis"

curl -s -o redis-stable.tar.gz $URL
sudo mkdir -p "$INSTALL_DIR"
sudo chown -R cuba:cuba "$INSTALL_DIR"
sudo tar -C "$INSTALL_DIR" -xzf redis-stable.tar.gz
rm redis-stable.tar.gz

# Compile
cd "$INSTALL_DIR/redis-stable"
make 
sudo make PREFIX="$INSTALL_DIR" install

sudo echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

sudo mkdir -p /opt/redis/var
sudo chown -R cuba:cuba /opt/redis/var

sudo mkdir -p /etc/redis && sudo cp 6379.conf /etc/redis/
sudo cp redis-server.service /etc/systemd/system/
sudo systemctl daemon-reload
# systemctl start redis-server.service && \
    # sudo systemctl enable redis-server.service


echo "Redis установлен в $INSTALL_DIR/bin"
