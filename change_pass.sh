#!/bin/bash

if [[ "$#" -ne 1 ]]
then
	echo "usage: ./change_pass.sh <Proxy servicio autenticacion>"
else
	./src/client.py --Ice.Config=config/Client.config "changepass" "$1"
fi
