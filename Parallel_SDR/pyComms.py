#!/usr/bin/python

from rtlsdr import *
import time
import pylab
import numpy
import threading
import time
import math
from Tkinter import *
import ttk

# Constants
threadLock=threading.Lock()
sampleBuffer=[]
timeVector=[]
totalStartTime=0
elapsedTime=0
sampleRate=2.4e6
centerFreq=901e6
gain=10
numSamples=256*256
elapsedTime=0
numSweeps=int(math.ceil(elapsedTime/(numSamples/sampleRate)))

class figureWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("BFSK Demodulator")
        self.style = ttk.Style()
        self.style.theme_use("default")
        

        # Widgets        
        lbl = Label(self, text="Parameters")
        record = Button(self, text="Record")
        stop = Button(self, text="Stop")
        plot = Button(self, text="Plot")
        #data = Text(self)
        exit = Button(self, text="Exit Program")

        # Placement
        #self.parent.grid(column=0, row=0, columnspan=4, rowspan=10, sticky=(N, S, E, W))
        lbl.grid(sticky=(N, S, E, W), pady=4, padx=5)
        record.grid(sticky=(N, S, E, W),row=1, column=1)
        stop.grid(sticky=(N, S, E, W),row=1, column=2)
        plot.grid(sticky=(N, S, E, W),row=1, column=3)
        exit.grid(sticky=(N, S, E, W),row=10, column=3)
        #data.grid(row=5, column=0, rowspan=1, columnspan=1)

        self.pack()
       

# Thread that will do the demodulations
class demodulation (threading.Thread):
    def __init__(self, threadID, samples):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.samples=samples
    def run(self):
        global variable
        global threadLock

        # Perform Processing
        procTimeStart=time.clock()

        transform=numpy.fft.fft(self.samples)
        #print "Processing, Start: " + repr(procTimeStart) + " Duration: " + repr(time.clock()-procTimeStart)
        

# Thread that recieves samples from the ADC
class sdrRetriever (threading.Thread):
    def __init__(self, threadID, sampleRate, centerFreq, gain, numSamples, numSweeps):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.sampleRate= sampleRate
        self.centerFreq= centerFreq
        self.gain=gain
        self.numSamples= numSamples
        self.numSweeps= numSweeps

    def configureSDR(self):
        global sdr
        sdr = RtlSdr()

        # Bandwidth/Sample Rate
        sdr.rs = self.sampleRate
        # Center Freq
        sdr.fc = self.centerFreq
        # Gain
        sdr.gain = self.gain
        numSamplesPerSweep = self.numSamples

    def run(self):
        global totalStartTime, threadLock, sdr, sampleBuffer, numSamples, startTime, timeVector

        print "Starting SDRRetriever" 

        for i in range(self.numSweeps):

            rxTimeStart=time.clock()
            
            # Obtain Samples
            sampleSweep=sdr.read_samples(self.numSamples)

            # Append to the buffer
            threadLock.acquire()
            sampleBuffer.extend(sampleSweep)
            timeVector.append(time.clock()-totalStartTime)
            threadLock.release()
            print "Recieve, Start: " + repr(rxTimeStart) + " Duration: " + repr(time.clock()-rxTimeStart)
        
        print "Exiting sdrRetriever, " + repr(time.clock()-totalStartTime)

# Sets up the SDR



def main():
    
 
    root = Tk()
    root.geometry("350x300+300+300")
    app = figureWindow(root)
    root.mainloop()  

    # Start the timer
    startTime=time.clock()

    # Create new threads
    rxThread = sdrRetriever(1, sampleRate, centerFreq, gain, numSamples, numSweeps)

    rxThread.configureSDR()
    # Start recieving IQ samples

    totalStartTime=time.clock()
    rxThread.start()
    
    # Create a while loop to continually monitor when the buffer is filled.
    # When it is filled create a new thread to do the processing.
    while(1):

        if len(sampleBuffer)>0:

            threadLock.acquire()
            samplesToProcess=sampleBuffer[0:numSamples]
            del sampleBuffer[0:numSamples]
            threadLock.release()
            procThread = demodulation(1, samplesToProcess)
            procThread.start()

    print "Exiting Main Thread, " + str(time.clock-totalStartTime)


if __name__ == '__main__':
    main()
