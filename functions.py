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
compareIn = lambda new_uids,old_uid : [x for x in new_uids if x not in old_uid] 
#取出在new_uids里，old_uid里没有的数据
# 参数 list 两个列表
delDuplicated = lambda list0 : sorted(set(list0), key = list0.index)
#列表去重
# 参数 list 一个列表

#Standard Functions
#发送请求，获取搜索“碧蓝航线”，分区为轻小说（你也可以在variable.py里换成其他的）的所有结果
# 参数 int 搜索结果的第几页
def sendGetRequest( page_num ):
    response = requests.get(url = var.address + str(page_num))
    return response.text

#获取该专栏作者的uid
# 参数 string 一个json文本
# 一般来说把sendGetRequest函数的结果作为此函数的参数就好了
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
    name = name.replace('","sex":',"")
    return name

#将倒序线程与顺序线程获取的uid加入variable.py里的uids列表，并去重
# 参数 无参数
def addToUids():
    temp = var.thread_in + var.thread_seq
    uids = delDuplicated(temp)
    new_uids = compareIn(uids,var.uids)
    var.uids.extend(new_uids)

#读取uids.listf里面的所有数据并加入variable.py里的uids列表
# 参数 无参数
def readFromFile():
    fo = open("uids.listf",mode="a+")
    fo.seek(0,0)
    temp = fo.readlines()
    i = 0
    while i < len(temp):
        temp[i] = temp[i][0:(len(temp[i])-1)]
        temp[i] = int(temp[i])
        i += 1
    temp = delDuplicated(temp)
    var.uids.extend(temp)
    fo.close()

#将variable里的所有uid写到uids.listf文件里
# 参数 无参数
def writeToFile():
    fo = open("uids.listf",mode="a+",encoding="utf-8")
    new_uids = []
    new_uids.extend(var.uids)
    readFromFile()
    pre_wrt_uids = compareIn(new_uids,var.uids)
    var.uids.extend(pre_wrt_uids)
    i = 0
    while i < len(var.uids):
        fo.write(str(var.uids[i]) + "\n")
        i += 1
    fo.close()

# 将uids.listf与names.listf合并成一个markdown文件
# 参数 无参数
def makeMarkdown():
    nfo = open("names.listf",mode="a+",encoding="utf-8")
    ufo = open("uids.listf",mode="a+",encoding="utf-8")
    mdfo = open("up.md",mode="a+",encoding="utf-8")
    nfo.seek(0,0)
    ufo.seek(0,0)
    names = nfo.readlines()
    uids = ufo.readlines()
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
        time.sleep(10) 

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
        time.sleep(10) 

#查找昵称线程主函数，将所有的uid匹配昵称并写入names.listf文件中
# 参数 无参数
def find_name_in_thread():
    readFromFile()
    i = 0
    fo = open("names.listf",mode="a+",encoding="utf-8")
    while i < len(var.uids):
        name = getName(var.uids[i])
        fo.write(name + "\n")
        print("Finder_in:The no. "+ str(i) + " is " + name)
        i += 1
        time.sleep(5)
    fo.close()

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