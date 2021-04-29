#!/bin/bash

sudo apt update
sudo apt upgrade
sudo apt install libpq5
sudo apt install libgpiod2
pip3 install -r /home/pi/RP_sensor/Requirements/requirements.txt

mkdir /home/pi/.config/autostart
cp /home/pi/RP_sensor/Requirements/xyz.desktop /home/pi/.config/autostart/