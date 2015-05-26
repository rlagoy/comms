from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as fft


def Problem2(T=0.1e-3):
    detected = False
    threshold = 50
    ft = 2.450e9
    fs = 2e6
    f = 2.451e9
    A = 1
    dt = 1 / fs
    t = np.arange(0, T, dt)
    N = 3 * len(t)
    print 'T: ', T
    print 'N: ', len(t)
    x_reference = A * np.cos(2 * np.pi * (f - ft) * t)
    tvec = np.zeros(N)
    # plt.plot(t, x_reference)
    # plt.show()
    x_recorded = np.zeros(N)
    for x in range(len(x_recorded)):
        if x > N / 3 and x < N / 3 + len(x_reference):
            x_recorded[x] = x_reference[x % len(x_reference)]
    # plt.plot(range(3 * len(t)), x_recorded)
    # plt.show()

    noise = np.random.normal(0, 1, N)
    conv = fft.convolve(x_reference, x_recorded + noise)
    # plt.plot(range(len(conv)), conv)
    # plt.show()
    SNR = 10 * np.log10(A ** 2 / np.linalg.norm(noise) ** 2)
    print 'SNR: ', SNR, 'dB'
    maximum = conv[0]
    tau = 0
    for x in range(len(conv)):

        if conv[x] > maximum:
            maximum = np.max(conv[x])
            tau = x
    tau = tau - N

    if maximum > threshold:
        detected = True

    print 'Detected: ', detected
    return detected, SNR
    print 'Offset: ', tau
    print
    print
    print


def main():

    # Problem2(0.1e-3)
    xvec = []
    SNRvec = []
    snrthresh = 0
    # for x in np.arange(0.1e-4, .1e-2, 0.01e-3):
    #     status, SNR = Problem2(x)
    #     if status is True:
    #         snrthresh = SNR
    #         break

    for x in np.arange(0.1e-4, .1e-2, 0.01e-3):
        status, SNR = Problem2(x)
        xvec.append(x)
        SNRvec.append(SNR)

    print '\n' * 10
    print 'SNR Threshold: ', snrthresh
    print
    plt.plot(SNRvec, xvec)
    plt.xlabel('Min Detection SNR (dB)')
    plt.ylabel('Pulse Length T (sec)')
    plt.title('Pulse Length vs Min Detection SNR')
    plt.show()
if __name__ == '__main__':
    main()
