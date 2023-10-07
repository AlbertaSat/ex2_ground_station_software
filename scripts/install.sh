#!/bin/bash

sudo apt remove cmdtest
sudo apt remove yarn

#install curl if not present
which curl &> /dev/null || sudo apt install curl

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update
sudo apt-get install yarn -y
sudo apt-get install expect
pip install pyserial
pip install numpy
pip install zmq
