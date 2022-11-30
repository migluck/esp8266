# Description:  Read soil mosture level and turn on water pump if below n-percent
#               Also desplay air humidity and temperature
#
# Created two buttons
#   Button 'A' Get moisture/temp/humidity and display on OLED
#              If moisture < 50% turn on pump for 3 seconds
#   Button 'B' Turn on pump while button 'B' is held down
#
#   11/20/2022  Michael Gluck  micglu@gmail.com

from machine import Pin, SoftI2C, ADC
import ssd1306  # OLED File
from time import sleep
import time
import dht  # Temperature/Humidity sensor


# ESP8266 Pin assignment  (0,4,5,12,13,14)
soilMoisture = ADC(0)
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
pumpOFF = Pin(2, Pin.OUT)

sensor = dht.DHT11(Pin(13))
pump_button = Pin(12, Pin.IN,Pin.PULL_UP)
oled_button = Pin(14, Pin.IN,Pin.PULL_UP)
airValue=865
waterValue=450

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('Hello, World', 0, 0)
oled.show()

def runPump(t):
    pumpOFF.value(0)
    time.sleep(t)
    pumpOFF.value(1)

def clearScreen():
    oled.fill(0)
    

def dateStr(st):
    return f"{st[0]}-{st[1]}-{st[2]}"

def timeStr(st):
    return f"{st[3]}:{st[4]}:{st[5]}"

def getTime():
    time_string = time.localtime()
#    oled.text(dateStr(time_string), 0, 10)
#    oled.text(timeStr(time_string), 0, 20)
#    oled.show()
    
def getTempHumidity():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    oled.text('Temp(f): ' + str(temp_f), 0, 30)
    oled.text('Humidity: ' + str(hum), 0, 40)
    oled.show()

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def getSoilMoisture():
    adcValue=soilMoisture.read()
    moisture_pct=map_range(adcValue, airValue, waterValue, 1, 100)
    oled.text('Soil(%): ' + str(moisture_pct), 0, 50)
    oled.show()
    return moisture_pct
    
try:
    while True:
    ##############################################
    # Check Sensors when button 'OLED' pressed
    ##############################################
      pumpOFF.value(1) # Turn pump off (Switch reversed)
      if not oled_button.value():
        time.sleep_ms(20)
      if not oled_button.value():
        clearScreen()
        getTime()
        getTempHumidity()
        moist_pct = getSoilMoisture()        
        ##############################################
        # If moisture value > 50% turn pump on for n-seconds
        ##############################################
        if moist_pct < 50:  
            runPump(3)
            
        while not oled_button.value():
          time.sleep_ms(20)
      ##############################################
      # Turn pump on while button 'PUMP' is pressed
      ##############################################
      if not pump_button.value():  
          time.sleep_ms(20)
          while not pump_button.value():
              pumpOFF.value(0)
              time.sleep_ms(20)
          
          
          
except Exception as e:
    print("Exception!")
    print(e)
    pass

print("Done")
