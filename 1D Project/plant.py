from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, BorderImage, Line
from kivy.uix.image import AsyncImage, Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
import sys
import time
import Adafruit_DHT
import Adafruit_ADS1x15
import smbus
import RPi.GPIO as io
from kivy.clock import Clock
     
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

class Plant1(App):
    def build(self,**kwargs):
        self.layout = FloatLayout(size=(300,300))
#        with self.layout.canvas:
#            BorderImage(source='GUIBackground.png',size=(800,600))
#            Line(points=[450,0,450,1000],width=2)
#            Line(points=[450,296,800,296],width=2)
            
        self.readings=Label(text='Setpoints',font_size=40,size_hint=(0.24,0.24),pos_hint={'center_x': 0.21,'center_y': 0.9})
        self.layout.add_widget(self.readings)
        
        self.TemperatureReading=Label(text='Temperature',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.83})
        self.layout.add_widget(self.TemperatureReading)
        self.ATemperatureReading=Label(text='24',background=[1,1,1,1],font_size=22,pos_hint={'center_x': 0.08,'center_y': 0.78})
        self.layout.add_widget(self.ATemperatureReading)
        
        self.LightIntensity=Label(text='Light Intensity',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.83})
        self.layout.add_widget(self.LightIntensity)
        self.ALightIntensity=Label(text='300',background=[1,1,1,1],font_size=22,pos_hint={'center_x': 0.22,'center_y': 0.78})
        self.layout.add_widget(self.ALightIntensity)
        
        self.Humidity=Label(text='Humidity',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.83})
        self.layout.add_widget(self.Humidity)
        self.AHumidity=Label(text='100',background=[1,1,1,1],font_size=22,pos_hint={'center_x': 0.36,'center_y': 0.78})
        self.layout.add_widget(self.AHumidity)
        
        self.Moisture=Label(text='Moisture',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.83})
        self.layout.add_widget(self.Moisture)
        self.AMoisture=Label(text='15000',background=[1,1,1,1],font_size=22,pos_hint={'center_x': 0.50,'center_y': 0.78})
        self.layout.add_widget(self.AMoisture)
