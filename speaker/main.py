from peripheral import BLESimplePeripheral, queue
import bluetooth
#from sound import play_tones
from play_tone import mix_signal, get_signal, audio_out
from play_sound import play_sound

import time

import _thread


note_frequencies = {
    "f1": 349.23,
    "f#1": 369.99,
    "g1": 392.00,
    "g#1": 415.30,
    "a1": 440.00,  # Standard A4 reference pitch
    "a#1": 466.16,
    "b1": 493.88,
    "c2": 523.25,
    "/": 0
}

frequencies = [0]
packed_samples_list = []
lock = _thread.allocate_lock()


def play_audio():
    global packed_samples_list
    while True:
        for packed_samples in packed_samples_list:
            audio_out.write(packed_samples)


ble = bluetooth.BLE()
p = BLESimplePeripheral(ble)

def on_rx(v):
    #print(f'Received {v}')
    global frequencies
    global packed_samples_list
    global note_frequencies
    with lock:
        tones = str(v)[2:-1].split(",")
        new_frequencies = [note_frequencies[tone] for tone in tones]
        if new_frequencies != frequencies:
            frequencies = new_frequencies
            if frequencies[0] == 0:
                packed_samples_list = []
                return
            signal = mix_signal(22_050, frequencies, 0.05, 16, offset=0)
            packed_samples_list = get_signal(signal, 16, audio_out, n_samples=50)

p.on_write(on_rx)

_thread.start_new_thread(play_audio, ())

connected = False

while True:
    while not p.is_connected():
        connected = False
        play_sound("BLE_waiting.wav")
        print("Waiting for central ...")
        time.sleep(1)

    if not connected:  # flag not yet set
        connected = True
        play_sound("BLE_success.wav")
    time.sleep(1)
