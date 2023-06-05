# Temperature and Humidity Sensor
import dht
from machine import Pin
from time import sleep
import network
import urequests

# Global Variables
sensor = dht.DHT11(Pin(14))  # Sensor's data pin
SSID = 'WestwoodHome'
SSID_KEY = 'MayaAnnie'
thingspeak_api_key = 'EM8XL3ONUI7839DQ'


# Function to connect to WiFi
# https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_KEY)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Connect to WiFi
do_connect()

while True:
  try:
    sleep(600)  # 10 minutes
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    # print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
  except OSError as e:
    print('Failed to read sensor.')

  try:
    URL = ("https://api.thingspeak.com/update?api_key=" +
                 thingspeak_api_key + 
                 "&field1=" + str(temp_f) +
                 "&field2=" + str(hum))
    #URL = 'https://api.thingspeak.com/update?api_key=EM8XL3ONUI7839DQ&field1=50;field2=75'

    print('Send data to ThingSpeak')
    req = urequests.get(URL)    
    print('Status: ' + str(req.status_code))
  except OSError as e:
    print('Failed to send data to ThingSpeak.')

