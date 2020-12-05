#!/bin/bash

if [ "$#" -ne 1 ]
then
	echo "usage: ./run_game.sh <Proxy servicio mapas>"
else
	./icegauntlet/dungeon_remote --Ice.Config=config/Client.config --proxy "$1"
fi
