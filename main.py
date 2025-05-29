import threading
import os


from service_announcement import service_announcemet
from peer_discovery import peer_discovery
from chat_initiator import chat_initiator
from user_initiator import user_initiator
from chat_responder import chat_responder


def main():
    threads = []
    quit_event = threading.Event()
    lock = threading.Lock()


    #Set constants
    port = 6000
    addr = '192.168.1.255'
    user_dic = {}
    message_log = []
    #

    #get username
    try:   
        while True:
            main_user = user_initiator()
            if main_user:
                username = main_user['username']
                break
    except Exception as e:
        print(f" - [ERROR] :  System could not initiate user: {e}")
        exit(1)
    #

    #create message_log.txt
    if not os.path.exists('message_log.txt'):
        with open("message_log.txt", "w") as file:
            pass
    #

    #Threading
    udp_server_thread = threading.Thread(target=service_announcemet, args=(port, addr, main_user))
    udp_client_thread = threading.Thread(target=peer_discovery, args=(port, user_dic, main_user))
    chat_responder_thread = threading.Thread(target=chat_responder, args=(user_dic, lock, message_log))
    #

    #start threads
    threads.extend([udp_server_thread, udp_client_thread, chat_responder_thread])
        
    for thread in threads:
        thread.daemon = True
        thread.start()
    #

    chat_initiator(user_dic, username, quit_event, lock, message_log)


if __name__ == "__main__":
    main()
