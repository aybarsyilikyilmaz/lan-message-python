import os
import json
import uuid


def user_initiator():

    #get user info from user.txt, if it exist
    if os.path.isfile("user.txt"):

        try:
            with open("user.txt", "r") as file:
                data = file.read()
                if data:
                    saved = json.loads(data)
                    main_user = {
                        "uuid" : saved['uuid'],
                        "username" : saved['username']
                    }
                else:
                    print(" - [ERROR] : System could not read 'user.txt', its content is corrupted.")
                    os.remove('user.txt')
                    return None
                return main_user
        except Exception as e:
            print(f" - [ERROR] : System could not reach 'user.txt' : {e}")
            return None
    #

    #initiate user, save it to user.txt
    else:
        while True:
            username = input("\n - [System] : Enter your username: ").strip().lower()

            if not username:
                print("\n - [ERROR] : Enter a valid username !")
                continue

            main_user = {
                "uuid" : str(uuid.uuid4()),
                "username" : username
            }

            try:
                with open("user.txt", "w") as file:
                    json.dump(main_user, file, indent=2)
            except Exception as e:
                print(f" - [ERROR] : System could not write 'user.txt' : {e}")
                continue

            return main_user
    #