#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('src/slice.ice')
import IceGauntlet

class MapManaging(IceGauntlet.MapManaging, Ice.Application):

    def publish(self, token, roomData, argv):
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RunTimeError('Invalid proxy')

        print("token: {0}, RoomData: {1}".format(token, roomData))
        
        if (gauntlet.isValid(token)):
            print("El token es valido")
        else:
            print("El token es no es valido")

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
