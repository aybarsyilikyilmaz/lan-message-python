import socket
import time
import json


def service_announcemet(port, broadcast_adress, main_user):

    while True:
        try:
            #UDP socket creating
            service_annocer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #

            #Set socket as broadcast
            service_annocer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #
        except Exception as e:
                print(f"\n - [ERROR] : System could not broadcast on port 6000, trying again. Error: {str(e)}")
                continue

        #Send message in every 8 seconds
        while True:

            message_dic = {
                "uuid" : main_user['uuid'],
                "username" : main_user['username']
            }
            message_json = json.dumps(message_dic)

            try:
                service_annocer.sendto(message_json.encode('utf-8'), (broadcast_adress, port))
            except Exception as e:
                print(f"\n - [ERROR] : System could not broadcast. Error: {str(e)}")
                continue
            time.sleep(8)



