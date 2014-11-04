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
	f1 = 2e4 #Hz
	# Sample Rate
	sampleRate = 2e6#Hz

	# Number of Samples
	numSamples = 256

	packet=[0]

	samples=[]
	timeVector=[]
	bitNum=0
	timePassed=0

	for i in range(numSamples):

		samples.append(numpy.power(numpy.e,1j*2*numpy.pi*f1*i/sampleRate))
		

	pylab.figure()
	pylab.psd(samples, NFFT=256, Fc=1, Fs=sampleRate/(1e6))
	pylab.show()


	pylab.figure()
	pylab.plot(samples)
	pylab.show()

	pylab.figure()
	pylab.plot(numpy.fft.fft(samples,8))
	pylab.show()



	

if __name__ == '__main__':
    main()