#!/bin/bash

set -e

mv evn_example .env

sudo mkdir -p /usr/share/school_bell && sudo chown -R cuba:cuba /usr/share/school_bell
sudo mkdir -p /var/log/school_bell && sudo chown -R cuba:cuba /var/log/school_bell

sudo apt update && sudo apt install python3-pip python3.12-venv vlc \
    libvlc-dev python3-vlc alsa-utils pulseaudio sox libsox-fmt-all

cp defaultAudio.mp3 /usr/share/school_bell/startLessonAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/endLessonAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/alarmAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/fireAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/ambulanceAudio.mp3
cp defaultAudio.mp3 /usr/share/school_bell/testAudio.mp3

python3 -m venv .venv && \
    .venv/bin/pip install -r requirements.txt


sudo cp cuba-school-bell.service /etc/systemd/system
sudo cp ps_killer/ps-killer.service /etc/systemd/system
sudo systemctl daemon-reload
