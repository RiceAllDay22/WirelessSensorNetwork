from machine import Pin
import time

# Pin D9 (ON/SLEEP/DIO9)
LED_PIN_ID = "D16"
led_pin = Pin(LED_PIN_ID, Pin.OUT, value=0)

while True:
    print("- LED OFF")
    led_pin.value(0)
    time.sleep(0.1)

    print("- LED ON")
    led_pin.value(1)
    time.sleep(0.1)
