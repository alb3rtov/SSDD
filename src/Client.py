#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import getpass
Ice.loadSlice('src/slice.ice')
import IceGauntlet

class RoomToolClient(Ice.Application):
    
    def getNewToken(self, argv):
        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        
        return gauntlet.getNewToken(username, password)
        

class Client(Ice.Application):
    
    def run (self, argv):    
        roomToolClient = RoomToolClient()
        proxy = self.communicator().stringToProxy(argv[1])
        gauntlet = IceGauntlet.MapManagingPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        token = roomToolClient.getNewToken(argv) 
        print(token) 
        gauntlet.publish(token, "datos")

        return 0

sys.exit(Client().main(sys.argv))

