import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as fft


def Problem3(T=0.1e-3):
    detected = False
    threshold = 50

    ft = 2.450e9
    fs = 2e6
    f1 = 2.450e9
    f2 = 2.452e9
    fref = 2.451e9
    A = 1
    dt = 1 / fs
    t = np.arange(0, T, dt)
    N = 3 * len(t)
    print 'T: ', T
    print 'N: ', len(t)
    x_reference = A * np.cos(2 * np.pi * (fref - ft) * t)
    tvec = np.zeros(N)
    # plt.plot(t, x_reference)
    # plt.show()

    noise = np.random.normal(0, 1, N)

    for f in np.arange(f1, f2, .001e9):
        x_insert = A * np.cos(2 * np.pi * (f - ft) * t)
        x_recorded = np.zeros(N)
        for x in range(len(x_recorded)):
            if x > N / 3 and x < N / 3 + len(x_insert):
                x_recorded[x] = x_insert[x % len(x_insert)]
        # plt.plot(range(3 * len(t)), x_recorded)
        # plt.show()
        conv = fft.convolve(x_reference, x_recorded + noise)
        # plt.plot(range(len(conv)), conv)
        # plt.show()
        maximum = conv[0]
        for x in range(len(conv)):

            if conv[x] > maximum:
                maximum = np.max(conv[x])

            if maximum > threshold:
                detected = True

    print 'Detected: ', detected
    SNR = 10 * np.log10(A ** 2 / np.linalg.norm(noise) ** 2)
    print 'SNR: ', SNR, 'dB'
    return detected, SNR


def main():

    # Problem2(0.1e-3)
    xvec = []
    SNRvec = []
    snrthresh = 0
    for x in np.arange(0.1e-4, .1e-2, 0.01e-3):
        status, SNR = Problem3(x)
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
