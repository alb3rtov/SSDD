#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('src/slice.ice')
import IceGauntlet

class MapManaging(IceGauntlet.MapManaging):
    def publish(self, mapName, roomData, current=None):
        print("Map name: {0}, RoomData: {1}".format(mapName, roomData))
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
