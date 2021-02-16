# Subscribing the request from DC through broker. Running forever

import paho.mqtt.client as mqtt
import pandas as pd
import sys
import time
import datetime
from publish import publish
from sym_key_generator import Decryption
pd.options.mode.chained_assignment = None
# mqtt_host = "3.81.10.247"
mqtt_host=sys.argv[1]

def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to a topic 
        client.subscribe("request/data")
def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    print("I've subscribed for request")

def verify_request():
    print("Received a new request")
    df1=pd.read_csv("data/register_dc.csv",delimiter=",",names=["topic","time"]) # file having details of registered DC
    df1["time"]=pd.to_datetime(df1["time"],infer_datetime_format=True) # converting to datatime format
    df2=pd.read_csv("data/data_request.csv",delimiter=",",names=["topic","time"]) # file with new request
    df2["time"]=pd.to_datetime(df2["time"],infer_datetime_format=True) # converting to datatime format
    l=len(df1) # when there are  more than one registered DC
    for i in range(0,l):
        if(df1.topic[i]==df2.topic[0]):
            if(df1.time[i] < df2.time[0]):
                df1.time[i]=datetime.datetime.now() # updating the time to the request time
                print(df1.time[i]) # print the request time
                publish("sensor_data_req","usbdata") # requesting data from IoTD
                df1.to_csv("data/register_dc.csv",index=False,header=False)
                #print("DC name im request ",df2.topic[0])
                with open('data/temporary_store.txt','a+') as f:
                    f.write(str(df2.topic[0]))              # storing the EDC name to be used in other decider_proper.py
                    #print("file written")
                f.close()
                df2=df2.drop(df2.index[[0]]) #removing the request details
                df2.to_csv("data/data_request.csv",mode="w",index=False,header=False) #update the file
            else:
                print("old request") # Discard the old request
        else:
            pass
    
def on_message_mqtt(client, userdata, msg):
    mess=msg.payload
    Decryption(mess) # Decrypt the message
    verify_request() # verify the message

if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message=on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()

