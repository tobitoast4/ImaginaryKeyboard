# For the glove

import os, struct
from machine import I2S
from machine import Pin


# ======= I2S CONFIGURATION =======
SCK_PIN = 13   # BCLK
WS_PIN = 12    # LRC
SD_PIN = 14    # DIN	
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 5000
# ======= I2S CONFIGURATION =======

# ======= AUDIO CONFIGURATION =======
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.STEREO
SAMPLE_RATE_IN_HZ = 22_500
# ======= AUDIO CONFIGURATION =======

audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# Function to convert bytearray to integers (with little-endian byte order)
def bytearray_to_ints_little_endian(byte_array, chunk_size=2):
    int_list = []
    for i in range(0, len(byte_array), chunk_size):
        # Unpack the chunk as a little-endian 2-byte integer
        chunk = byte_array[i:i+chunk_size]
        if len(chunk) == chunk_size:
            # Use struct to unpack using little-endian format for 2-byte unsigned short
            int_list.append(struct.unpack('<H', chunk)[0])  # '<H' means little-endian 2-byte unsigned short
    return int_list


def ints_to_bytearray_little_endian(int_list):
    byte_array = bytearray()
    for value in int_list:
        # Pack the integer as a little-endian 2-byte unsigned short ('<H')
        byte_array.extend(struct.pack('<H', value))
    return byte_array



wav1 = open("c1.wav", "rb")
pos = wav1.seek(44)  # advance to first byte of Data section in WAV file

wav2 = open("a1.wav", "rb")
pos = wav2.seek(44)  # advance to first byte of Data section in WAV file

# allocate sample array
# memoryview used to reduce heap allocation
wav_samples = bytearray(1000)
wav_samples_mv = memoryview(wav_samples)

# continuously read audio samples from the WAV file
# and write them to an I2S DAC
print("==========  START PLAYBACK ==========")
# try:
while True:
    num_read = wav1.readinto(wav_samples_mv)
    
    # Convert bytearray to little-endian integers (4-byte chunks in this case)
    int_array_little_endian = bytearray_to_ints_little_endian(bytes(wav_samples_mv))
    # # Print the result
    wav_samples_mv2 = ints_to_bytearray_little_endian(int_array_little_endian)
    
    
    #result = bytearray([b1 + b2 for b1, b2 in zip(bytes(wav_samples_mv), bytes(wav_samples_mv))])
    #for _ in range(1000): pass


    # end of WAV file?
    if num_read == 0:
        # end-of-file, advance to first byte of Data section
        _ = wav1.seek(44)
    else:
        _ = audio_out.write(wav_samples_mv[:num_read])

# except (KeyboardInterrupt, Exception) as e:
#     print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
wav1.close()
audio_out.deinit()
print("Done")
