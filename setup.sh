sudo apt update
sudo apt install -y python3 python3-pip python3-dev vlc alsa-utils
sudo pip3 install -r requirements.txt
mkdir log
touch log/debug.log && touch log/development.log && touch log/production.log && touch cronjobs.log
mv env_example .env
sudo mv cuba-school-bell.service /lib/systemd/system/cuba-school-bell.service
sudo chown -R $USER:$USER .
sudo usermod -aG audio,pulse,pulse-access $USER
sudo systemctl daemon-reload
