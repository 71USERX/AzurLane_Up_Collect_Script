import requests
import json
import re
import time
import os
import threading

import variable as var

# ********************************************************
# 请安装requests模块！否者将无法运行
# 可以使用一下指令安装：
# pip install requests
# ********************************************************

#Lambda Functions
compareIn = lambda new_uids,old_uids : [x for x in new_uids if x not in old_uids] 
#取出在new_uids里，old_uid里没有的数据
# 参数 list 两个列表

#Standard Functions
#发送请求，获取搜索“碧蓝航线”，分区为轻小说（你也可以在variable.py里换成其他的）的所有结果
# 参数 int 搜索结果的第几页
def sendGetRequest( page_num ):
    response = requests.get(url = var.address + str(page_num))
    return response.text

#获取该专栏作者的uid
# 参数 string 一个json文本
# 一般来说把sendGetRequest()函数的结果作为此函数的参数就好了
def getMid( text ):
    temp = var.regeX.findall(text)
    mids = []

    i = 0
    while i < len(temp):
        mids.append(re.sub(r"\D+","",temp[i]))
        mids[i] = int(mids[i])
        i += 1

    return mids

#根据uid获取该用户的昵称
# 参数 int 用户uid
def getName( uid ):
    responses = requests.get(url = var.InfoAddr + str(uid))
    temp = var.nameRegeX.findall(responses.text)
    if temp == []:
        return "[用户不存在]"
    name = temp[0].replace('"name":"',"")
    name = name.replace('",',"")
    return name

#将倒序线程与顺序线程获取的uid加入variable.py里的uids列表，并去重
# 参数 无参数
def addToUids():
    temp = var.thread_in + var.thread_seq
    uids = delDuplicated(temp)
    new_uids = compareIn(uids,var.uids)
    var.uids.extend(new_uids)

#列表去重
# 参数 list 一个列表
def delDuplicated( list0 ):
    return sorted(set(list0), key = list0.index)

def writeNames():
    fo = open("names.listf",mode="w",encoding="utf-8")
    var.finder_seq.reverse()
    names = []
    names.extend(var.finder_in)
    names.extend(var.finder_seq)
    i = 0
    while i < len(names):
        fo.write(names[i] + "\n")
        i += 1
    fo.close()

#读取uids.listf里面的所有数据并加入variable.py里的uids列表
# 参数 无参数
def readFromFile():
    fo = open("uids.listf",mode="r",encoding="utf-8")
    temp = fo.readlines()
    i = 0
    while i < len(temp):
        temp[i] = temp[i][0 : (len(temp[i]) - 1)]
        temp[i] = int(temp[i])
        i += 1
    fo.close()
    temp = delDuplicated(temp)
    return temp

#将variable里的所有uid写到uids.listf文件里
# 参数 无参数
def writeToFile():
    fo = open("uids.listf",mode="a+",encoding="utf-8")
    fo.seek(0,0)
    origin = fo.readlines()
    i = 0
    while i < len(origin):
        origin[i] = origin[i][0 : (len(origin[i]) - 1)]
        origin[i] = int(origin[i])
        i += 1    
    temp = compareIn(var.uids,origin)
    fo.seek(0,2)
    i = 0
    while i < len(temp):
        fo.write(str(temp[i]) + "\n")
        i += 1
    fo.close()

# 将uids.listf与names.listf合并成一个markdown文件
# 参数 无参数
def makeMarkdown():
    nfo = open("names.listf",mode="r",encoding="utf-8")
    ufo = open("uids.listf",mode="r",encoding="utf-8")
    mdfo = open("up.md",mode="w",encoding="utf-8")
    names = nfo.readlines()
    uids = ufo.readlines()
    mdfo.write("**排名不分前后**  \n")
    i = 0
    while i < len(names):
        names[i] = names[i][0:(len(names[i])-1)]
        i += 1
    nfo.close()

    i = 0
    while i < len(uids): 
        uids[i] = uids[i][0:(len(uids[i])-1)]
        i += 1
    ufo.close()
    
    i = 0
    while i < len(uids):
        mdfo.write("[" + names[i] + "]" + "(" + var.UsrPage + uids[i] + ")  \n")
        i += 1
    mdfo.close()

#顺序线程主函数，查找1-25页的所有搜索结果
# 参数 无参数
def inverted_thread():
    i = 1
    text = ""
    while i <= 25:
        text = sendGetRequest(i)
        GotUid = getMid(text)
        new_uid = compareIn(GotUid,var.thread_in)
        var.thread_in.extend(new_uid)
        print("Thread_in:page " + str(i) +" Processed.")
        i += 1
        time.sleep(var.waitingTime) 

#倒序线程主函数，查找26-50页的所有搜索结果
# 参数 无参数
def sequential_thread():
    i = 50
    text = ""
    while i > 25:
        text = sendGetRequest(i)
        GotUid = getMid(text)
        new_uid = compareIn(GotUid,var.thread_seq)
        var.thread_seq.extend(new_uid)
        print("Thread_seq:page " + str(i) +" Processed.")
        i -= 1
        time.sleep(var.waitingTime) 

#查找昵称线程主函数，将所有的uid匹配昵称并写入variable.py里的finder_*.py中
# 参数 无参数
# 别在此函数前放置readFromFil()函数！不然会重复匹配
def find_name_in_thread():
    uids = readFromFile()
    i = 0
    while i <= len(uids)//2 :
        name = getName(uids[i])
        var.finder_in.append(name)
        print("Finder_in:The no. "+ str(i) + " is " + name)
        i += 1
        time.sleep(var.waitingTime)

#倒序查找昵称
def find_name_seq_thread():
    uids = readFromFile()
    i = len(uids) - 1
    while i > len(uids)//2 :
        name = getName(uids[i])
        var.finder_seq.append(name)
        print("Finder_seq:The no. "+ str(i) + " is " + name)
        i -= 1
        time.sleep(var.waitingTime)

#顺序线程类
# 参数 无参数
class inverted_thread_class(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Thread Inverted Start!")

    def __del__(self):
        print("Thread Inverted Exit")

    def run(self):
        inverted_thread()

#倒叙线程类
# 参数 无参数
class sequential_thread_class(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Thread Sequential Start!")

    def __del__(self):
        print("Thread Sequential Exit")

    def run(self):
        sequential_thread()

#查找昵称线程类
# 参数 无参数
class find_name_in_thread_class(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Find Name Inverted Thread Start!")

    def __del__(self):
        print("Find Name Inverted Thread Exit")

    def run(self):
        find_name_in_thread()

#倒序查找昵称线程类
# 参数 无参数
class find_name_seq_thread_class(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Find Name Sequential Thread Strat")

    def __del__(self):
        print("Find Name Sequential Thread Exit")

    def run(self):
        find_name_seq_thread()