####################               
        self.setpoints=Label(text='Actual Readings',font_size=40,size_hint=(0.24,0.24),pos_hint={'center_x': 0.135,'center_y': 0.67})
        self.layout.add_widget(self.setpoints)
        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
        self.layout.add_widget(self.Plant)
        
        self.LightIntensityL=Label(text='Light Intensity',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
        self.layout.add_widget(self.LightIntensityL)
        self.LightIntensity=Slider(min=0,max=100, size_hint=(0.4,0.10),disabled=True,pos_hint={'center_x': 0.25,'center_y': 0.55})
        self.layout.add_widget(self.LightIntensity)
        self.LightIntensityV=Label(text=str(self.LightIntensity.value),font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
        self.layout.add_widget(self.LightIntensityV)
        
        
        self.TemperatureL=Label(text='Temperature',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
        self.layout.add_widget(self.TemperatureL)
        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),disabled=True,pos_hint={'center_x': 0.25,'center_y': 0.40})
        self.layout.add_widget(self.TemperatureSlider)
        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
        self.layout.add_widget(self.TemperatureV)
        
        self.HumidityL=Label(text='Humidity',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
        self.layout.add_widget(self.HumidityL)
        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),disabled=True,pos_hint={'center_x': 0.25,'center_y': 0.25})
        self.layout.add_widget(self.HumiditySlider)
        self.HumidityV=Label(text=str(self.HumiditySlider.value),font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
        self.layout.add_widget(self.HumidityV)
        
        self.MoistureL=Label(text='Moisture',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
        self.layout.add_widget(self.MoistureL)
        self.MoistureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),disabled=True,pos_hint={'center_x': 0.25,'center_y': 0.10})
        self.layout.add_widget(self.MoistureSlider)
        self.MoistureV=Label(text=str(self.MoistureSlider.value),font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
        self.layout.add_widget(self.MoistureV)
        
        Clock.schedule_once(self.PWMstart, 1.0)
        Clock.schedule_interval(self.h_t_sensor, 2.0)
        Clock.schedule_interval(self.l_sensor, 2.0)
        Clock.schedule_interval(self.sm_sensor, 2.0)
        
        self.inc_temp = Button(text='temp',font_size=40,size_hint=(0.222,0.245),pos_hint={'center_x': 0.675,'center_y': 0.365},on_press= Clock.schedule_interval(self.adjustT, 1.0) )
        self.layout.add_widget(self.inc_temp)
        
        self.inc_moist = Button(text='moist',font_size=40,size_hint=(0.222,0.245),pos_hint={'center_x': 0.675,'center_y': 0.125},on_press=Clock.schedule_interval(self.adjustM, 1.0))
        self.layout.add_widget(self.inc_moist)
        
        self.light = Button(text='light',font_size=40,size_hint=(0.222,0.245),pos_hint={'center_x': 0.89,'center_y': 0.365},on_press=Clock.schedule_interval(self.adjustL, 1.0))
        self.layout.add_widget(self.light)
        
        self.water = Button(text='water',font_size=40,size_hint=(0.222,0.245),pos_hint={'center_x': 0.89,'center_y': 0.125},on_press=Clock.schedule_interval(self.adjustW, 1.0))
        self.layout.add_widget(self.water)
        
        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
        self.layout.add_widget(self.goback)
        

        
        return self.layout
    
    def PWMstart():
        p1.start(0)
        p2.start(0)
        p3.start(0)
        p4.start(0)
        p5.start(0)

    
    def adjustT(self,instance):
        if self.c_tempt > (self.t_tempt-0.5) and self.c_tempt < (self.t_tempt+0.5): 
            print 'Temperature is regulated'
            p2.ChangeDutyCycle(0) #hotpeltier off
            p1.ChangeDutyCycle(0) #coldpeltier off
            p3.ChangeDutyCycle(0) #backfan off
            self.Clock.schedule_interval(self.adjustT, 1.0).cancel()
        elif self.c_tempt > (self.t_tempt+0.5):
            print 'Temperature too high'
            p1.ChangeDutyCycle(100) #coldpeltier on
            p3.ChangeDutyCycle(100) #backfan on
        else:
            print 'Temperature too low'
            p2.ChangeDutyCycle(100) #hotpeltier on
        
        
    def adjustM(self,instance):
        if self.c_humidity > (self.t_humidity-0.5) and self.c_humidity < (self.t_humidity+0.5):
            print 'Humidity is regulated'
            p1.ChangeDutyCycle(0) #coldpeltier off
            p4.ChangeDutyCycle(0) #front fan off
            io.output(24, False) #water pump off (LED)
            self.Clock.schedule_interval(self.adjustM, 1.0).cancel()
        elif self.c_humidity < (self.t_humidity-0.5):
            print 'Humidity too low'
            p4.ChangeDutyCycle(100) #front fan on
            io.output(24, True) #water pump on (LED)
        else: 
            print 'Humidity too high'
            p1.ChangeDutyCycle(100) #coldpeltier on
        
    
    def adjustL(self,instance):
        if float(self.c_light_intensity) > self.t_light_intensity-0.5:
            print 'Light intensity regulated'
            io.output(23, False) #led off
            self.Clock.schedule_interval(self.adjustL, 1.0).cancel()
        else:
            print 'Light intensity too low'
            io.output(23, True) #led on
    
    def adjustW(self,instance):
        if self.c_soil_moisture < (self.t_soil_moisture-0.5):
            print 'Soil Moisture regulated'
            p5.ChangeDutyCycle(0) #water pump off (LED)
            self.Clock.schedule_interval(self.adjustW, 1.0).cancel()
        else:
            print 'Soil Moisture too low'
            p5.ChangeDutyCycle(100) #water pump on (LED)
    
    def GoBack(self,instance):
        pass
        
    
    ''''''''''''''''''''' HUMIDITY AND TEMPERATURE SENSOR '''''''''''''''''''''
    def h_t_sensor(self):
        sensor_args = { '11': Adafruit_DHT.DHT11,
                        '22': Adafruit_DHT.DHT22,
                        '2302': Adafruit_DHT.AM2302 }
        sensor = Adafruit_DHT.AM2302
        pin = '4'
        self.humidity_reading, self.temperature_reading = Adafruit_DHT.read_retry(sensor,pin)
        self.TemperatureSlider.value = self.temperature_reading
        self.HumiditySlider.value = self.humidity_reading
        
        self.c_tempt = float(self.temperature_reading)
        self.c_humidity = float(self.humidity_reading)
        
        
        
    ''''''''''''''''''''''''''''LIGHT SENSOR'''''''''''''''''''''''''''''''''
    def l_sensor(self):
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
        self.light_reading = str(readLight())
        self.LightIntensity.value = self.light_reading
#        self.LightIntensity.value = 25
        self.c_light_intensity = self.light_reading
    
       
    '''''''''''''''''''''''''''SOIL MOISTURE SENSOR'''''''''''''''''''''''''''
    def sm_sensor(self):
        adc = Adafruit_ADS1x15.ADS1115()
        GAIN = 1
        values = [0]*4
        values[0] = adc.read_adc(0, gain=GAIN)
        self.soil_reading = values[0]
        self.MoistureSlider.value = self.soil_reading
        self.c_soil_moisture = self.soil_reading
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
Plant1().run()    