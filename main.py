import functions as fns

import threading

# *********************************************************
# 由于b站的限制，只有50页可以访问，所以有一些up的专栏就查不出来
# 也希望有大佬可以给出更好的解决方案
# 因为怕b站锁api，所以在执行请求时加了延迟
# 至于main.py里的main函数嘛，各位根据自己需要，
# 自行写一下代码好了，我也不敢保证我的需求是不是一定符合你的需求。
# 函数的作用我已经在functions.py里注释好了
# ---------------------------------------------------------
# 下面提供的是最简单的实现
# 至于为什么把python的for写得和C一样呢，
# 因为我是刚从C转到python，所以很多东西不习惯。
# *********************************************************

def main():
    
    thread_in = fns.inverted_thread_class()
    thread_seq = fns.sequential_thread_class()

    thread_in.start()
    thread_seq.start()

    thread_in.join()
    thread_seq.join()

    fns.addToUids()
    fns.writeToFile()

    thread_find_in  = fns.find_name_in_thread_class()
    thread_find_seq = fns.find_name_seq_thread_class()
    thread_find_in.start()    
    thread_find_seq.start()
    thread_find_in.join()
    thread_find_seq.join()

    fns.writeNames()

    fns.makeMarkdown()

main()
