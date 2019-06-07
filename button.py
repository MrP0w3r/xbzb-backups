import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3,GPIO.HIGH)


while True:
    GPIO.output(3,GPIO.LOW)
    print("pressy pressy")
    time.sleep(1)
    GPIO.output(3,GPIO.HIGH)
    time.sleep(7)
    
