import numpy as np

def extract_features(signal, sr):

    N = len(signal)

    fft = np.fft.fft(signal)

    fft = np.abs(fft[:N//2])

    freq = np.fft.fftfreq(N, 1/sr)

    freq = freq[:N//2]

    idx = np.argmax(fft)

    dominant_frequency = freq[idx]

    peak_amplitude = fft[idx]

    return freq, fft, dominant_frequency, peak_amplitude