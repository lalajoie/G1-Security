import RPi.GPIO as GPIO

relay = 12


GPIO.output(relay, 0)
time.sleep(5)
GPIO.output(relay, 1)