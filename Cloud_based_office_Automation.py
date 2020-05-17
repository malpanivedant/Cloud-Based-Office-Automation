import time
from firebase import firebase
import RPi.GPIO as GPIO
import datetime
from firebase import firebase
import Adafruit_DHT

import urllib2, urllib, httplib
import json
import os 
from functools import partial

###########################
in1 = 15
in2 = 18

pin = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, False)
GPIO.output(in2, False)

#################################
GPIO.setmode(GPIO.BOARD)
#GPIO.cleanup()
GPIO.setwarnings(False)

sensor = Adafruit_DHT.DHT22


humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

#################################
firebase = firebase.FirebaseApplication('https://microcontroller-project-1c7ad.firebaseio.com/', None)

#################################
def update_firebase():

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		time.sleep(5)
		str_temp = ' {0:0.2f} *C '.format(temperature)	
		str_hum  = ' {0:0.2f} %'.format(humidity)
		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))	
			
	else:
		print('Failed to get reading. Try again!')	
		time.sleep(10)

	data = {"temp": temperature, "humidity": humidity}
	firebase.post('/dht', data)

#####################################
update_firebase()
while True:
    #update_firebase()
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    result_fan = firebase.get('/fan', None)
    result_light = firebase.get('/light', None)
    print (result_fan + " ")
    print (result_light + " \n")
    if(result_fan=="true"):
        GPIO.output(in1, True)
    else:
        GPIO.output(in1, False)
    if(result_light=="true"):
        GPIO.output(in2, True)
    else:
        GPIO.output(in2, False)
    
    time.sleep(2)
GPIO.cleanup()
