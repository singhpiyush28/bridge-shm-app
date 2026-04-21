import librosa
import numpy as np
from scipy.signal import butter, filtfilt
import tempfile
import os

def bandpass_filter(data, sr):

    low = 10/(sr/2)
    high = 2000/(sr/2)

    b, a = butter(4, [low, high], btype='band')

    filtered = filtfilt(b, a, data)

    return filtered


def process_audio(file):

    # Case 1: file is already a path (recorded audio)
    if isinstance(file, str) and os.path.exists(file):
        signal, sr = librosa.load(file, sr=None)

    else:
        # Case 2: uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        signal, sr = librosa.load(tmp_path, sr=None)

    # Remove DC offset
    signal = signal - np.mean(signal)

    # Filter
    filtered = bandpass_filter(signal, sr)

    time = np.arange(len(filtered)) / sr

    return signal, sr, filtered, time