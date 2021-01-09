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


class DungeonAreaSyncI(IceGauntlet.DungeonAreaSync):
    def __init__(self, dungeon_area):
        self._parent_ = dungeon_area
    
    def fireEvent(self, event, current=None):
        try:
            event = pickle.loads(event)
        except Exception:
            return
        self._parent_.event_handler(event)

class DungeonAreaI(IceGauntlet.DungeonArea):
    """
    def run(self, argv):
        topic_mgr = self.getEventChannel()

        if not topic_mgr:
            print("Invalid proxy")
    
        topic_name = "RoomManagerSyncChannel"

        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("No such topic found, creating")
            topic = topic.mgr.create(topic_name)
        
        publisher = topic.getPublisher()
        prueba = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisher)

        prueba.newRoom("hola","adios")

    def getEventChannel(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        
        if proxy is None:
            print("property {} not set".format(key))
            return None
        
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    """

    
    def __init__(self):
        self._topic_name_ = str(uuid.uuid4())
        self._topic_ = self.create_new_topic(self._topic_name_)

        self._subscriber_ = DungeonAreaSyncI(self)
        self.subscribe_to_topic(self._subscriber_, self._topic_name_)

    def event_handler(self, event):
        event_type = event[0]
        event_args = event[1:]
        if event_type == 'kill_object':
            self.kill_object(*event_args)
        elif event_type == 'spawn_actor':
            self.spawn_actor(*event_args)
        elif event_type == 'open_door':
            self.open_door(*event_args)

    def getMap(self):
        return 0

    def getActors(self):
        return 0
 
    def getItems(self):
        return 0

    def getNextArea(self):
        return 0
    
    def create_new_topic(self, topic_name):
        return 0
    


class Dungeon(IceGauntlet.Dungeon, Ice.Application):
    """ Class for game service """
    def getEntrance(self, argv):
        print("getEntrance")

class RoomManagerSync(IceGauntlet.RoomManagerSync):
    def hello(self, manager, managerId):
        print("hello")
    def announce(self, manager, managerId):
        print("announce")
    def newRoom(self, roomName, managerId):
        print(roomName)
        print(managerId)
    def removedRoom(self, roomName):
        print("removedRoom")

class RoomManager(IceGauntlet.RoomManager, Ice.Application):
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

class Server(Ice.Application):
    """ Class server initialize and create servants and brokers
        for RoomManager and Dungeon proxies
    """
    def run(self, argv):
        DungeonArea()
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
