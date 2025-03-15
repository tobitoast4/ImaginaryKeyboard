from machine import Pin, ADC
import time

from ble_simple_central import *

tones = ["f1", "g1", "a1", "a#1", "c2"]
pins = [2, 4, 15, 26, 27]

# Set up ADC pins (e.g., GPIO34 on ESP32)
adcs = []
for pin in pins:
    adc = ADC(pin)  # GPIO34 is an example for ESP32
    adc.width(ADC.WIDTH_10BIT)  # 10-bit resolution (0-1023 range)
    adc.atten(ADC.ATTN_0DB)  # Full-scale voltage range (0-3.3V)
    adcs.append(adc)

blueLED = Pin(23, Pin.OUT)

global_counter = 0

# Use recent values to smooth the flex sensor values
smoothed_vals = [0, 0, 0, 0, 0]
alpha = 0.2


def main():
    ble = bluetooth.BLE()
    central = BLESimpleCentral(ble)
    not_found = False

    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print("Found peripheral:", addr_type, addr, name)
            central.connect()
        else:
            nonlocal not_found
            not_found = True
            print("No peripheral found.")

    central.scan(callback=on_scan)

    # Wait for connection...
    while not central.is_connected():
        time.sleep_ms(50)
        if not_found:
            return
    print("Connected") 

    def on_rx(v):
        print("RX", v)
    central.on_notify(on_rx) 

    i = 0
    with_response = False
    while central.is_connected():
        blueLED.on()
        current_tones_str = measure_sensors()
        measure_sensors()
        try:
            print("TX", current_tones_str)
            central.write(current_tones_str, with_response)
        except Exception as e:
            print("TX failed: " + str(e))
        i += 1
        time.sleep_ms(400 if with_response else 10)
    
    print("Disconnected")    
    blueLED.off()

def measure_sensors():
    current_tones = []
    #if not global_counter % 10:
    for i, sensor in enumerate(adcs):
        raw = sensor.read()
        smoothed = alpha * raw + (1- alpha) * smoothed_vals[i]
        smoothed_vals[i] = smoothed
        if i == 0:  # Daumen
            if smoothed < 500:
                current_tones.append(tones[i])
        if i == 1:  # Zeigefinger
            if smoothed < 1000:
                current_tones.append(tones[i])
        if i == 2:  # Mittelfinger
            if smoothed < 1000:
                current_tones.append(tones[i])
        if i == 3:  # Ringfinger
            if smoothed < 950:
                current_tones.append(tones[i])
        if i == 4:  # Kleiner Finger
            if smoothed < 1010:
                current_tones.append(tones[i])
    if len(current_tones) > 0:
        tones_str = ",".join(current_tones)
    else:
        tones_str = "/"
    if tones_str == "a#1,c2":
        return "c2"
    return tones_str


while True:
    global_counter += 1
    if global_counter % 2 == 0:
        blueLED.on()
    else:
        blueLED.off()
    main()
    #current_tones_str = measure_sensors()
    #print(current_tones_str)
    #time.sleep_ms(25)
