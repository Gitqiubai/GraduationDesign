import requests
import demjson
import time
import random


#获取好友列表
def get_friend_list():


    #print(content)
    t = 0
    while True:
        print('this')
        #url = "http://127.0.0.1:5700/_get_friend_list"
        url = "http://111.230.243.181:5700/_get_friend_list"
        req = requests.get(url)
        content = demjson.decode(req.text)
        if content["data"] != None:

            list = {}
            for each in content["data"]:
                for friend_message in each['friends']:

                    list.setdefault(friend_message["nickname"],friend_message['user_id'])
            t = 0

            return list
        else:
            t = ++1
            if t <= 5:
                print(" >>[获取好友列表失败]正在重试[{}]..".format(t))
                time.sleep(2)
            else:
                return None


#消息发送模块
def send_private_msg(content):
    #url =  "http://127.0.0.1:5700/send_private_msg"
    #url =  "http://111.230.243.181:5700/send_private_msg"
    url =  "http://111.230.243.181:5700/send_group_msg"
    param = {
                #'user_id':'438793957',
                'group_id':'429114952',
                'message':content
            }
    req = requests.get(url,params=param)
    result = demjson.decode(req.text)

    if result["retcode"] == 0:
        print("[消息发送成功] to:{}".format(content))
    else:
        print("[消息发送失败] to:{}".format(content))

