from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

sense = SenseHat()

Broker = "test.mosquitto.org"
sub_topic = "techlab/sensehat/test"    # receive messages on this topic

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
    client.publish("techlab/sensehat/bigboipi4-temp", str(read_temp()))
    client.publish("techlab/sensehat/bigboipi4-hum", str(read_humidity()))
    client.publish("techlab/sensehat/bigboipi4-pres", str(read_pressure()))  

    time.sleep(1*60)