#!/bin/bash
#
# Testo
# Skrypt aktualizuje katalogi install/update, a następnie je archiwizuje
# Następnie zależnie od parametru wysyła do urządzenia i wykonuje procees instalacji lub aktualizacji
#
# Author : Damian Karbowiak
# Company: Silesian Softing
# Site   : 
#
# Date   : 08/05/2017
#

# ABY WYELIMINOWAĆ POTRZEBĘ KLEPANIA HASŁA ZA KAŻDYM RAZEM TRZEBA 
# WYWOŁAĆ ODPOWIEDNIE KOMENDY, 192.168.94.25 IP DOCELOWE
# ssh-keygen
# ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.94.25
# ABY PRZETESTOWAĆ:
# ssh pi@192.168.94.25

# funkcja sprawdza czy dana sciezka istenieje i zaklada ja w razie potrzeby
checkPathAndCreate() {
	if [ -d $1 ]; then
		echo "Directory: $1 exist"
		return 0
	else
		echo "Directory: $1 created"
		mkdir $1
		return 1
	fi
}

# funkcja wstawia ifnormacje o wersji i rewizji do odpowiednich plików
insertDataToHtml() {
	sed -i 's/'$1'/'$2'/g' ss-afa/html/index.html
	sed -i 's/'$1'/'$2'/g' ss-afa/html/testo/index.html
	sed -i 's/'$1'/'$2'/g' ss-afa/html/rasp/index.html
}

u=false
i=false
l=false
c=false
ipf=false
portf=false
ip_default=192.168.1.100
port_default=22
revision=$(git rev-list --count HEAD)
#revision=1
version=1.0

if [ "$#" -gt 0 ]; then
	for arg in "$@"; 
	do 
		case "$arg" in
		-u)    c=true; u=true;;
		-i)    c=true; i=true;;
		-l)    l=true;;
		-c)    c=true;;
		-ip*)  ipf=true ip_arg=${arg##*ip};;
		-p*)   portf=true port_arg=${arg##*p};;
		esac
	done
else
	echo "No parameters"
	echo "Supported parameters are:"
	echo -e "-i\t\t-\t Install software on odroid"
	echo -e "-u\t\t-\t Update software on odroid"
	echo -e "-c\t\t-\t Create update archive"
	echo -e "-l\t\t-\t Update on local machine"
	echo -e "-ip x.x.x.x\t-\t Set x.x.x.x IP for update/install"
	echo -e "-p x\t-\t Set x port for update/install"
fi

if $ipf; then
	ip=$ip_arg
else
	ip=$ip_default
fi

if $portf; then
	port=$port_arg
else
	port=$port_default
fi

if $c; then
	echo "Clean dest folder"	
	if checkPathAndCreate ss-afa; then
		rm ss-afa/* -R
	fi

	echo "Compiling programs"
	echo "PYTHON"
	#cd nav/*/src; pwd; python setup.py bdist_egg --exclude-source-files; cd ../../..
	cd testo-concentrator/src; python setup.py bdist_egg --exclude-source-files --version $version.$revision; cd ../..

	echo "Copy required files"
	cp install_script.sh update_script.sh environment ss-afa/
	cp html ss-afa/ -R
	insertDataToHtml 'vvv' $version
	insertDataToHtml 'rrr' $revision
	checkPathAndCreate ss-afa/testo
	checkPathAndCreate ss-afa/testo/lib
	checkPathAndCreate ss-afa/rasp

	cp testo-concentrator/src/Testo* ss-afa/testo/ -v
	cp testo-concentrator/src/dist/* ss-afa/testo/lib/ -v
	cp rasp/* ss-afa/rasp/ -v

	echo "Create archive"
	rm ss-afa.zip
	zip -rq ss-afa.zip ss-afa
fi

if $i; then
	echo "Copy new software to rasp:" $ip -P$port
	scp -P$port ss-afa.zip pi@$ip:ss-afa.zip
	echo "Install software on rasp:" $ip -P$port
	ssh -p$port pi@$ip "rm ss-afa -R; unzip -q ss-afa.zip; cd ss-afa; ./install_script.sh"	
fi

if $u; then
	echo "Copy new software to rasps:" $ip-P$port
	scp -P$port ss-afa.zip pi@$ip:ss-afa.zip
	echo "Update oftware on rasp:" $ip -P$port
	ssh -p$port pi@$ip "rm ss-afa -R; unzip -q ss-afa.zip; cd ss-afa; ./update_script.sh"
fi

echo "FINISH"
