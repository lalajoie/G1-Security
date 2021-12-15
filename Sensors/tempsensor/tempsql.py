import mysql.connector
from smbus2 import SMBus
from mlx90614 import MLX90614

mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing"
    )

mycursor = mydb.cursor()
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
sql = "INSERT INTO testing (Ambient, Object) VALUES (%d, %d)"
val = (sensor.get_ambient(), sensor.get_object)
mycursor.execute(sql, val)
mydb.commit();
bus.close()
