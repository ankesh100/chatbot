sudo service botserver restart
sudo kill -9 $(sudo lsof -t -i:3000)
sleep 70s
sudo service botserver restart
sudo service SimpleBot restart

