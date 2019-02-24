import sys
import time
import Adafruit_DHT

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
sensor = Adafruit_DHT.AM2302
pin = '4'

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
    time.sleep(0.5)
