#!/bin/bash

if [[ "$#" -ne 3 ]]
then
    echo "usage: ./delete_map.sh <Proxy servicio mapas> <token> <nombre mapa>"
else
    src/client.py --Ice.Config=config/Client.config "delete" "$1" "$2" "$3"
fi
