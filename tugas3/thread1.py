import threading
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s)%(message)s',)

class MyThread(threading.Thread):
    def run(self):
        logging.debug('waw')

class ThreadClass(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print "%s says Hello World at time: %s\n" % (self.getName(),now)

def worker(num):
    print "Worker: %s" % num

threads = []

for i in range(5):
    t = MyThread()
    t.start()
