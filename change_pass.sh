#!/bin/bash

if [[ "$#" -ne 1 ]]
then
	echo "usage: ./change_pass.sh <Proxy servicio autenticacion>"
else
	./src/Client.py --Ice.Config=config/Client.config "changepass" "$1"
fi
