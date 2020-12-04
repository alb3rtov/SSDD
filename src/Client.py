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

        proxy = self.communicator().stringToProxy(argv)
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        return gauntlet

class Client(Ice.Application):

    def generateHashSha256(self, password):

        m = hashlib.sha256()
        m.update(password.encode('utf8'))
        
        return m.hexdigest()
    
    def run (self, argv):

        if (argv[1] == 'upload'):
           
            roomToolClient = RoomToolClient()
            gauntlet = roomToolClient.mapManagingProxy(argv)

            with open (argv[4]) as f:
                try:
                    data = json.load(f)
                except:
                    raise IceGauntlet.WrongRoomFormat()

            gauntlet.publish(argv[3], json.dumps(data))

        elif (argv[1] == 'delete'):
            roomToolClient = RoomToolClient()
            gauntlet = roomToolClient.mapManagingProxy(argv)
            #do something
            #gauntlet.remove(argv[3], roomName)

        elif (argv[1] == '-t'):
            authenticationToolClient = AuthenticationToolClient()
            gauntlet = authenticationToolClient.authenticationProxy(argv[3])

            password = getpass.getpass("Enter password:")

            # Print user new token
            print(gauntlet.getNewToken(argv[2], self.generateHashSha256(password)))

        elif (argv[1] == 'changepass'):
            authenticationToolClient = AuthenticationToolClient()
            gauntlet = authenticationToolClient.authenticationProxy(argv[2])
            
            username = input("Enter username: ")
            current_password = getpass.getpass("Enter current password: ")
            new_password = getpass.getpass("Enter new password: ")
            
            gauntlet.changePassword(username, self.generateHashSha256(current_password), self.generateHashSha256(new_password))
            
        return 0
#  self.generateHashSha256(current_password)
sys.exit(Client().main(sys.argv))

