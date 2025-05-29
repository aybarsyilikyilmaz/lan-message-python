import time

def control_status(user_dic):


    for user in user_dic:

        time_preiod = time.time()-user_dic[user]['last_seen']

        if time_preiod <= 10:
            user_dic[user]['user_status'] = "online"

        elif time_preiod <= (15*60):
            user_dic[user]['user_status'] = "away"

        else:
            del user_dic[user]

    return

        