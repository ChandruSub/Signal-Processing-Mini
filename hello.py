from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt

# Specify the file path (ensure the path is correct)
file_path = r"C:\Users\Flip\Downloads\run-vine-sound-effect.mp3"  # Use raw string to avoid Unicode errors

# Verify FFmpeg configuration
try:
    ffmpeg_path = AudioSegment.converter
    if not ffmpeg_path:
        raise Exception("FFmpeg is not configured properly. Ensure it is installed and in PATH.")
    print(f"FFmpeg is configured at: {ffmpeg_path}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Load the audio file
try:
    audio = AudioSegment.from_file(file_path)
    print(f"Audio loaded successfully: {file_path}")
except Exception as e:
    print(f"Error loading audio file: {e}")
    exit()

# Convert the audio to mono
audio = audio.set_channels(1)

# Convert the audio to a NumPy array
samples = np.array(audio.get_array_of_samples())

# Downsample the audio for quicker visualization
downsample_factor = 10
samples = samples[::downsample_factor]

# Create the time axis for the downsampled waveform
time_axis = np.linspace(0, len(samples) * downsample_factor / audio.frame_rate, num=len(samples))

# Plot the waveform
plt.figure(figsize=(10, 4))
plt.plot(time_axis, samples, color="blue")
plt.title("Audio Waveform (Mono, Downsampled)")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid()
plt.tight_layout()
plt.show()
