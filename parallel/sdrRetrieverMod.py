import threading
import time

class sdrRetriever (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        global variable
        global threadLock

        print "Starting SDRRetriever" 
        
        # Configure SDR
        print "Configure SDR"

        # Capture Data
        print "Capturing Data"

        # Append to the buffer
        for i in range(0, 5):
            time.sleep(1)
            threadLock.acquire()
            variable=variable+1
            print "Rx"
            threadLock.release()

        print "Exiting sdrRetriever"
