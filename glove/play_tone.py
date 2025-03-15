import os
import math
import struct
import time

from i2s import audio_out


def mix_signal(rate, frequencies, t, bits, offset=0):
    total_samples = rate * t
    volume_reduction_factor = 32
    max_range = pow(2, bits) // 2 // volume_reduction_factor
    
    signal = []
    for i in range(total_samples):
        sample = max_range  # Start with the DC offset
        for freq in frequencies:
            sample += int((max_range - 1) * math.sin(2 * math.pi * freq * (i+offset) / rate))
        
        # Clip to avoid overflow
        sample = max(-max_range, min(max_range - 1, sample))
        
        signal.append(sample)
    return signal


def get_signal(signal, bits, audio_out, n_samples=50):
    sample_size_in_bytes = bits // 8
    format = "<" + ("h" if bits == 16 else "l") * n_samples  # Correctly builds format string
    
    packed_samples_list = []
    for i in range(0, len(signal), n_samples):
        sample_chunk = signal[i:i + n_samples]

        # Ensure the chunk is always the correct size
        if len(sample_chunk) < n_samples:
            sample_chunk += [0] * (n_samples - len(sample_chunk))  # Zero-padding

        # Ensure all samples are properly converted to integers
        sample_chunk = [int(s) for s in sample_chunk]

        packed_samples = struct.pack(format, *sample_chunk)
        packed_samples_list.append(packed_samples)
    return packed_samples_list
    audio_out.write(packed_samples)
        

#samples = make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, TONE_FREQUENCY_IN_HZ)

# continuously write tone sample buffer to an I2S DAC
frequencies = [[441], [761], [441, 761]]
#frequencies = [
#    [261.63, 329.63, 392.00],  # C Major
#    [196.00, 246.94, 392.00],  # G Major
#    [220.00, 261.63, 329.63],  # A Minor
#    [293.66, 349.23, 440.00],  # D Minor
#    [261.63, 329.63, 392.00, 466.16],  # C7
#]
def play_tones(frequencies):
    signal = mix_signal(SAMPLE_RATE_IN_HZ, fre, .1, SAMPLE_SIZE_IN_BITS, offset=0)
    


