import threading
import Queue
import time

myQueue = Queue.Queue()

class count_stuff(threading.Thread):
    def __init__(self,start_num,end,q):
        self.num = start_num
        self.end = end
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.num != self.end:
                self.q.put(self.num)
                self.num += 1
                time.sleep(1)
            else:
                break

myThread = count_stuff(1,5,myQueue)
myThread.start()

while True:
    if not myQueue.empty():
        val = myQueue.get()
        print "Output: ", val
    else:
        print "Empty"
    time.sleep(2)
