#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "usage: ./run_map_server.sh <Proxy servicio autenticacion>"
else
	mkdir -p /tmp/db/registry
	icegridregistry --Ice.Config=config/node1.config &
	./src/server.py --Ice.Config=config/Server.config "$1"
fi
