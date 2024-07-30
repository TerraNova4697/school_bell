sudo apt update
sudo apt install -y python3 python3-pip python3-dev
sudo pip3 install -r requirements.txt
sudo mv cuba-school-bell.service /lib/systemd/system/cuba-school-bell.service
mv env_example .env
sudo systemctl daemon-reload