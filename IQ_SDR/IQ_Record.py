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


def main():
	sdr = RtlSdr()
	print ' '

	# Bandwidth/Sample Rate
	sdr.rs = 2e6
	# Center Freq
	sdr.fc = 907.941e6
	# Gain
	sdr.gain = 20
	numSamplesPerSweep = 256*256*8
	numSweeps = 7

	samples=[0]*numSweeps*numSamplesPerSweep
	timeVector=[]

	print 'Capturing data for ' + str(numSweeps) + ' sweeps...' + '\n'
	for i in range(numSweeps):
		samples[i*numSamplesPerSweep:(i+1)*numSamplesPerSweep-1]=(sdr.read_samples(numSamplesPerSweep))
		timeVector.append(time.clock())
		# print samples

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

	print 'CSV file created; program terminating...' + '\n'

	pylab.figure()
	pylab.psd(samples, NFFT=1024, Fc=sdr.fc/(1e6), Fs=sdr.rs/(1e6))
	pylab.show()

	pylab.figure()
	pylab.plot(samples)
	pylab.show()



	sdr.close()


if __name__ == '__main__':
    main()