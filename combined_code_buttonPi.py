from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import time
import RPi.GPIO as GPIO
import serial
import base64

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

device = XBeeDevice("/dev/ttyAMA0", 9600)
device.open()

GPIO.setup(7, GPIO.OUT) #debug LED
GPIO.output(7,GPIO.LOW)

count = 1                  # number of packets recieved
full_message = ''          # string to store the messages as they arrive

while True:
    while True:
        button1 = GPIO.input(5)
        button2 = GPIO.input(16)
        button3 = False

        #if button2 == True:
        if button3 == True:
            print("sending IMAGE")
            device.send_data_broadcast("IMAGE")
            print("sent IMAGE")
            try:
                    full_message = ''                              # empty string for mesage
                    xbee_message = device.read_data(4)                           # try getting a message
                    number_packets = int(xbee_message.data.decode("utf8"))      # first message is number of packets
                    print("Number of packets: ", number_packets)
                    
                    while ( count <= number_packets ):                          # recieve messages until reaches expected number
                        
                        try:                        
                                xbee_message = device.read_data()               # read message section
                                message = xbee_message.data.decode("utf8")      # decode message to utf-8
                                                                                
                                full_message = full_message + message           # concatonate messages back into full message
                                print("count:", count)                          # count
                                count += 1                                                                               
                        except:
                                time.sleep(0.1)
                                print('...')
                                #print("ERROR count:", count)
                               # print("ERROR number packets:", count)
                                #if (count >= 20):
                                    #print("error: counted out")
                                    #break
                    count = 1
                    full_message = full_message.encode()
                    full_message = full_message.replace(b'zzzzz', b'\n')        # re-replace the z with \n in bytes
                    image_64_decode =  base64.decodestring(full_message)        # decode message from base64 
                    image_result = open('recieved_image.png', 'wb')             # create a writable image and write 
                    image_result.write(image_64_decode) 
                    image_result.close()              
            except:
                    time.sleep(0.1)
                    print('.')
                    print('..')
                    print('...')
            else:
                    break

        elif button1 == False:
            try:
                device.send_data_broadcast("DROP")
                print("sent DROP")
            except:
                print("send failed")
        
            try:
                xbee_message = device.read_data(4)
                message = xbee_message.data.decode("utf8")
                print(message)
                print("")
                GPIO.output(7,GPIO.HIGH)
                time.sleep(1)
                #time.sleep(1)
            except:
                print("NO RESPONSE")
            else:
                break
                
            print("ready")
            print("")
        
        else:
            GPIO.output(7,GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(7,GPIO.LOW)
            time.sleep(0.2)
            # Read the output power level to keep device active
            #p_level = device.get_power_level()
        
device.close()