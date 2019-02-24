# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:32:59 2017

@author: gorilagila
"""
from firebase import firebase
url = "https://padiworld-84347.firebaseio.com/" # URL to Firebase database
token = "QTaA7OMmsgQ8uHGxz9c2wYpOliqem0QrFWGLvfkD" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

import sys
import time
import Adafruit_DHT
import Adafruit_ADS1x15
import smbus
import RPi.GPIO as io
from libdw import sm

io.setmode(io.BCM)

#1 = cold peltier (20)
#2 = hot peltier (19)
#3 = back fan (18)
#4 = fron fan (17)
#5 = led  (23)
#6 = water pump (24)
 
in1_pin = 20
in2_pin = 19
in3_pin = 18
in4_pin = 17
in5_pin = 23
in6_pin = 24
 
io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)
io.setup(in4_pin, io.OUT)
io.setup(in5_pin, io.OUT)
io.setup(in6_pin, io.OUT)

p1 = io.PWM(20,100) 
p2 = io.PWM(19,100)   
p3 = io.PWM(18,100)
p4 = io.PWM(17,100)
io.output(23, False)
p5 = io.PWM(24,100)


''''''''''''''''''''' HUMIDITY AND TEMPERATURE SENSOR '''''''''''''''''''''

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
sensor = Adafruit_DHT.AM2302
pin = '4'

humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)

    
''''''''''''''''''''''''''''LIGHT SENSOR'''''''''''''''''''''''''''''''''

DEVICE     = 0x23 

POWER_DOWN = 0x00 
POWER_ON   = 0x01 
RESET      = 0x07 

CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)

def convertToNumber(data):
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

   
'''''''''''''''''''''''''''SOIL MOISTURE SENSOR'''''''''''''''''''''''''''

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

values = [0]*4

values[0] = adc.read_adc(0, gain=GAIN)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#system's logic
#tempt inc = cold peltier on, back fan on
#tempt dec = hot peltier on
#humidity inc = cold peltier on
#humidity dec = water pump on, front fan on
#light intensity inc = -
#light intensity dec = led on
#soil sensor inc = -
#soil sensor dec = water pump on

#1 = cold peltier
#2 = hot peltier
#3 = back fan
#4 = fron fan
#5 = led
#6 = water pump
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)
p5.start(0)

t_tempt = 24
t_humidity = 64
t_light_intensity = 300 
t_soil_moisture = 15000 





try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor,pin) #humidity, temperature readings
        c_tempt = round(float(temperature),2) #current temperature
        c_humidity = round(float(humidity),2) #current humidity
        c_light_intensity = round(readLight(),2) #current light intensity
        c_soil_moisture = adc.read_adc(0, gain=GAIN) #current soil moisture
        
        #updating firebase datas of the current surrounding conditions
        firebase.put('/','GameMaster/Plant1/tempt',c_tempt)
        firebase.put('/','GameMaster/Plant1/humidity',c_humidity)
        firebase.put('/','GameMaster/Plant1/light intensity',c_light_intensity)
        firebase.put('/','GameMaster/Plant1/soil moisture', c_soil_moisture)
        
        print('Temp : {0:0.1f}  Humidity : {1:0.1f}%'.format(temperature, humidity))
        print "Light Level : {0:0.1f} lx".format(c_light_intensity)
        print "Soil Moisture : {0:0.1f}".format(adc.read_adc(0, gain=GAIN))
        print "\n"
      
     
#TEMPERATURE ACTUATOR'S OUTPUT
        
        if c_tempt > (t_tempt-0.5) and c_tempt < (t_tempt+0.5): 
            print 'Temperature is regulated'
            firebase.put('/','GameMaster/Plant1/tempt switch','off')
            p2.ChangeDutyCycle(0) #hotpeltier off
            p1.ChangeDutyCycle(0) #coldpeltier off
            p3.ChangeDutyCycle(0) #backfan off
            print '    Peltier OFF, Back Fan OFF'
            
        else:
            if c_tempt > (t_tempt+0.5):
                print 'Temperature too high'
                if firebase.get('/GameMaster/Plant1/tempt switch') == "on":
                    p1.ChangeDutyCycle(100) #coldpeltier on
                    p3.ChangeDutyCycle(100) #backfan on
                    print '    Cold Peltier ON, Back Fan ON' 
                    p2.ChangeDutyCycle(0) #hotpeltier off
                else:
                    print '    Cold Peltier OFF, Back Fan OFF'
            else:
                print 'Temperature too low'
                if firebase.get('/GameMaster/Plant1/tempt switch') == "on":
                    p2.ChangeDutyCycle(100) #hotpeltier on
                    p1.ChangeDutyCycle(0) #coldpeltier off
                    print '    Hot Peltier ON' 
                    p3.ChangeDutyCycle(0) #backfan off
                else:
                    print '    Hot Peltier OFF'
            
#HUMIDITY ACTUATOR'S OUTPUT
        
        if c_humidity > (t_humidity-0.5) and c_humidity < (t_humidity+0.5):
            print 'Humidity is regulated'
            firebase.put('/','GameMaster/Plant1/humidity switch','off')
            p1.ChangeDutyCycle(0) #coldpeltier off
            p4.ChangeDutyCycle(0) #front fan off
            p5.ChangeDutyCycle(0) #water pump off 
            print '    Peltier OFF, Fan OFF, Water Pump OFF'
        else:
            if c_humidity < (t_humidity-0.5):
                print 'Humidity too low'
                if firebase.get('/GameMaster/Plant1/humidity switch') == "on":
                    p1.ChangeDutyCycle(0) #coldpeltier off
                    p3.ChangeDutyCycle(0) #back fan off
                    p4.ChangeDutyCycle(100) #front fan on
                    p5.ChangeDutyCycle(50) #water pump on 
                    print '    Front Fan ON, Water Pump ON'
                else:
                    print '    Front Fan OFF, Water Pump OFF' 
            else: 
                print 'Humidity too high'
                if firebase.get('/GameMaster/Plant1/humidity switch') == "on":
                    p1.ChangeDutyCycle(100) #coldpeltier on
                    p3.ChangeDutyCycle(100) #back fan on
                    p4.ChangeDutyCycle(0) #front fan off
                    p5.ChangeDutyCycle(0) #water pump off 
                    print '    Cold Peltier ON, Back Fan ON'
                else:
                    print '    Cold Peltier OFF, Back Fan OFF' 

#LIGHT INTENSITY ACTUATOR'S OUTPUT
        
        if float(c_light_intensity) > t_light_intensity-0.5:
            print 'Light intensity regulated'
            firebase.put('/','GameMaster/Plant1/light intensity switch','off')
            io.output(23, False) #led off
            print '    LED Light OFF'
        else:
            print 'Light intensity too low'
            if firebase.get('/GameMaster/Plant1/light intensity switch') == "on":
                io.output(23, True) #led on
                print '    LED Light ON'
            else:
                print '    LED Light OFF'
        
#SOIL MOISTURE ACTUATOR'S OUTPUT
        
        if c_soil_moisture < (t_soil_moisture-0.5):
            print 'Soil Moisture regulated'
            firebase.put('/','GameMaster/Plant1/soil moisture switch','off')
            p5.ChangeDutyCycle(0) #water pump off
            print '    Water Pump OFF'
        else:
            print 'Soil Moisture too low'
            if firebase.get('/GameMaster/Plant1/soil moisture switch') == "on":
                p5.ChangeDutyCycle(100) #water pump on
                print '    Water Pump ON'
            else:
                print '    Water Pump OFF'
                
        time.sleep(0.5) #it will check the current condition every 0.5 seconds, however
                        #due to hardware and firebase connection, there is extra delay occured.

  
                            
except KeyboardInterrupt:
    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()
    p5.stop()
    io.cleanup()
          

        
        
        
        
        
        
        
        
        
        
        
