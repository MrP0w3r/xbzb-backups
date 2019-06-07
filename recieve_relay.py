import time
from digi.xbee.devices import XBeeDevice
import RPi.GPIO as GPIO

device = XBeeDevice("/dev/ttyAMA0", 9600)		# Instantiate an XBee device object.
device.open()


count = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT) #debug LED
GPIO.output(7,GPIO.LOW)

while 1:
	# Read data.
	try:
		xbee_message = device.read_data()
		message = xbee_message.data.decode("utf8")
		print(message)
		time.sleep(0.2)
		count+=1
	except:
		count+=1
	if(count%6 == 0):
		GPIO.output(7,GPIO.HIGH)
	if(count%9 == 0):
		GPIO.output(7,GPIO.LOW)
pwm.stop()
