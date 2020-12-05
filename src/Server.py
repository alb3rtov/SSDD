#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import json
import os
import random
Ice.loadSlice('slice.ice')
import IceGauntlet


class Dungeon(IceGauntlet.Dungeon, Ice.Application):

    def getRoom(self, argv):

        #comprobar que hay mapas en maps/
        if (not os.listdir("maps/")):
            #print("Directory vacio, debe subir mapa")
            raise IceGauntlet.Unauthorized()
        else:
            #Elegir aleatoriamente un mapa
            for root, dirs, files in os.walk('maps/'):

                value = random.randint(0, len(files)-1)
                filename = 'maps/' + files[value]

            #print(filename)
            with open(filename) as f:
                data = json.load(f)

            return json.dumps(data)

class RoomManager(IceGauntlet.RoomManager, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        #print("token: {0}".format(token))

        if (gauntlet.isValid(token)):

            #print("El token es valido")

            filename = "tokenRoom.json"

            room_json = json.loads(roomData) #Loads file as a string
            roomName = 'maps/' + (str(room_json['room'])).replace(" ", "_") + '.json'

            #Si el archivo no existe, nuevo.
            if (not os.path.isfile(filename)):
                data = {}

                data[roomName] = token

                with open(filename, 'w') as f:
                    json.dump(data,f, indent=4)

                #Publish the .json file in maps folder
                with open(roomName, 'w') as f:
                    json.dump(room_json,f) #Dictionary to json file

                sys.stdout.flush()

            else:
                with open(filename) as file:
                    data = json.load(file)

                if roomName in data:

                    if data[roomName] == token: # eres el dueño del mapa

                        with open(roomName, 'w') as f:
                            json.dump(room_json,f)

                        #print("mapa reemplazado")
                        sys.stdout.flush()

                    else: # no eres el dueño del mapa
                        #print('RoomAlreadyExists')
                        raise IceGauntlet.RoomAlreadyExists()
                else:
                    data[roomName] = token

                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=4)

                    with open(roomName, 'w') as f:
                        json.dump(room_json,f)

                    sys.stdout.flush()

        else:
            raise IceGauntlet.Unauthorized()
            #print("El token es no es valido")
    def remove(self, token, roomName, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        #print("token: {0}".format(token))

        if (gauntlet.isValid(token)):
        	filename = "tokenRoom.json"
        	with open(filename) as json_file:
        		data = json.load(json_file)
        		for element in data:
        			if roomName in data:
        				del element[roomName]
        	with open(filename, 'w') as json_file:
        		data = json.dump(data, json_file)

class Server(Ice.Application):
    def run(self, argv):
        RMbroker = self.communicator()
        RMservant = RoomManager()

        RMadapter = RMbroker.createObjectAdapter("RoomManagerAdapter")
        RMproxy = RMadapter.add(RMservant, RMbroker.stringToIdentity("RoomManager"))

        print(RMproxy, flush = True)

        Dbroker = self.communicator()
        Dservant = Dungeon()

        Dadapter = Dbroker.createObjectAdapter("DungeonAdapter")
        Dproxy = Dadapter.add(Dservant, Dbroker.stringToIdentity("Dungeon"))

        os.system("echo '" + str(Dproxy) + "' | tee config/game-proxy.out > /dev/null")

        RMadapter.activate()
        Dadapter.activate()

        self.shutdownOnInterrupt()

        RMbroker.waitForShutdown()
        Dbroker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
