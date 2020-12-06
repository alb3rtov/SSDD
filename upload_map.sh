#!/bin/bash

if [[ "$#" -ne 3 ]]
then
	echo "usage: ./upload_map.sh <Proxy servicio mapas> <token> <ruta archivo mapa (.JSON)>"
else
	src/client.py --Ice.Config=config/Client.config "upload" "$1" "$2" "$3"
fi
