#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0413

"""
RoomManager and Dungeon game SERVER

"""

import sys
import json
import os
import random
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

FILE_TOKEN_ROOM = "tokenRoom.json"
JSON_EXTENSION = ".json"
MAPS_PATH = "maps/"

class Dungeon(IceGauntlet.Dungeon, Ice.Application):
    """ Class for game service """
    def getRoom(self, argv):
        """ Returns a dictionary with the data map and map name """
        #Check if there are maps in maps/
        if len(os.listdir(MAPS_PATH)) <= 0:
            raise IceGauntlet.RoomNotExists()
        # Choose random map
        files = os.listdir(MAPS_PATH)
        value = random.randint(0, len(files)-1)

        filename = MAPS_PATH + files[value]
        #print(filename)

        with open(filename) as file:
            data = json.load(file)

        return json.dumps(data)

class RoomManager(IceGauntlet.RoomManager, Ice.Application):
    """ Class to manage maps """
    def publish(self, token, room_data, argv):
        """ Generate a map with the given room_data and check the token """
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        if gauntlet.isValid(token):
            room_json = json.loads(room_data) #Loads file as a string
            room_name = MAPS_PATH + (str(room_json['room'])).replace(" ", "_") + JSON_EXTENSION
            #If file doesn't exists, create a new one
            if not os.path.isfile(FILE_TOKEN_ROOM):
                data = {}

                data[room_name] = token

                with open(FILE_TOKEN_ROOM, 'w') as file:
                    json.dump(data,file, indent=4)

                #Publish the .json file in maps folder
                with open(room_name, 'w') as file:
                    json.dump(room_json,file) #Dictionary to json file

            else:
                with open(FILE_TOKEN_ROOM) as file:
                    data = json.load(file)

                if room_name in data:
                    if data[room_name] == token: # Check if is the owner
                        with open(room_name, 'w') as file:
                            json.dump(room_json,file)

                    else:
                        raise IceGauntlet.RoomAlreadyExists()
                else:
                    data[room_name] = token

                    with open(FILE_TOKEN_ROOM, 'w') as file:
                        json.dump(data, file, indent=4)

                    with open(room_name, 'w') as file:
                        json.dump(room_json,file)

        else:
            raise IceGauntlet.Unauthorized()

    def remove(self, token, room_name, argv):
        """ Remove an existing map from directory maps/ """
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        is_owner = False

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        if gauntlet.isValid(token):

            full_room_name = room_name.replace(" ", "_") + JSON_EXTENSION
            files = os.listdir(MAPS_PATH)

            if full_room_name in files:
                full_room_name_path = MAPS_PATH + full_room_name

                with open(FILE_TOKEN_ROOM, "r") as file:
                    lines = file.readlines()

                with open(FILE_TOKEN_ROOM, "w") as file:

                    for line in lines:
                        if not (full_room_name_path in line and token in line):
                            file.write(line)
                        else:
                            is_owner = True
                            os.system('rm ' + full_room_name_path)

                if not is_owner:
                    raise IceGauntlet.Unauthorized()

                if os.stat(FILE_TOKEN_ROOM).st_size <= 3:
                    os.system('rm ' + FILE_TOKEN_ROOM)
            else:
                raise IceGauntlet.RoomNotExists()
        else:
            raise IceGauntlet.Unauthorized()

class Server(Ice.Application):
    """ Class server initialize and create servants and brokers
        for RoomManager and Dungeon proxies
    """
    def run(self, argv):
        rm_broker = self.communicator()
        rm_servant = RoomManager()

        rm_adapter = rm_broker.createObjectAdapter("RoomManagerAdapter")
        rm_proxy = rm_adapter.add(rm_servant, rm_broker.stringToIdentity("RoomManager"))

        print(rm_proxy, flush = True)

        d_broker = self.communicator()
        d_servant = Dungeon()

        d_adapter = d_broker.createObjectAdapter("DungeonAdapter")
        d_proxy = d_adapter.add(d_servant, d_broker.stringToIdentity("Dungeon"))

        os.system("echo '" + str(d_proxy) + "' | tee config/game-proxy.out > /dev/null")

        rm_adapter.activate()
        d_adapter.activate()

        self.shutdownOnInterrupt()

        rm_broker.waitForShutdown()
        d_broker.waitForShutdown()

        return 0

server = Server()
sys.exit(server.main(sys.argv))
