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
