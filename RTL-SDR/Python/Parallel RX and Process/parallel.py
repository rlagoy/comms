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
	sdr = RtlSdr()
	print ' '

	# Bandwidth/Sample Rate
	sdr.rs = 2.4e6
	# Center Freq
	sdr.fc = 901e6
	# Gain
	sdr.gain = 20
	numSamplesPerSweep = 256
	numSweeps = 256

	samples=[0]*numSweeps*numSamplesPerSweep
	timeVector=[]
	binData=[]

	print 'Capturing data for ' + str(numSweeps) + ' sweeps...' + '\n'
	for i in range(numSweeps):
		sampleSweep=sdr.read_samples(numSamplesPerSweep)
		samples[i*numSamplesPerSweep:(i+1)*numSamplesPerSweep-1]=(sampleSweep)
		timeVector.append(time.clock())
		# print samples
		transform=numpy.fft.fft(sampleSweep)

		maxInd=-1
		maxVal=-100

		for j in range(len(transform)):

			if(transform[j]>maxVal):
				maxInd=j
				maxVal=transform[maxInd]

			if (maxInd<numSamplesPerSweep/2):
				binData.append(1)
				print(0)
			else:
				binData.append(0)
				print(1)


	print 'Creating IQ.csv...' + '\n'
	f=open('IQ.csv','w')

	print 'Writing CSV data...' + '\n'

	f.write('Sample Rate,' + str(sdr.rs)+ '\nCenter Freq,'+str(sdr.fc)+ '\nGain,'+str(sdr.gain)+ '\nSamples Per Sweep,'+str(numSamplesPerSweep)+'\nNumber of Sweeps,'+str(numSweeps)+str('\n\n'))
	f.write('Time Elapsed, Sample\n')


	for i in range(numSweeps):
		for j in range(numSamplesPerSweep-1):
			f.write(str(timeVector[i]-timeVector[0]+j/sdr.rs)+','+str(samples[i*numSamplesPerSweep+j])+ '\n')
		f.write(str(timeVector[i]-timeVector[0]+j/sdr.rs)+','+str(samples[(i+1)*numSamplesPerSweep-1]) + '\n')

	f.close

	print 'CSV file created...' + '\n'



	print '\nCreating Binary.csv...' + '\n'
	f=open('Binary.csv','w')

	print 'Writing Bin data...' + '\n'

	for i in range(len(binData)):
		
		f.write(str(binData[i]) + '\n')

	f.close

	print 'Binary Data file created; program terminating...' + '\n'




	sdr.close()


if __name__ == '__main__':
    main()