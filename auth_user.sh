#!/bin/bash

if [[ "$#" -ne 1 ]]
then
	echo "usage: ./auth_user.sh <Proxy servicio autenticacion>"
else
	./src/Client.py --Ice.Config=config/Client.config "$0" "$1"
fi
