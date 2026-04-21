import matplotlib.pyplot as plt
import streamlit as st

def compare_signals(df):

    st.subheader("Dominant Frequency Comparison")

    fig, ax = plt.subplots()

    ax.bar(df["Vehicle"], df["Dominant Frequency (Hz)"])

    ax.set_ylabel("Frequency (Hz)")

    ax.set_title("Dominant Frequency Comparison")

    ax.set_xticklabels(df["Vehicle"], rotation=45)

    st.pyplot(fig)


    st.subheader("Amplitude Comparison")

    fig2, ax2 = plt.subplots()

    ax2.bar(df["Vehicle"], df["Peak Amplitude"])

    ax2.set_ylabel("Amplitude")

    ax2.set_title("Peak Amplitude Comparison")

    ax2.set_xticklabels(df["Vehicle"], rotation=45)

    st.pyplot(fig2)