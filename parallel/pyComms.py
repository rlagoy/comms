#!/usr/bin/python

from rtlsdr import *
import time
import pylab
import numpy
import threading
import time
import math


# Constants
threadLock=threading.Lock()
sampleBuffer=[]
timeVector=[]
startTime=0
elapsedTime=0
sampleRate=2.4e6
centerFreq=901e6
gain=10
numSamples=256*256
elapsedTime=1
numSweeps=int(math.ceil(numSamples/sampleRate))

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
        print "Processing, Start: " + repr(procTimeStart) + " Duration: " + repr(time.clock()-procTimeStart)
        

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
    def run(self):
        global variable, threadLock, sdr, sampleBuffer, numSamples, startTime, timeVector

        print "Starting SDRRetriever" 
        
        # Configure SDR
        print "Configure SDR"
        samples=configureSDR(self.sampleRate, self.centerFreq, self.gain, self.numSamples)
        

        for i in range(self.numSweeps):

            rxTimeStart=time.clock()
            
            # Obtain Samples
            sampleSweep=sdr.read_samples(self.numSamples)

            # Append to the buffer
            threadLock.acquire()
            sampleBuffer.extend(sampleSweep)
            timeVector.append(time.clock()-startTime)
            threadLock.release()
            print "Recieve, Start: " + repr(rxTimeStart) + " Duration: " + repr(time.clock()-rxTimeStart)
        
        print "Exiting sdrRetriever"

# Sets up the SDR
def configureSDR(sampleRate, centerFreq, gain, numSamples):
    global sdr
    sdr = RtlSdr()
    print ' '

    # Bandwidth/Sample Rate
    sdr.rs = sampleRate
    # Center Freq
    sdr.fc = centerFreq
    # Gain
    sdr.gain = gain
    numSamplesPerSweep = numSamples


def main():

    # Start the timer
    startTime=time.clock()

    # Create new threads
    rxThread = sdrRetriever(1, sampleRate, centerFreq, gain, numSamples, numSweeps)

    # Start recieving IQ samples
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

    print "Exiting Main Thread"


if __name__ == '__main__':
    main()
