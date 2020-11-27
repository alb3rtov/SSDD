#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import json
Ice.loadSlice('slice.ice')
import IceGauntlet


class Game(IceGauntlet.Game, Ice.Application):
    
    def getRoom(self, argv):
        with open('maps/prueba_room.json') as f:
            data = json.load(f)

        return json.dumps(data)


class MapManaging(IceGauntlet.MapManaging, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)
        
        if not gauntlet:
            raise RunTimeError('Invalid proxy')
    
        print("token: {0}".format(token))
   
        if (gauntlet.isValid(token)):
            print("El token es valido")
            
            room_json = json.loads(roomData) #Loads file as a string
            roomName = 'maps/' + (str(room_json['room'])).replace(" ", "_") + '.json'
            
            #Publish the .json file in maps folder
            with open(roomName, 'w') as f:
                json.dump(room_json,f) #Dictionary to json file
            
            sys.stdout.flush() 
        
        else:
            print("El token es no es valido")
            
class Server(Ice.Application):
    def run(self, argv):
        MMbroker = self.communicator()
        MMservant = MapManaging()
        
        MMadapter = MMbroker.createObjectAdapter("MMAdapter")
        MMproxy = MMadapter.add(MMservant, MMbroker.stringToIdentity("mapmanaging1"))

        print(MMproxy, flush = True)

        Gbroker = self.communicator()
        Gservant = Game()
        
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
