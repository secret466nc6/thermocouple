import paho.mqtt.client as mqtt
import msgpack
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("paho/temperature")
    client.subscribe("paho/temperature/t1")
    client.subscribe("MOS/MOLD/TEMPERATURE/1234567890")
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.username_pw_set("admin","kK123")
client.connect("140.113.213.86",61613)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()


#client.publish("paho/temperature","my message")

rc = 0
while rc == 0:
 rc = client.loop()
 print("rc:"+str(rc))

