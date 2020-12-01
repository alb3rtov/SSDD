#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import getpass
import json
import os
import hashlib
Ice.loadSlice('slice.ice')
import IceGauntlet

class GameToolClient(Ice.Application):
    
    def getRoom(self, argv):
        
        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.DungeonPrx.checkedCast(proxy)
        
        if not gauntlet:
            raise RumTimeError('Invalid proxy')

        roomData = gauntlet.getRoom()
        
        room_json = json.loads(roomData)
        
        home = os.path.expanduser("~")
        path = home + '/.icegauntletmaps'
 
        if (not os.path.isdir(path)):
            os.system('mkdir ' + path)

        roomName = path + '/' + (str(room_json['room'])).replace(" ", "_") + '.json'
        #print(roomName)
        with open(roomName, 'w') as f:
            json.dump(room_json,f)
    
        return 0
    
class RoomToolClient(Ice.Application):
    
    def mapManagingProxy(self, argv):
        
        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.RoomManagerPrx.checkedCast(proxy)
        
        if not gauntlet:
            raise RunTimeError('Invalid proxy')
        
        return gauntlet  


class AuthenticationToolClient(Ice.Application):
    
    def authenticationProxy(self, argv):

        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        return gauntlet

class Client(Ice.Application):

    def run (self, argv):

        if (argv[1] == './upload_map.sh'):
           
            roomToolClient = RoomToolClient()
            gauntlet = roomToolClient.mapManagingProxy(argv)

            with open (argv[4]) as f:
                data = json.load(f)

            gauntlet.publish(argv[3], json.dumps(data))

        elif (argv[1] == './delete_map.sh'):
            roomToolClient = RoomToolClient()
            gauntlet = roomToolClient.mapManagingProxy(argv)
            #do something
            #gauntlet.remove(argv[3], roomName)

        elif (argv[1] == './auth_user.sh'):
            authenticationToolClient = AuthenticationToolClient()
            gauntlet = authenticationToolClient.authenticationProxy(argv)

            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")

            m = hashlib.sha256()
            m.update(password.encode('utf8'))

            # Print user new token
            print(gauntlet.getNewToken(username, m.hexdigest()))
        
        elif (argv[1] == './run_game.sh'):
            gameToolClient = GameToolClient()
            gauntlet = gameToolClient.getRoom(argv)
            
            #proxy = self.communicator().stringToProxy(argv[2])
            #gauntlet = IceGauntlet.GamePrx.checkCast(proxy)
            
            #if not gaunlet:
            #    raise RunTimeError('Invalid proxy')
            
            #gauntlet.getRoom()    

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

