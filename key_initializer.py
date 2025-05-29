import secrets
import json
import socket


def key_initiator(client_socket,):

    P = 19
    G = 2
    #

        
    #initiate user public key
    private_key = secrets.randbelow(19-1) + 1
    public_key = pow(G, private_key, P)
    #

    #send user public key
    try:
        message_dic = {"key" : str(public_key)}
        message_json = json.dumps(message_dic)
        client_socket.sendall(message_json.encode('utf-8'))
    except Exception as e:
        print(f"\n - [ERROR] : System could not create key due to connection errors. Error : {str(e)}")
        return None
    #

    #get client public key
    try:
        rcv_message_json = client_socket.recv(1024).decode('utf-8')
        rcv_message_dic = json.loads(rcv_message_json)
        other_public_key = int(rcv_message_dic['key'])
    except Exception as e:
        print(f"\n - [ERROR] : System could not create key due to connection errors. Error : {str(e)} ")
        return None
    #

    #initiate shared key, hashed it, get first 8 bit
    shared_key = pow(other_public_key, private_key, P)
    return shared_key
    #