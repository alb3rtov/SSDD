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
import uuid
import pickle
import Ice
import IceStorm
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

FILE_TOKEN_ROOM = "tokenRoom.json"
JSON_EXTENSION = ".json"
MAPS_PATH = "maps/"

servers_list = {}

class RoomManagerSync(IceGauntlet.RoomManagerSync):
    def hello(self, manager, managerId, current=None):
    
        if (manager_id != managerId): # No recibes el evento HELLO si eres el que lo envía
            servers_list.update({managerId : manager})
            print(" o/ HELLO {0} - RoomManager Instance: {1}".format(managerId, manager))
            publisher_object.announce(manager, managerId)
                
                #publisher_object.announce(manager, managerId)
        #except:
        #    print("Error appeding server to the list")

    def announce(self, manager, managerId, current=None):
        if (manager_id == managerId):
            print(" a/ ANNOUNCE {0} - RoomManager Instance: {1}".format(managerId, manager))

    def newRoom(self, roomName, managerId, current=None):
        print("newRoom")

    def removedRoom(self, roomName, current=None):
        print("removedRoom")

class RoomManager(IceGauntlet.RoomManager, Ice.Application):
    def get_publisher(self):
        publisher = self.topic.getPublisher()
        return IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisher)

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    
    def run(self, argv):
        global manager_id
        manager_id = str(uuid.uuid4())
        
        topic_mgr = self.get_topic_manager()

        if not topic_mgr:
            print("Invalid proxy")
            return 2

        ic = self.communicator()
        servant_rms = RoomManagerSync()
        servant_rm = RoomManager()
        adapter = ic.createObjectAdapter("RoomManagerSyncAdapter")
        subscriber = adapter.addWithUUID(servant_rms)
        proxy = adapter.addWithUUID(servant_rm)
        

        topic_name = "RoomManagerSyncChannel"
        qos = {}
        try:
            self.topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            self.topic = topic_mgr.create(topic_name)


        self.topic.subscribeAndGetPublisher(qos, subscriber)

        global publisher_object

        publisher_object = self.get_publisher()
        room_manager = IceGauntlet.RoomManagerPrx.uncheckedCast(proxy)

        print("Waiting events... '{}'".format(subscriber))
        adapter.activate()
        publisher_object.hello(room_manager , manager_id)

        self.shutdownOnInterrupt()

        ic.waitForShutdown()
        self.topic.unsubscribe(subscriber)

        return 0

    """ Class to manage maps """
    def publish(self, token, room_data, argv):
        """ Generate a map with the given room_data and check the token """
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        room_json = json.loads(room_data) #Loads file as a string
        room_name = MAPS_PATH + (str(room_json['room'])).replace(" ", "_") + JSON_EXTENSION
        #If file doesn't exists, create a new one
        if not os.path.isfile(FILE_TOKEN_ROOM):
            data = {}

            data[room_name] = gauntlet.getOwner(token)

            with open(FILE_TOKEN_ROOM, 'w') as file:
                json.dump(data,file, indent=4)

            #Publish the .json file in maps folder
            with open(room_name, 'w') as file:
                json.dump(room_json,file) #Dictionary to json file

        else:
            with open(FILE_TOKEN_ROOM) as file:
                data = json.load(file)

            if room_name in data:
                if data[room_name] == gauntlet.getOwner(token): # Check if is the owner
                    with open(room_name, 'w') as file:
                        json.dump(room_json,file)

                else:
                    raise IceGauntlet.RoomAlreadyExists()
            else:
                data[room_name] = gauntlet.getOwner(token)

                with open(FILE_TOKEN_ROOM, 'w') as file:
                    json.dump(data, file, indent=4)

                with open(room_name, 'w') as file:
                    json.dump(room_json,file)

    def remove(self, token, room_name, argv):
        """ Remove an existing map from directory maps/ """
        proxy = self.communicator().stringToProxy(sys.argv[1])
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        is_owner = False

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        full_room_name = room_name.replace(" ", "_") + JSON_EXTENSION
        files = os.listdir(MAPS_PATH)

        if full_room_name in files:
            full_room_name_path = MAPS_PATH + full_room_name

            with open(FILE_TOKEN_ROOM, "r") as file:
                lines = file.readlines()

            with open(FILE_TOKEN_ROOM, "w") as file:

                for line in lines:
                    if not (full_room_name_path in line and gauntlet.getOwner(token) in line):
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

    def availableRooms(self):
        return 0

class Server():
    """ Class server initialize and create servants and brokers
        for RoomManager and Dungeon proxies
    """
    def main(self, argv):
        RoomManager().main(sys.argv)

        """
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
        """
server = Server()
sys.exit(server.main(sys.argv))
