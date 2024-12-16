import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import streamlit as st
import tempfile

st.title("Low-Pass Filter")

#the low-pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

#Main script
def main():
    st.header("Upload your audio file here :")
    uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
    
    if uploaded_file is not None:
        #temp file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        
        #Read the audio file
        fs, data = wavfile.read(temp_file_path)
        
        #converting audio to mono
        if data.ndim > 1:
            data = np.mean(data, axis=1).astype(data.dtype)
        
        st.header("Low-Pass Filter Controls")
        st.write("")
        st.write("Filter Settings:")
        st.write("")
        cutoff = st.slider("Cutoff Frequency (Hz) :", 100, 2000, 200)
        order = st.slider("Filter Order :", 1, 8, 3)
        
        #low-pass filter
        filtered_data = apply_lowpass_filter(data, cutoff, fs, order)
        
        #normalize the filtered data
        filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
        
        #Save the filtered audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as output_file:
            wavfile.write(output_file.name, fs, filtered_data)
            output_file_path = output_file.name

        #display the original and filtered signals
        st.header("Audio Signals")
        fig, ax = plt.subplots(2, 1, figsize=(12, 6))
        ax[0].plot(data, label="Original Signal",color='orange')
        ax[0].set_title("Original Signal")
        ax[1].plot(filtered_data, label="Filtered Signal", color='green')
        ax[1].set_title("Filtered Signal")
        st.pyplot(fig)
        
        #download button for the filtered audio
        st.header("Download Filtered Audio")
        with open(output_file_path, "rb") as file:
            st.download_button(
                label="Download Filtered Audio",
                data=file,
                file_name="filtered_audio.wav",
                #mime="audio/wav"
            )

if __name__ == "__main__":
    main()
