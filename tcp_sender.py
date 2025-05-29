import os
import json
import pyDes
import base64
import socket
from datetime import datetime

from key_initializer import key_initiator



def tcp_sender(user_dic, user, message, is_secure, lock, message_log):

    shared_key = None

    #initiate socket and connect
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(None)

        client_socket.connect((user_dic[user]['user_ip'], 6001))

    except Exception as e:
        print(f"\n - [ERROR] : System could not establish connection with {user_dic[user]['username']}. Error: {str(e)}")
        return 
    #



    message_json = None

    if is_secure == False:
        message_dic = {"unencrypted_message" : (base64.b64encode(message.encode('utf-8')).decode('utf-8'))}
        message_json = json.dumps(message_dic)


    elif is_secure == True:

        shared_key = str(key_initiator(client_socket))

        if shared_key:
            message_bytes = message.encode('utf-8')
            message_encrypted = pyDes.triple_des(shared_key.ljust(24, '0')).encrypt(message_bytes, padmode=2)
            encoded_message = base64.b64encode(message_encrypted).decode('utf-8')
            message_dic = {"encrypted_message" : encoded_message}
            message_json = json.dumps(message_dic)

        if not shared_key:
            print(f"\n - [ERROR] : System could not exchange key with {user_dic[user]['username']}.")

    #send message to server
    try:
        client_socket.sendall(message_json.encode('utf-8'))
    except Exception as e:
        print(f"\n - [ERROR] : System could not send the message to {user_dic[user]['username']}. Error: {str(e)}")
    #
    
    #save message to messege_log list
    data = {
        "message" : message,
        "direction" : "sent",
        "username" : user_dic[user]['username'],
        "day" : datetime.now().strftime('%d-%m-%Y'),
        "time" : datetime.now().strftime('%H:%M')
    }
    #

    # log the message to message_log.txt
    with lock:
        if os.path.exists("message_log.txt"):
            with open("message_log.txt", "r") as file:
                try:
                    message_log = json.load(file)
                except json.JSONDecodeError:
                    message_log = []
        else:
            messages_log = []

        message_log.append(data)

        with open("message_log.txt", "w") as file:
            json.dump(message_log, file, indent=2)
            message_log.clear()
    #



    try:
        client_socket.close()
        return
    except:
        return