import socket
import select
import Queue
from threading import Thread
from time import sleep
from random import randint
import sys
 
class ProcessThread(Thread):
    def __init__(self):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
 
    
    def add(self, data):
        self.q.put(data)
 
    def stop(self):
        self.running = False

    def run(self):
        q = self.q
        while self.running:
            try:
                # block for 1 second only:
                value = q.get(block=True, timeout=1)
                process(value)
            except Queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()
        #
        if not q.empty():
            print "Elements left in the queue:"
            while not q.emFalsepty():
                print q.get()

t = ProcessThread()
t.start()

def process(value):
    """
    Implement this. Do something useful with the received data.
    """
    print value
    sleep(randint(1,5))    # emulating processing time

def main():
    s = socket.socket()                # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 5001                          # Reserve a port for your service.
    s.bind(('localhost', port))                 # Bind to the port
    print "Listening on host {h} port {p}...".format(p=port,h=host)
 
    s.listen(5)                 # Now wait for client connection.
    while True:
        try:
            client, addr = s.accept()
            ready = select.select([client,],[], [],2)
            if ready[0]:
                data = client.recv(4096)
                # print data
                t.add(data)
        except KeyboardInterrupt:
            print
            print "Stop."
            cleanup()
            break
        except socket.error, msg:
            print "Socket error! %s" % msg
            cleanup()
            break

def cleanup():
    t.stop()
    t.join()
 
 
if __name__ == "__main__":
    main()