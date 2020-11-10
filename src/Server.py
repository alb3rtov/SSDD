#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import json
Ice.loadSlice('src/slice.ice')
import IceGauntlet

class MapManaging(IceGauntlet.MapManaging, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')
    
        print("token: {0}".format(token))
   
        if (gauntlet.isValid(token)):
            print("El token es valido")
        else:
            print("El token es no es valido")
            
        #print(type(roomData)) # DEBUG
        
        #print(type(json.loads(roomData))) #DEBUG
               
        room_json = json.loads(roomData)

        roomName = 'maps/' + (str(room_json['room'])).replace(" ", "_") + '.json'
        #print(roomName)
        
        #Publish the .json file in maps folder
        with open(roomName, 'w') as f:
            json.dump(room_json,f)

        sys.stdout.flush()

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = MapManaging()
        
        adapter = broker.createObjectAdapter("MMAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("mapmanaging1"))

        print(proxy, flush = True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
