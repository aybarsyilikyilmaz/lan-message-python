import json
from datetime import datetime

from list_users import list_users
from tcp_sender import tcp_sender
from chat_history import history



def chat_initiator(user_dic, username, quit_event, lock, message_log):

    print(f"\n Hello {username} !")
    print("\n - Available commands:\n - 'users'   : Show users list,\n - 'history' : Show message history,\n - 'chat'    : Choose one user,\n - 'quit'    : Exit program.\n")
    print("-----------------------------------------")

    while True:

        main_input = input("\n - [System] : Your choice : ").strip().lower()

        if main_input == "users":
            list_users(user_dic)
            continue

        elif main_input == "history":
            history(user_dic, lock)

        elif main_input == "quit":
            quit_event.set()
            return

        elif main_input == "chat":
            chosen_user = input("\n - [System] : Enter a username : ").strip().lower()

            #check if the entered username exists
            if not any(user['username'] == chosen_user for user in user_dic.values()):
                print("\n - [System] : There is no user with this name. Returning to menu.")
                continue
            #

            for user in user_dic:

                if user_dic[user]['username'] == chosen_user:
                    secure_input = input("\n - [System] : Do you want to chat securely or unsecurely? (secure/unsecure) : ")
                    message = input(f"({datetime.now().strftime('%d-%m-%Y')}) - ({datetime.now().strftime('%H:%M')}) - [You] : ")

                    if secure_input == "secure":
                        tcp_sender(user_dic, user, message, True, lock, message_log)

                    elif secure_input == "unsecure":
                        tcp_sender(user_dic, user, message, False, lock, message_log)
                    else:
                        print("\n - [System] : This is not a valid input. Returning to menu.")

        else:
            print("\n - [System] : This is not a valid input. Returning to menu.")
            


            
