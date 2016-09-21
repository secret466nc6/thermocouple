import paho.mqtt.client as mqtt
import msgpack

import time
import numpy as np
from io import BytesIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
# global
messgeindex = 0
connected = 0
MOLD_UPSIDE_PLAT_FLAG  = (0x01)
MOLD_TIMESTAMP_FLAG    = (0x02)
MOLD_AMBIENT_TEMP_FLAG = (0x04)
# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
DO  = 18
CLK = 23
CS0 = 24
CS1 = 25
CS2 = 8
CS3 = 7

sensor0 = MAX31855.MAX31855(CLK, CS0, DO)
sensor1 = MAX31855.MAX31855(CLK, CS1, DO)
sensor2 = MAX31855.MAX31855(CLK, CS2, DO)
sensor3 = MAX31855.MAX31855(CLK, CS3, DO)


#DO2  = 4
#CLK2 = 17
CS4 = 12
CS5 = 16
CS6 = 20
CS7 = 21

sensor4 = MAX31855.MAX31855(CLK, CS4, DO)
sensor5 = MAX31855.MAX31855(CLK, CS5, DO)
sensor6 = MAX31855.MAX31855(CLK, CS6, DO)
sensor7 = MAX31855.MAX31855(CLK, CS7, DO)


CS8 = 4
CS9 = 17
CS10 = 27
CS11 = 22

sensor8 = MAX31855.MAX31855(CLK, CS8, DO)
sensor9 = MAX31855.MAX31855(CLK, CS9, DO)
sensor10 = MAX31855.MAX31855(CLK, CS10, DO)
sensor11 = MAX31855.MAX31855(CLK, CS11, DO)


CS12 = 6
CS13 = 13
CS14 = 19
CS15 = 26

sensor12 = MAX31855.MAX31855(CLK, CS12, DO)
sensor13 = MAX31855.MAX31855(CLK, CS13, DO)
sensor14 = MAX31855.MAX31855(CLK, CS14, DO)
sensor15 = MAX31855.MAX31855(CLK, CS15, DO)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    global connected
    print("Connected with result code "+str(rc))
    connected = 1
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    global messgeindex
    messgeindex += 1
    print("Total publish count: ", messgeindex)

# Pack sensor data by messagepack lib and do the MQTT publish
def do_mqtt_publish(client, hdr_flag, s_v, s_ambient):
    global MOLD_TIMESTAMP_FLAG
    global MOLD_AMBIENT_TEMP_FLAG
    # get the length of plat and sensor from s_v
    vec = np.array(s_v)
    plat_length = vec.shape[0]
    sensor_length = vec.shape[1]
    # construct header
    hdr_num = plat_length * sensor_length
    hdr_payloadlength = hdr_num * 4
    timestamp = int(time.time())

    # set payload length
    if (hdr_flag & MOLD_TIMESTAMP_FLAG) == MOLD_TIMESTAMP_FLAG:
        hdr_payloadlength += 8
    if (hdr_flag & MOLD_AMBIENT_TEMP_FLAG) == MOLD_AMBIENT_TEMP_FLAG:
        hdr_payloadlength += 4

    buf = BytesIO()
    # pack header
    buf.write(msgpack.packb(int(hdr_flag)))
    buf.write(msgpack.packb(int(hdr_num)))
    buf.write(msgpack.packb(int(hdr_payloadlength)))

    # pack sensor data
    for i in range(plat_length):
        for y in range(sensor_length):
            buf.write(msgpack.packb(float(vec[i][y])))
     
    # pack timestamp   
    if (hdr_flag & MOLD_TIMESTAMP_FLAG) == MOLD_TIMESTAMP_FLAG:
        buf.write(msgpack.packb(int(timestamp)))
    # ambient temperature
    if (hdr_flag & MOLD_AMBIENT_TEMP_FLAG) == MOLD_AMBIENT_TEMP_FLAG:
        buf.write(msgpack.packb(float(s_ambient)))

    buf.seek(0)
    client.publish("MOS/MOLD/TEMPERATURE/1234567890", bytearray(buf.getvalue()));

def main():
    global MOLD_UPSIDE_PLAT_FLAG
    global MOLD_TIMESTAMP_FLAG
    global MOLD_AMBIENT_TEMP_FLAG
    global connected
    client = mqtt.Client(client_id="ccu_sensor_hub1", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.username_pw_set("admin", "kK123")
    client.connect("140.113.213.86", 61613)

    rc = 0
    while rc == 0:
        if connected == 1:
            temp0 = sensor0.readTempC()
            temp1 = sensor1.readTempC()
            temp2 = sensor2.readTempC()
            temp3 = sensor3.readTempC()
            temp4 = sensor4.readTempC()
            temp5 = sensor5.readTempC()
            temp6 = sensor6.readTempC()
            temp7 = sensor7.readTempC()
	    temp8 = sensor8.readTempC()
            temp9 = sensor9.readTempC()
            temp10 = sensor10.readTempC()
            temp11 = sensor11.readTempC()
            temp12 = sensor12.readTempC()
            temp13 = sensor13.readTempC()
            temp14 = sensor14.readTempC()
            temp15 = sensor15.readTempC()	    

            sensor_data1 = [ [temp0,temp1,temp2,temp3], [temp4,temp5,temp6,temp7], [temp8,temp9,temp10,temp11], [temp12,temp13,temp14,temp15] ]
            sensor_data2 = [ [15,14,13,12], [11,10,9,8], [7,6,5,4], [3,2,1,0] ]
            # publish upside plat data
            do_mqtt_publish(client, (MOLD_UPSIDE_PLAT_FLAG | MOLD_TIMESTAMP_FLAG | MOLD_AMBIENT_TEMP_FLAG), sensor_data1, 26.0)
            # publish downside plat data
            do_mqtt_publish(client, (MOLD_TIMESTAMP_FLAG), sensor_data2, 0)
            time.sleep(1)
        rc = client.loop()
        print("rc:"+str(rc))

    client.disconnect()

# start program
main()


