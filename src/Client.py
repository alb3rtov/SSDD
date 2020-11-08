#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('src/slice.ice')
import IceGauntlet

#class RoomsToolClient(Ice.Application):
	
class Client(Ice.Application):
    def run(self,argv):
        proxy = self.communicator().stringToProxy(argv[1])
        gauntlet = IceGauntlet.MapManagingPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        roomName = input("Enter room name: ")
        roomData = input("Enter room data (JSON file): ")
        gauntlet.publish(roomName, roomData)
        
        return 0

sys.exit(Client().main(sys.argv))

