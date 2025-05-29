import os
import json
import pyDes
import base64
import socket
import secrets
from datetime import datetime


def chat_responder(user_dic, lock, message_log):

    #set constants
    G = 2
    P = 19
    #

    while True:
        #create socket
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.settimeout(None)
        except Exception as e:
            print(f"\n - [ERROR] : System could not establish TCP Server Socket, trying agin. {str(e)}")
            continue
        #

        #set socket port
        try:
            server_socket.bind(('', 6001))
        except Exception as e:
            print(f"\n - [ERROR] : System can not bind to port 6001, trying again. Error : {str(e)}")
            try:
                server_socket.close()
            except:
                pass
            continue
        #

        #start listening on port 6001
        server_socket.listen()
        #


        #get sender message
        while True:

            shared_key = None

            try:
                client_socket, client_address = server_socket.accept()

                #get the uuid of user who wants to connect
                for user in user_dic:
                    if user_dic[user]['user_ip'] == client_address[0]:
                        client_uuid = user
                        break
                #

            except Exception as e:
                print(f"\n - [ERROR] : System could not accept connection request. Error : {str(e)}")
                continue



            while True:
                message = None

                #getting dictionary
                try:
                    byte_message = client_socket.recv(1024)
                    if not byte_message:
                        print(" - [ERROR] : System could not receive valid data.")
                        break
                except Exception as e:
                    print(f"\n - [ERROR] : System could not receive message comes from {user_dic[client_uuid]['username']}. Error : {str(e)}")
                    break
                message_json = byte_message.decode('utf-8')
                message_dic = json.loads(message_json)
                #

                #getting dictionary key
                keys = list(message_dic.keys())
                key = keys[0]
                #

                #
                if key == "unencrypted_message":
                    encoded_message = message_dic['unencrypted_message']
                    message = base64.b64decode(encoded_message.encode('utf-8')).decode('utf-8')
                    print(f"\n({datetime.now().strftime('%d-%m-%Y')}) - ({datetime.now().strftime('%H:%M')}) - [{user_dic[client_uuid]['username']}] : {message}" )


                elif key == "key":
                     other_public_key = int(message_dic['key'])
                     
                     private_key = secrets.randbelow(19-1) + 1
                     public_key = pow(G, private_key, P)

                     send_message_dic = {"key" : str(public_key)}
                     send_message_json = json.dumps(send_message_dic)

                     client_socket.sendall(send_message_json.encode('utf-8'))
                     shared_key = str(pow(other_public_key, private_key, P))



                elif key == "encrypted_message":

                    if not shared_key:
                        print(" - [ERROR] : System could not reach key coming from {user_dic[client_uuid]['username']}")

                    encoded_message = message_dic["encrypted_message"]
                    encrypted_message = base64.b64decode(encoded_message.encode('utf-8'))

                    message_byte = pyDes.triple_des(shared_key.ljust(24, '0')).decrypt(encrypted_message, padmode=2)

                    message = message_byte.decode('utf-8') 
                    print(f"\n({datetime.now().strftime('%d-%m-%Y')}) - ({datetime.now().strftime('%H:%M')}) - [{user_dic[client_uuid]['username']}] : {message}" )
                #


                if message:
                    #save message to message_log list
                    data = {
                        "message" : message,
                        "direction" : "received",
                        "username" : user_dic[client_uuid]['username'],
                        "day" : datetime.now().strftime('%d-%m-%Y'),
                        "time" : datetime.now().strftime('%H:%M')
                    }
                    message_log.append(data)
                    #

                    #save the message to message_log.txt
                    with lock:
                        if os.path.exists("message_log.txt"):
                            with open("message_log.txt", "r") as file:
                                try:
                                    message_log = json.load(file)
                                except json.JSONDecodeError:
                                    message_log = []
                        else:
                            message_log = []

                        message_log.append(data)

                        with open("message_log.txt", "w") as file:
                            json.dump(message_log, file, indent=2)
                            message_log.clear()

                        break
                    #