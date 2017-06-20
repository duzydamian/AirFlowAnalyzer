#!/bin/bash
#
# Skrypt wywoływany na urządzeniu
#
# Author : Damian Karbowiak
# Company: Silesian Softing
# Site   : 
#
# Date   : 08/05/2017
#

# funkcja sprawdza czy dana sciezka istenieje i zaklada ja w razie potrzeby
checkPathAndCreate() {
	if [ -d $1 ]; then
		echo "Directory: $1 exist"
	else
		echo "Directory: $1 created"
		sudo mkdir $1
	fi
}

# instalacja dodatkowego oprogramowania w systemie
sudo apt-get update
sudo apt-get install htop nano
sudo apt-get install zip unzip wget bash-completion apache2
sudo apt-get autoremove python3
sudo apt-get install python python-pip

# instalacja bibliotek python'ay
sudo pip install --upgrade pip
sudo pip install pygatt pyexpect

# utworzenie odpowiednich folderów
checkPathAndCreate /opt/ss
checkPathAndCreate /opt/ss/testo
checkPathAndCreate /opt/ss/rasp

# podmiana pliku /etc/enviroment, aby zaktualizować PATH tak, aby aplikacje były dostępne globalnie
sudo cp environment /etc/

# wywolanie skryptu wgrywajacego programowanie
./update_script.sh

# zapytanie czy uruchomić ponownie system czy pozostawić
echo "Reboot system (y/n)?"
read -p "Reboot system (y/n)?" CONT
if [ "$CONT" = "y" ]; then
	echo "REBOOT NOW"
	reboot
else
  echo "SOME CHANGES MAY BE AVAIBLE AFTER SYSTEM REBOOT";
fi
