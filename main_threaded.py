import _thread
import time
import os
import math
import struct
from machine import I2S
from machine import Pin

from peripheral import *


SAMPLE_SIZE_IN_BITS = 16
if SAMPLE_SIZE_IN_BITS == 16:
    BIT_FORMAT = "<h"
else:  # assume 32 bits
    BIT_FORMAT = "<l"

def make_tone(rate, frequency):
    # create a buffer containing the pure tone samples
    array_length = rate // frequency
    volume_reduction_factor = 32
    range = pow(2, SAMPLE_SIZE_IN_BITS) // 2 // volume_reduction_factor
    samples_int = []
    for i in range(array_length):
        sample = range + int((range - 1) * math.sin(2 * math.pi * i / array_length))
        samples_int.append(sample)
    return samples_int

def generate_byte_array_from_ints(integer_array):
    sample_size_in_bytes = SAMPLE_SIZE_IN_BITS // 8
    samples = bytearray(len(integer_array) * sample_size_in_bytes)
    for i in range(len(integer_array)):
        sample = integer_array[i]
        struct.pack_into(BIT_FORMAT, samples, i * sample_size_in_bytes, sample)
    return samples




# ======= I2S CONFIGURATION =======
SCK_PIN = 13   # BCLK
WS_PIN = 12    # LRC
SD_PIN = 14    # DIN
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 2000
# ======= I2S CONFIGURATION =======


# ======= AUDIO CONFIGURATION =======
FORMAT = I2S.MONO  # only MONO supported in this example
SAMPLE_RATE_IN_HZ = 22_050
# ======= AUDIO CONFIGURATION =======

audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)


samples_int_f1 = make_tone(SAMPLE_RATE_IN_HZ, 350)
samples_int_g1 = make_tone(SAMPLE_RATE_IN_HZ, 392)
samples_int_a1 = make_tone(SAMPLE_RATE_IN_HZ, 441)
samples_int_ais1 = make_tone(SAMPLE_RATE_IN_HZ, 466)
samples_int_c2 = make_tone(SAMPLE_RATE_IN_HZ, 523)
samples = generate_byte_array_from_ints(samples_int_f1)


counter = 0

def mix_audios(current_tones_str):
    mixed_array = []
    for i in range(256):
        value_f1 = 0
        value_g1 = 0
        value_a1 = 0
        value_ais1 = 0
        value_c2 = 0
        tones = ""
        if "f1" in current_tones_str:
            value_f1 = samples_int_f1[i % len(samples_int_f1)]
            tones += "f1"
        if "g1" in current_tones_str:
            value_g1 = samples_int_g1[i % len(samples_int_g1)]
            tones += "g1"
        if "a1" in current_tones_str:
            value_a1 = samples_int_a1[i % len(samples_int_a1)]
            tones += "a1"
        if "a#1" in current_tones_str:
            value_ais1 = samples_int_ais1[i % len(samples_int_ais1)]
            tones += "a#1"
        if "c2" in current_tones_str:
            value_c2 = samples_int_c2[i % len(samples_int_c2)]
            tones += "c2"
        mixed_array.append(value_f1 + value_g1 + value_a1 + value_ais1 + value_c2)
    samples = generate_byte_array_from_ints(mixed_array)
    return samples


current_tones_str = ""
lock = _thread.allocate_lock()
samples = mix_audios(current_tones_str)

def play_audio():
    global samples
    while True:
        num_written = audio_out.write(samples)


ble = bluetooth.BLE()
p = BLESimplePeripheral(ble)

def on_rx(v):
    global current_tones_str
    global samples
    new_current_tones_str = str(v)[2:-1]
    if new_current_tones_str != current_tones_str:
        with lock:  # Ensures only one thread modifies `counter` at a time
            current_tones_str = str(v)[2:-1]
            samples = mix_audios(current_tones_str)
        print(current_tones_str)

p.on_write(on_rx)


# Start the thread
_thread.start_new_thread(play_audio, ())

# Main loop
while True:
    time.sleep(5)

