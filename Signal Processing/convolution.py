# This creates a signal and then conovolves the signal with expected signals.

# Import Stuff
import scipy as sp
import matplotlib.pyplot as plt

# Create Signal

sampleRate=2e3 #Hz
signalDuration=0.5 #seconds
freq=0.1e3 #Hz
numFrequencies=100
freqBW=0.2e3
freqGuess=sp.linspace(freq-freqBW/2.0, freq+freqBW/2.0,num=numFrequencies)

maxConv=sp.zeros(numFrequencies)
numberSamples=int(signalDuration*sampleRate)
signalInterest=sp.zeros(numberSamples)
signalGuess=sp.zeros(numberSamples)

for i in range(numberSamples):
	signalInterest[i]=sp.exp(1j*freq*i)

for i in range(numFrequencies):

	for n in range(numberSamples):
		signalGuess[n]=sp.exp(1j*freqGuess[i]*n)

	maxConv[i]=sp.amax(sp.convolve(signalInterest,signalGuess))

plt.plot(freqGuess, maxConv)
plt.show()

