import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

# Define the low-pass filter
def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Main script
def main():
    # Input file
    input_file = r"C:\Users\Flip\Downloads\let-her-go.wav"
    output_file = r"C:\Users\Flip\Downloads\output2.wav"
    
    # Read the audio file
    fs, data = wavfile.read(input_file)
    
    # Handle stereo audio by converting to mono (if needed)
    if data.ndim > 1:
        data = np.mean(data, axis=1).astype(data.dtype)
    
    # Filter settings
    cutoff = 500.0  # Cutoff frequency in Hz
    order = 6        # Filter order
    
    # Apply the low-pass filter
    filtered_data = apply_lowpass_filter(data, cutoff, fs, order)
    
    # Normalize the filtered data
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)
    
    # Save the filtered audio
    wavfile.write(output_file, fs, filtered_data)
    
    # Plot original and filtered signals
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(data, label="Original Signal")
    plt.title("Original Signal")
    plt.subplot(2, 1, 2)
    plt.plot(filtered_data, label="Filtered Signal", color='orange')
    plt.title("Filtered Signal")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
