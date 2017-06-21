#!/bin/bash
#
# Skrypt wywoływany na urządzeniu
#
# Author : Damian Karbowiak
# Company: Silesian Softing.
# Site   : 
#
# Date   : 08/05/2017
#

# instalacja bibliotek python'a z plikow egg
echo "Usuwanie starych bibliotek Python'a"
sudo pip uninstall -y ss-afa-tc
echo "Instalacja nowych bibliotek Python'a"
sudo easy_install testo/lib/*

# backup konfiguracji
#cp /opt/ss/testo/config.cfg testo/config.cfg

# czyszczenie lokalizacji docelowych
rm /var/www/html/* -R
rm /opt/ss/testo/* -R
rm /opt/ss/rasp/* -R

# kopiowanie nowych plików
cp html/* /var/www/html/ -R
cp testo/* /opt/ss/testo/
cp rasp/* /opt/ss/rasp/

# linkowanie dla przedniej kamery
ln -s /tmp/ss-afa/current/temp_datetime.data /var/www/html/testo/temp_datetime
ln -s /tmp/ss-afa/current/temp_value.data /var/www/html/testo/temp_value
ln -s /tmp/ss-afa/current/velo_datetime.data /var/www/html/testo/velo_datetime
ln -s /tmp/ss-afa/current/velo_value.data /var/www/html/testo/velo_value
ln -s /tmp/ss-afa/current/bat_datetime.data /var/www/html/testo/bat_datetime
ln -s /tmp/ss-afa/current/bat_value.data /var/www/html/testo/bat_value
ln -s /tmp/ss-afa/current/status.data /var/www/html/testo/status

# linkowanie dla diagnostyki
ln -s /tmp/ss-afa/rasp/datetime.data /var/www/html/rasp/datetime
ln -s /tmp/ss-afa/rasp/temperature.data /var/www/html/rasp/temperature
ln -s /tmp/ss-afa/rasp/freq.data /var/www/html/rasp/freq
ln -s /tmp/ss-afa/rasp/ip.data /var/www/html/rasp/ip
ln -s /tmp/ss-afa/rasp/users.data /var/www/html/rasp/users
ln -s /tmp/ss-afa/rasp/ram.data /var/www/html/rasp/ram
ln -s /tmp/ss-afa/rasp/df.data /var/www/html/rasp/df
ln -s /tmp/ss-afa/rasp/uptime.data /var/www/html/rasp/uptime
ln -s /tmp/ss-afa/rasp/ps_py.data /var/www/html/rasp/ps_py
