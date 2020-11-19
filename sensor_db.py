import time
import mysql.connector

import board
import busio
import adafruit_tsl2591

# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

# Initialize MySQL db connection
mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    password= "logic",
    database= "LightData"
    )
mycursor = mydb.cursor()

sql_delete = "DELETE FROM raw_data WHERE time < CURRENT_TIMESTAMP - INTERVAL 1 DAY"
# condition = ("CURRENT_TIMESTAMP - INTERVAL 5 MINUTE",)
mycursor.execute(sql_delete)
mydb.commit()
print(mycursor.rowcount, "record(s) deleted")

# normalizes output to approximately the percentage of max light
n_factor  = 10/2147483647.0

count = 0
last_del = time.time()

while True:
    visible = sensor.visible*n_factor*100
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    sql = """INSERT INTO raw_data (time, visible_light)
                VALUES (%s, %s)"""
    vals = (timestamp, visible)
    mycursor.execute(sql, vals)
    mydb.commit()
    print(mycursor.rowcount, "record inserted: {}".format(vals))
    
    if (time.time() - last_del)/60 > 60:
        sql_delete = "DELETE FROM raw_data WHERE time < CURRENT_TIMESTAMP - INTERVAL 1 DAY"
        mycursor.execute(sql_delete)
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        last_del = time.time()
        
    count = count + 1
    time.sleep(2)

