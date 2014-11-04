
import time
import pylab
import numpy

f=open('IQ_gen.csv','r')

samples=[]
fftSamples=256

f.readline()
data=0;

for line in f.readlines():

	strings=line.partition(",")

	if (data==1):
		samples.append(complex(strings[2]))

	if (strings[0]=='Time Elapsed' or data==1):
		data=1

binData=[]

for i in range(len(samples)/fftSamples):

	transform=numpy.fft.fft(samples[i*fftSamples:(i+1)*fftSamples-1])

	maxInd=-1
	maxVal=-100

	for j in range(len(transform)):

		if(transform[j]>maxVal):
			maxInd=j
			maxVal=transform[maxInd]

	if (maxInd<fftSamples/2):
		binData.append(1)
	else:
		binData.append(0)

pylab.figure()
pylab.plot(binData)
pylab.show()


f.close()
