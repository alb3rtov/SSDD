#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "usage: ./run_game.sh <Proxy servicio mapas>"
else

PS3='Elige una opcion: '	
echo "Menu Juego IceGautlet"
select opt in jugar getroom salir; do

	case $opt in
		jugar)
			file=~/.icegautletmaps/prueba_room.json
			echo "Ejecutando juego..."
			if test -f "$file"; then
				icegautlet/dungeon_local $file
			else
				echo "$file no existe, utilize la segunda opcion"
			fi
			;;
		getroom)
			echo "Descargar room del servidor de mapas"
			./src/Client.py --Ice.Config=config/Client.config "getroom" "$1"	
			;;
		salir)
			break
			;;
		*)
			echo "Invalid option $REPLY"
			;;
	esac
done
fi
