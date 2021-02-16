# Subscribing the data  from broker. Running forever
import paho.mqtt.client as mqtt
import time
import sys
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),9006))
s.listen()
#mqtt_host = "mqtt.eclipse.org"
#mqtt_host = "3.81.10.247"
mqtt_host=sys.argv[1]

def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:       
        client.subscribe("usbdata1")
def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    print("I've subscribed sensor Data")

def print_received_message_mqtt(msg):
    print("Message received. Payload: {}".format(str(msg.payload)))

def on_message_mqtt(client, userdata, msg):
    #print_received_message_mqtt(msg)
    mess=msg.payload.decode("utf-8")
    with open('data/test.csv','a+') as f:
       if(mess=="done"):
           clientsocket,address = s.accept()
           clientsocket.send(bytes("done","utf-8"))
           #print("All data written to file")
           mess=""
           mosquitto_client.connect(host=mqtt_host, port=1883)
       f.write("\n"+str(mess))
    f.close()
    
if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message=on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()

