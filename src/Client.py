#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import getpass
import json
import os
Ice.loadSlice('slice.ice')
import IceGauntlet

class RoomToolClient(Ice.Application):
    
    def getRoom(self, argv):
        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.GamePrx.checkedCast(proxy)

        if not gauntlet:
            raise RumTimeError('Invalid proxy')

        roomData = gauntlet.getRoom()
        
        room_json = json.loads(roomData)
        
        home = os.path.expanduser("~")
        path = home + '/.icegauntletmaps'
 
        if (not os.path.isdir(path)):
            os.system('mkdir ' + path)

        roomName = path + '/' + (str(room_json['room'])).replace(" ", "_") + '.json'

        with open(roomName, 'w') as f:
            json.dump(room_json,f)
    
        return 0
    
    def getNewToken(self, argv):
        proxy = self.communicator().stringToProxy(argv[3])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        
        return gauntlet.getNewToken(username, password)
        

class Client(Ice.Application):

    def run (self, argv):
        if (argv[1] == './upload_map.sh'):
            proxy = self.communicator().stringToProxy(argv[2])
            gauntlet = IceGauntlet.MapManagingPrx.checkedCast(proxy)
           
            if not gauntlet:
                raise RunTimeError('Invalid proxy')

            with open (argv[4]) as f:
                data = json.load(f)

            gauntlet.publish(argv[3], json.dumps(data))
        else:
            print("otro")

        
        #roomToolClient = RoomToolClient()
        #proxy = self.communicator().stringToProxy(argv[1])
        #gauntlet = IceGauntlet.MapManagingPrx.checkedCast(proxy)

        #if not gauntlet:
        #    raise RunTimeError('Invalid proxy')

        #token = roomToolClient.getNewToken(argv) 
        #print(token) #DEBUG 
        
        #roomData = input("Enter roomData (Path of JSON file): ");
        
        #with open(roomData) as f:
        #    data = json.load(f)
    
        #gauntlet.publish(token, json.dumps(data))
         
        #roomToolClient.getRoom(argv)

        return 0

sys.exit(Client().main(sys.argv))

