sudo apt update
sudo apt install -y python3 python3-pip python3-dev
sudo pip3 install -r requirements.txt
touch log/debug.log && touch log/development.log && touch log/production.log && touch cronjobs.log
mv env_example .env
sudo mv cuba-school-bell.service /lib/systemd/system/cuba-school-bell.service
sudo systemctl daemon-reload