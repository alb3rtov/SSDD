#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=E0401
# pylint: disable=C0413

"""
Authentication and RoomManager Client

"""

import sys
import getpass
import json
import hashlib
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

def generate_hash_sha256(password):
    """ Generate the hash sha256 from a given string """
    m_hash = hashlib.sha256()
    m_hash.update(password.encode('utf8'))

    return m_hash.hexdigest()


class RoomToolClient(Ice.Application):
    """ Class to create roommanager proxy """
    def map_managing_proxy(self, argv):
        """ Returns the RoomManager proxy """
        proxy = self.communicator().stringToProxy(argv[2])
        gauntlet = IceGauntlet.RoomManagerPrx.checkedCast(proxy)

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        return gauntlet

class AuthenticationToolClient(Ice.Application):
    """ Class to create authentication proxy"""
    def authentication_proxy(self, argv):
        """ Returns the authenticaction proxy """
        proxy = self.communicator().stringToProxy(argv)
        gauntlet = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not gauntlet:
            raise RuntimeError('Invalid proxy')

        return gauntlet

class Client(Ice.Application):
    """ Client class instance other class depeding on args"""
    def run(self, argv):

        if argv[1] == 'upload':

            room_tool_client = RoomToolClient()
            gauntlet = room_tool_client.map_managing_proxy(argv)

            with open (argv[4]) as file:
                try:
                    data = json.load(file)
                except:
                    raise IceGauntlet.WrongRoomFormat()

                if (data.get('data') is None or data.get('room') is None):
                    raise IceGauntlet.WrongRoomFormat()
            
            gauntlet.publish(argv[3], json.dumps(data))

        elif argv[1] == 'delete':
            room_tool_client = RoomToolClient()
            gauntlet = room_tool_client.map_managing_proxy(argv)
            gauntlet.remove(argv[3], argv[4])

        elif argv[1] == '-t':
            authentication_tool_client = AuthenticationToolClient()
            gauntlet = authentication_tool_client.authentication_proxy(argv[3])

            password = getpass.getpass("Enter password:")

            # Print user new token
            print(gauntlet.getNewToken(argv[2], generate_hash_sha256(password)))

        elif argv[1] == 'changepass':
            authentication_tool_client = AuthenticationToolClient()
            gauntlet = authentication_tool_client.authentication_proxy(argv[2])

            username = input("Enter username: ")
            current_password = getpass.getpass("Enter current password: ")
            new_password = getpass.getpass("Enter new password: ")

            gauntlet.changePassword(username,
                    generate_hash_sha256(current_password),
                    generate_hash_sha256(new_password))

        return 0

sys.exit(Client().main(sys.argv))
