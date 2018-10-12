#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-

# 本程序要做的一件事就是主线程有往队列里插入5个数据，有3个线程从这个队列里每秒钟尝试取数据，直到队列被取空，程序结束
# 方法简单来说就是上锁， 主线程上锁后一次性把5个数据全部入队完毕，另外3个线程每个一秒尝试取数据，方法是先尝试获取锁，
# 获得了就取一个数，然后休息一秒进入下一个周期，否则直接休息一秒进入下一个周期
# 这样3个线程之间在获取锁这件事上是有竞争关系的，任意时刻只有一个线程能获得锁
import queue
import threading
import time

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print
        "Starting " + self.name
        process_data(self.name, self.q)
        print
        "Exiting " + self.name


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (threadName, data))
        else:
            queueLock.release()
        time.sleep(1)


threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# 创建3个新线程，用来从队列里读数据
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print("Exiting Main Thread")