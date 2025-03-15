from i2s import audio_out


# allocate sample array
# memoryview used to reduce heap allocation
wav_samples = bytearray(1000)
wav_samples_mv = memoryview(wav_samples)

def play_sound(file_name):
    wav = open(file_name, "rb")
    pos = wav.seek(44)  # advance to first byte of Data section in WAV file
    while True:
        num_read = wav.readinto(wav_samples_mv)
        
        if num_read == 0:  # end-of-file, advance to first byte of Data section
            break
        else:
            _ = audio_out.write(wav_samples_mv[:num_read])
            
    wav.close()
