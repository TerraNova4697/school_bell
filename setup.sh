sudo apt update
sudo apt install -y python3 python3-pip python3-dev vlc alsa-utils pulseaudio sox soxlib-fmt-all
sudo pip3 install -r requirements.txt
sudo mkdir log
sudo touch log/debug.log && sudo touch log/development.log && sudo touch log/production.log && sudo touch cronjobs.log
sudo mv env_example .env
sudo mv cuba-school-bell.service /lib/systemd/system/cuba-school-bell.service
sudo chown -R $USER:$USER .
sudo usermod -aG audio,pulse,pulse-access $USER
sudo systemctl daemon-reload