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
            print("Directory vacio, debe subir mapa")
        else:
            #Elegir aleatoriamente un mapa
            for root, dirs, files in os.walk('maps/'):
                
                value = random.randint(0, len(files)-1)
                filename = 'maps/' + files[value]

            print(filename)
            with open(filename) as f:
                data = json.load(f)
            
            return json.dumps(data)

class RoomManager(IceGauntlet.RoomManager, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)
        
        if not gauntlet:
            raise RunTimeError('Invalid proxy')
    
        print("token: {0}".format(token))
  
        if (gauntlet.isValid(token)):

            print("El token es valido")

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
                            
                        print("mapa reemplazado")
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
            print("El token es no es valido")
            
class Server(Ice.Application):
    def run(self, argv):
        MMbroker = self.communicator()
        MMservant = RoomManager()
        
        MMadapter = MMbroker.createObjectAdapter("MMAdapter")
        MMproxy = MMadapter.add(MMservant, MMbroker.stringToIdentity("mapmanaging1"))

        print(MMproxy, flush = True)

        Gbroker = self.communicator()
        Gservant = Dungeon()
        
        Gadapter = Gbroker.createObjectAdapter("GameAdapter")
        Gproxy = Gadapter.add(Gservant, Gbroker.stringToIdentity("game1"))

        print(Gproxy, flush = True)
    
        MMadapter.activate()
        Gadapter.activate()
        
        self.shutdownOnInterrupt()
        
        MMbroker.waitForShutdown()
        Gbroker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
