from Adafruit_CharLCD import Adafruit_CharLCD
from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)

sensor = MLX90614(bus, address=0x5A)
print ("Ambient Temperature :", sensor.get_ambient())
print ("Object Temperature :", sensor.get_object_1())
obj = sensor.get_object_1()
strob = str(obj)
lcd.message('Temp: ' + strob)
bus.close()