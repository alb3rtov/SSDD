#!/bin/bash

if [[ "$#" -ne 3 ]]
then
	echo "usage: ./upload_map.sh <Proxy servicio mapas> <token> <ruta archivo mapa (.JSON)>"
else
	src/Client.py --Ice.Config=config/Client.config "$0" "$1" "$2" "$3"
fi
