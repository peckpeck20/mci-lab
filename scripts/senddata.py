from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sense = SenseHat()

Broker = "test.mosquitto.org"
sub_topic = "techlab/sensehat/#"    # receive messages on this topic

url = 'https://fthl-jenbach.cloud.arge3d.at/Thingworx/'
headers = { 'Content-Type': 'application/json', 'appKey': '0f2c6eae-9698-42eb-a4f7-cf2c5cfa036b' }
thing = 'RaspberryPiThing'

############### sensehat inputs ##################

def read_temp():
    t = sense.get_temperature()
    t = round(t)
    return t

def read_humidity():
    h = sense.get_humidity()
    h = round(h)
    return h

def read_pressure():
    p = sense.get_pressure()
    p = round(p)
    return p

def display_sensehat(message):
    sense.show_message(message)
    time.sleep(10)

############### MQTT section ##################

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)
    display_sensehat(message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    sensor_data = [read_temp(), read_humidity(), read_pressure()]
    client.publish("techlab/temp/group4", str(read_temp()))
    client.publish("techlab/hum/group4", str(read_humidity()))
    client.publish("techlab/pres/group4", str(read_pressure()))

    payload = { 'Prop_Humidity' : str(read_humidity()), 'Prop_Temperature' : str(read_temp())}
    response = requests.put(url + '/Things/' + thing + '/Properties/*', headers=headers, json=payload, verify=False)   

    time.sleep(1*60)