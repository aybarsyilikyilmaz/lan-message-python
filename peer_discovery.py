import socket
import json
import time


def peer_discovery(port, user_dic, user):

    while True:
        try:
            #UDP socket creating
            peer_discover = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #
            #Socket listening
            peer_discover.bind(('',port))
            #
        except:
            print(f" - [ERROR] : System could not bind port 6000, trying again. Error : {str(e)}")
            continue

        while True:
            #get message, decode and load to json
            try:
                message, address = peer_discover.recvfrom(2048)
                message_json = message.decode("utf-8")
                message_dic = json.loads(message_json)
            except Exception as e:
                print(f"\n [ERROR] : System could not reach service announcment message. Error : {str(e)}")
                continue
            #

            #do not add user itself to list
            if message_dic['uuid'] == user['uuid']:
                continue
            #

            #print users who are online
            if not message_dic['uuid'] in user_dic:  
                print(f"\n - [System] : {message_dic['username']} is online.")
            #

            #save users to user_dic
            user_dic[message_dic['uuid']] = {
                "user_ip" : address[0],
                "username" : message_dic['username'],
                "uuid" : message_dic['uuid'],
                "last_seen" : time.time(),
                "user_status" : "online"
            }
            #

