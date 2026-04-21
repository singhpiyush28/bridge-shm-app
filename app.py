import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tempfile

from audio_processing import process_audio
from feature_extraction import extract_features
from comparison import compare_signals
from classification import classify_bridge

# NEW: audio recorder
from audiorecorder import audiorecorder

st.title("Bridge Vibration Analyzer (SHM System)")

st.subheader("Upload OR Record Vehicle Audio")

# --------- RECORD AUDIO ---------
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    st.success("Recording complete")

    # Save recording
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.export().read())
        file_path = f.name

    # Save to session (multiple recordings)
    st.session_state.recordings.append(("Recorded " + str(len(st.session_state.recordings)+1), file_path))

    st.audio(file_path)
# --------- CLEAR RECORDINGS BUTTON ---------
if st.button("Clear Recordings"):
    st.session_state.recordings = []

# --------- FILE UPLOAD ---------
uploaded_files = st.file_uploader(
    "Upload vehicle audio recordings",
    accept_multiple_files=True
)

results = []

files_to_process = []

# Add all recorded files
for rec in st.session_state.recordings:
    files_to_process.append(rec)

# Add uploaded files
if uploaded_files:
    for file in uploaded_files:
        files_to_process.append((file.name, file))

# --------- PROCESS FILES ---------
if files_to_process:

    for name, file in files_to_process:

        signal, sr, filtered, time = process_audio(file)

        freq, fft_amp, dom_freq, peak_amp = extract_features(filtered, sr)

        status = classify_bridge(dom_freq)

        results.append({
            "Vehicle": name,
            "Dominant Frequency (Hz)": dom_freq,
            "Peak Amplitude": peak_amp,
            "Status": status
        })

        st.subheader(name)

        st.subheader(f"{name} - Original Signal")

        fig0, ax0 = plt.subplots()
        ax0.plot(time, signal)
        ax0.set_title("Original Audio Signal")
        ax0.set_xlabel("Time (s)")
        ax0.set_ylabel("Amplitude")
        st.pyplot(fig0)


# -------- FILTERED SIGNAL --------
        st.subheader(f"{name} - Filtered Signal")

        fig1, ax1 = plt.subplots()
        ax1.plot(time, filtered)
        ax1.set_title("Filtered Vibration Signal (10–2000 Hz)")
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Amplitude")
        st.pyplot(fig1)


# -------- FREQUENCY SPECTRUM --------
        st.subheader(f"{name} - Frequency Spectrum")

        fig2, ax2 = plt.subplots()
        ax2.plot(freq, fft_amp)
        ax2.set_xlim(0, 2000)
        ax2.set_title("FFT Spectrum")
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Amplitude")
        st.pyplot(fig2)
# ===== AFTER LOOP ENDS =====

if results:
    df = pd.DataFrame(results)

    st.subheader("Comparison Table")
    st.dataframe(df)

    # Comparison graph
    compare_signals(df)

    # -------- FINAL DECISION DISPLAY --------
    st.subheader("Bridge Condition Analysis")

    for result in results:
        st.write(f"Vehicle: {result['Vehicle']}")
        st.write(f"Dominant Frequency: {result['Dominant Frequency (Hz)']:.2f} Hz")
        st.write(f"Peak Amplitude: {result['Peak Amplitude']:.2f}")

        # Status color display
        if result['Status'] == "Unsafe":
            st.error("Unsafe Condition ⚠️")
        elif result['Status'] == "Moderate":
            st.warning("Moderate Condition ⚠️")
        else:
            st.success("Safe Condition ✅")

        st.markdown("---")
