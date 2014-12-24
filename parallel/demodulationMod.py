import threading
import time

class demodulation (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        global variable
        global threadLock

        print "Starting Demodulatuion" 
        # Retrieve From The Buffer
        print "Retrieve From The Buffer"

        # Delete The Amount Taken
        print "Delete The Amount Taken"

        # Perform Processing
        threadLock.acquire()
        for i in range(0, 5):
            time.sleep(0.1)
            variable=variable+1
            print "Proc"
        threadLock.release()
        print "Exiting Demodulation"