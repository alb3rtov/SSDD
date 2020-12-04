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
			#file=~/.icegauntletmaps/prueba_room.json

			mapsDir=~/.icegauntletmaps
			
			echo "Ejecutando juego..."
			
			if [[ -d $mapsDir ]] 
			then
				if [ -z "$(ls -A $mapsDir)" ]; then
					echo "No tienes ningun mapa en local, utiliza la opcion 2 para descargarte un mapa del servidor"
				else
					maps=`ls ~/.icegauntletmaps`
					echo ""
					echo "Mapas disponibles:"
					echo "$maps"
					echo ""
					echo "Introduce el nombre del mapa: "
					read map
					
					mapPath="$mapsDir/$map"
					
					icegauntlet/dungeon_local $mapPath
				fi
			else
				echo "$mapsDir no existe, utilize la segunda opcion"
			fi
			break
			;;
		getroom)
			./src/Client.py --Ice.Config=config/Client.config "$0" "$1"
			echo "Descargado mapa del servidor"
			mapas=`ls ~/.icegauntletmaps`
			echo ""
			echo "Mapas disponibles:"
			echo "$mapas"
			break
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
