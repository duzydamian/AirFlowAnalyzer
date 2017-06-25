#!/bin/bash
#
# Script executed on device
#
# Author : Damian Karbowiak
# Company: Silesian Softing
# Site   : 
#
# Date   : 08/05/2017
#

# function checks if given path exist and create if necessary
checkPathAndCreate() {
	if [ -d $1 ]; then
		echo "Directory: $1 exist"
	else
		echo "Directory: $1 created"
		sudo mkdir $1
	fi
}

# instalation extra software in system
sudo apt-get update
sudo apt-get install htop nano
sudo apt-get install zip unzip wget bash-completion apache2
sudo apt-get autoremove python3
sudo apt-get install python python-pip

# instalation python libs
sudo pip install --upgrade pip
sudo pip install pygatt pyexpect

# create directories
checkPathAndCreate /opt/ss
checkPathAndCreate /opt/ss/testo
checkPathAndCreate /opt/ss/rasp

# replace /etc/enviroment file to update PATH to be able to execute programs global
# sudo cp environment /etc/

# execution script to install software
./update_script.sh

# asking if reboot system after instlation
echo "Reboot system (y/n)?"
read -p "Reboot system (y/n)?" CONT
if [ "$CONT" = "y" ]; then
	echo "REBOOT NOW"
	reboot
else
  echo "SOME CHANGES MAY BE AVAIBLE AFTER SYSTEM REBOOT";
fi