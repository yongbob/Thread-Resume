
# coding: utf-8

import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        self.start_time = time.time()
        self.status = 'running'
        self.data = None
        
    def run(self):
        
        while self.__running.isSet():
            print( time.time()-self.start_time," = ",self.status)
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.do()
            time.sleep(0.5)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False
    
    def set_status(self,status): #设置状态用的，调试使用
        self.status=status
        
    def get_status(self): #在线程等待的时候，不会返回
        return self.status
    def thread_time(self):
        return time.time()-self.start_time
    def set_data(self,data):
        self.data = data
        
    def do(self):
        #time.sleep(0.5)
        for i in range(1,5):
            print("job thread:",i)
        print(self.data)
        print(self.thread_time())
        
if __name__ == '__main__': 
    job = Job()
    job.start()
    job.set_data('first job')
    print(threading.enumerate())
    time.sleep(3)

    job.set_status('pause')
    job.pause()
    print(threading.enumerate())
    time.sleep(5)
    print(job.get_status(),job.thread_time())
    time.sleep(3)
    
    job.set_status('running')
    job.set_data('second job ')
    print(job.get_status(),job.thread_time())
    job.resume()
    for i in range(1,10):
        print("main thred:",i)
        time.sleep(0.2)
    print(threading.enumerate())
    time.sleep(2)
    job.set_data('third job ')
    print(job.get_status(),job.thread_time())
    print(threading.enumerate())
    time.sleep(2)
    
    job.set_status('pause')
    job.pause()
    print(threading.enumerate())
    time.sleep(2)
    job.stop()
    time.sleep(1)
    print(threading.enumerate())
