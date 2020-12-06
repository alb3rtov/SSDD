#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import json
import os
import random
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

FILE_TOKEN_ROOM = "tokenRoom.json" 
JSON_EXTENSION = ".json"
MAPS_PATH = "maps/"

class Dungeon(IceGauntlet.Dungeon, Ice.Application):

    def getRoom(self, argv):
        
        #comprobar que hay mapas en maps/
        
        if (not os.listdir(MAPS_PATH) or len(os.listdir(MAPS_PATH)) == 1):
            raise IceGauntlet.RoomNotExists()
        else:
            #Elegir aleatoriamente un mapa
            for root, dirs, files in os.walk(MAPS_PATH):
                
                #Evitar que eliga el archivo .gitignore
                value = random.randint(0, len(files)-1)
                while (files[value] == ".gitignore"):
                    value = random.randint(0, len(files)-1)
                
                filename = MAPS_PATH + files[value]
            
            with open(filename) as f:
                data = json.load(f)

            return json.dumps(data)

class RoomManager(IceGauntlet.RoomManager, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        if (gauntlet.isValid(token)):

            room_json = json.loads(roomData) #Loads file as a string
            roomName = MAPS_PATH + (str(room_json['room'])).replace(" ", "_") + JSON_EXTENSION
            #Si el archivo no existe, nuevo.
            if (not os.path.isfile(FILE_TOKEN_ROOM)):
                data = {}

                data[roomName] = token

                with open(FILE_TOKEN_ROOM, 'w') as f:
                    json.dump(data,f, indent=4)

                #Publish the .json file in maps folder
                with open(roomName, 'w') as f:
                    json.dump(room_json,f) #Dictionary to json file

            else:
                with open(FILE_TOKEN_ROOM) as file:
                    data = json.load(file)

                if roomName in data:
                    if data[roomName] == token: # eres el dueño del mapa
                        with open(roomName, 'w') as f:
                            json.dump(room_json,f)

                    else: # no eres el dueño del mapa
                        raise IceGauntlet.RoomAlreadyExists()
                else:
                    data[roomName] = token

                    with open(FILE_TOKEN_ROOM, 'w') as f:
                        json.dump(data, f, indent=4)

                    with open(roomName, 'w') as f:
                        json.dump(room_json,f)

        else:
            raise IceGauntlet.Unauthorized()
    
    def remove(self, token, roomName, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)
        
        isOwner = False

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        if (gauntlet.isValid(token)):
            #filename = "tokenRoom.json"
           
            fullRoomName = MAPS_PATH + roomName.replace(" ", "_") + JSON_EXTENSION
            
            with open(FILE_TOKEN_ROOM, "r") as f:
                lines = f.readlines()

            with open(FILE_TOKEN_ROOM, "w") as f:
                
                for line in lines:    
                    if not (fullRoomName in line and token in line):
                        f.write(line)
                    else:
                        isOwner = True
                        os.system('rm ' + fullRoomName)
            
            if (not isOwner):
                raise IceGauntlet.Unauthorized()

            if (os.stat(FILE_TOKEN_ROOM).st_size <= 3):
                os.system('rm ' + FILE_TOKEN_ROOM)
    
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
