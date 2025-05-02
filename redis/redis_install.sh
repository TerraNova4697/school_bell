#!/bin/bash

set -e


echo "Installing redis from source..."

# Redis stable version download URL
URL="http://download.redis.io/redis-stable.tar.gz"
INSTALL_DIR="/opt/redis"
HOME_DIR=$(pwd)

echo "Downloading APT dependencies..."
sudo apt update && \
    sudo apt install make build-essential libjemalloc-dev -y
echo "APT dependencies downloaded and installed."

echo "Downloading and extracting source code..."
curl -s -o redis-stable.tar.gz $URL
sudo mkdir -p "$INSTALL_DIR"
sudo chown -R cuba:cuba "$INSTALL_DIR"
sudo tar -C "$INSTALL_DIR" -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
echo "Redis source code downloaded and extracted."

# Compile
echo "Compiling source code..."
cd "$INSTALL_DIR/redis-stable"
make 
sudo make PREFIX="$INSTALL_DIR" install
echo "Source code compiled."

echo "Setting default configurations..."
sudo echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

sudo mkdir -p /opt/redis/var
sudo chown -R cuba:cuba /opt/redis/var

sudo mkdir -p /etc/redis && sudo cp "$HOME_DIR/redis/6379.conf" /etc/redis/
echo "Default configurations set."

echo "Setting redis-server daemon..."
sudo cp "$HOME_DIR/redis/redis-server.service" /etc/systemd/system/
sudo systemctl daemon-reload
echo "Daemon is set and ready."
# systemctl start redis-server.service && \
    # sudo systemctl enable redis-server.service


echo "Redis successfully installed in $INSTALL_DIR/bin"
