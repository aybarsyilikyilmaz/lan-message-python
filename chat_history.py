import os
import json

def history(user_dic, lock):

    message_log = None

    print("\n--------------------------------------------")

    #read data from message_log.txt
    with lock:
        if os.path.exists('message_log.txt'):
            try:
                with open("message_log.txt", "r") as file:
                    data = file.read()
                    if data:
                        try:
                            message_log = json.loads(data)
                        except Exception as e:
                            print(" - [ERROR] : System could not access data in 'message_log.txt', it will be cleared.")
                            with open("message_log.txt", "w") as file:
                                pass
                            return
                    else:
                        print(" - [System] : There is no saved message.")
                        return
            except Exception as e:
                print(f" - [ERROR] : System could not open 'message_log.txt'.")
                return
        else:
            print(f" - [ERROR] : System could not reach 'message_log.txt', it will be cleared.")
            with open("message_log.txt", "w") as file:
                pass
    #

    #printing all saved message
    for element in message_log:

        if element['direction'] == "sent":
            print(f"({element['time']}) - ({element['day']}) - sent to [{element['username']}] : {element['message']}\n")
        if element['direction'] == "received":
            print(f"({element['time']}) - ({element['day']}) - received from [{element['username']}] : {element['message']}\n")
    #

    #clear the memory
    message_log.clear()
    #   

    print("--------------------------------------------")

    return