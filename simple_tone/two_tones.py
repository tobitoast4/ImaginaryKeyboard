# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:  Play a pure audio tone out of a speaker or headphones
#
# - write audio samples containing a pure tone to an I2S amplifier or DAC module
# - tone will play continuously in a loop until
#   a keyboard interrupt is detected or the board is reset
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S

import os
import math
import struct
from machine import I2S
from machine import Pin

import uasyncio as asyncio
import time


SAMPLE_SIZE_IN_BITS = 16
if SAMPLE_SIZE_IN_BITS == 16:
    BIT_FORMAT = "<h"
else:  # assume 32 bits
    BIT_FORMAT = "<l"

def make_tone(rate, frequency):
    # create a buffer containing the pure tone samples
    array_length = rate // frequency
    volume_reduction_factor = 16
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
print(len(samples_int_f1))
print(len(samples_int_g1))
print(len(samples_int_a1))
print(len(samples_int_ais1))
print(len(samples_int_c2))

async def thread_function():
    global samples
    global counter
    counter = 0
    while True:
        counter += 1
        print(counter)
        mixed_array = []
        for i in range(100):
            value_f1 = 0
            value_g1 = 0
            value_a1 = 0
            value_ais1 = 0
            value_c2 = 0
            if counter < 200:
                value_f1 = samples_int_f1[i % len(samples_int_f1)]
            if counter > 200 and counter < 400:
                value_g1 = samples_int_g1[i % len(samples_int_g1)]
            if counter > 400 and counter < 600:
                value_a1 = samples_int_a1[i % len(samples_int_a1)]
            if counter > 600 and counter < 800:
                value_ais1 = samples_int_ais1[i % len(samples_int_ais1)]
            if counter > 800 and counter < 1000:
                value_c2 = samples_int_c2[i % len(samples_int_c2)]
            mixed_array.append(value_f1 + value_g1 + value_a1 + value_ais1 + value_c2)
        samples = generate_byte_array_from_ints(mixed_array)
        await asyncio.sleep(1/100)

async def play_audio():
    while True:
        global samples
        num_written = audio_out.write(samples)
        await asyncio.sleep(1/1000000)


async def main():
    # Create tasks and run them concurrently
    task1_coroutine = asyncio.create_task(thread_function())
    task2_coroutine = asyncio.create_task(play_audio())


    # Run the tasks forever
    await asyncio.gather(task1_coroutine, task2_coroutine)

# Run the event loop
asyncio.run(main())