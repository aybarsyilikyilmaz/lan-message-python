import os
import time

from control_status import control_status

def list_users(user_dic):

    #set constants
    count = 0
    control_status(user_dic)
    #

    print(f"\nUSERS:")
    
    for user in user_dic:
        count+=1
        print(f"{count}. {user_dic[user]['username']}  ({user_dic[user]['user_status']})")


    print(f"-----------------------------------------\nReturning to menu.\n")

    return