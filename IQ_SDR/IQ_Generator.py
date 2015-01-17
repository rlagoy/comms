# This script was designed to print I&Q samples to a text file. 
# User can specify the following inputs:
#     Sampling Rate
#     Center Frequency
#     Gain
#     Number of Samples Per Sweep
#     Number of Sweeps
# The outputs are:
#     Sample PSD plot for sample set of data
#     IQ.csv file

from rtlsdr import *
import time
import pylab
import numpy


def main():

	print ' '

	# Space Frequency
	f1 = -50000 #Hz
	# Mark Freq
	f2 = 50000 #Hz
	# Sample Rate
	sampleRate = 2.4e6#Hz
	# Baud Rate
	baud=1200.0 #sps
	# Number of Samples
	numSamples = 256*256

	packet=[1,0,1,1,0]

	samples=[]
	timeVector=[]
	bitNum=0
	timePassed=0

	for i in range(numSamples):

		timePassed=timePassed+1/sampleRate

		if (timePassed>(1/baud)):
			timePassed=0
			print(packet[bitNum])
			bitNum=bitNum+1
			if (bitNum==len(packet)):
				bitNum=0

		if(packet[bitNum]==0):
			samples.append(numpy.power(numpy.e,1j*2*numpy.pi*f1*i/sampleRate))
		
		if(packet[bitNum]==1):
			samples.append(numpy.power(numpy.e,1j*2*numpy.pi*f2*i/sampleRate))


	pylab.figure()
	pylab.psd(samples, NFFT=1024, Fc=1, Fs=sampleRate/(1e6))
	pylab.show()

	pylab.figure()
	pylab.plot(samples)
	pylab.show()

	print 'Creating IQ.csv...' + '\n'
	f=open('IQ_gen.csv','w')

	f.write('Sample Rate,' + str(sampleRate)+ '\nCenter Freq,'+str((f2+f1)/2)+ '\nGain,'+str(20)+ '\nSamples Per Sweep,'+str(numSamples)+'\nNumber of Sweeps,'+str(numSamples)+str('\n\n'))
	f.write('Time Elapsed, Sample\n')

	print 'Writing CSV data...' + '\n'

	for j in range(numSamples):
		f.write(str(j/sampleRate)+','+str(samples[j])+ '\n')
	

if __name__ == '__main__':
    main()