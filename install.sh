#!/bin/bash

echo "Configuring operating system for payload..."
echo "** You will be prompted for your administrator account password!"

# Update package repositories and upgrade packages
sudo apt update
sudo apt upgrade -y

# Enable i2c bus 0
grep -qxF "dtparam=i2c_arm=on" /boot/config.txt || sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt

# Install python 3.9 and pip
#wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
#tar -zxvf Python-3.9.9.tgz
#./configure --enable-optimizations
#sudo make altinstall

# Install python 3.7 (python3)
sudo apt install python3
sudo apt install python3-pip

# Disable splash screen and boot delay for faster boot
grep -qxF "boot_delay=0"     /boot/config.txt || sudo echo "boot_delay=0"     >> /boot/config.txt
grep -qxF "disable_splash=1" /boot/config.txt || sudo echo "disable_splash=1" >> /boot/config.txt

# Install python libraries/modules for sensors and hardware (systemwide)
sudo pip3 install adafruit-blinka 
sudo pip3 install adafruit-circuitpython-fram
sudo pip3 install adafruit-circuitpython-mpl115a2
sudo pip3 install adafruit-circuitpython-bme280
sudo pip3 install adafruit-circuitpython-motorkit
sudo pip3 install adafruit-circuitpython-tca9548a
sudo pip3 install adafruit-circuitpython-vl53l1x
sudo pip3 install adafruit-circuitpython-adxl34x
sudo pip3 install adafruit-extended-bus
#for the alternate camera
sudo pip3 install adafruit-circuitpython-vc0706

echo "   *** DONE ***   "