
import time
import pylab
import numpy
import scipy
import scipy.signal as ss



def main():

	print ' '

	# Space Frequency
	f1 = -0.1e6 #Hz
	# Mark Freq
	f2 = 0.1e6 #Hz
	# Sample Rate
	sampleRate = 1e6#Hz
	# Baud Rate
	baud=2.0 #sps
	# Number of Samples
	numSamples = 256*256*8

	packet=[1,0]

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
	pylab.psd(samples, NFFT=1024, Fc=0, Fs=sampleRate/(1e6))
	pylab.show()

	sampleArray=numpy.array(samples)

	sampleArray.tofile('txData.bin')

if __name__ == '__main__':
    main()