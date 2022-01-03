import board
import busio as io
import adafruit_mlx90614
import mysql.connector

mydb = mysql.connector.connect (
    host = "localhost",
    user = "g1sec",
    password = "lala",
    database="testing"
    )

from time import sleep

mycursor = mydb.cursor()
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
targetTemp = "{:.2f}".format(mlx.object_temperature)

sleep(1)
sql = "INSERT INTO tempsensor (Ambient, Object) VALUES (%s, %s)"
val = (ambientTemp, targetTemp)
mycursor.execute(sql, val)
mydb.commit();
print("Ambient Temperature:", ambientTemp, "°C")
print("Target Temperature:", targetTemp,"°C")
  