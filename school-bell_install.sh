#!/bin/bash

set -e

echo "Installing School Bell app..."
cp env_example .env

sudo mkdir -p /usr/share/school_bell && sudo chown -R cuba:cuba /usr/share/school_bell
sudo mkdir -p /var/log/school_bell && sudo chown -R cuba:cuba /var/log/school_bell

echo "Downloading apt dependencies..."
sudo apt update && sudo apt install python3-pip python3.12-venv vlc \
    libvlc-dev python3-vlc alsa-utils pulseaudio sox libsox-fmt-all -y

# Set default audiofiles
cp defaultAudio.mp3 /usr/share/school_bell/startLessonAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/endLessonAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/alarmAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/fireAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/ambulanceAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/testAudio.mp3

echo "Downloading python dependencies..."
python3 -m venv .venv && \
    .venv/bin/pip install -r requirements.txt

echo "Setting daemons..."
sudo cp cuba-school-bell.service /etc/systemd/system
sudo cp ps_killer/ps-killer.service /etc/systemd/system
sudo systemctl daemon-reload

sudo timedatectl set-timezone Asia/Almaty

echo "School Bell installed."
echo "Don't forget to set your ENV in .env file."
