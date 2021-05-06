# this program start the request  for data fro SC
# it start as a sub process of main program decider_proper.py
import paho.mqtt.publish as pb
import time as tm
import datetime as dtm
from subprocess import call
# import threading
import sys
import logging
import asymcrypt

#accept the dynamic values 
HOST = sys.argv[1]
waiting = int(sys.argv[2]) # durtaion between each request
#print(type(Host))
#print(type(waiting))
# CONTAINER_MQTT_HOST = sys.argv[2]
PORT = 1883
logging.basicConfig(level=logging.DEBUG)

def startProcess():
    i = 0
    while True:
        i = i + 1
        publishData(i)

def publishData(i):
    TOPIC = "request/data"
    regPayload = encrypt("dc1" + "," + str(dtm.datetime.now())) # encrypt the request
    pb.single(TOPIC, regPayload, 0, False, HOST, PORT)
    # pb.single("bench_subscribe", str(dtm.datetime.now()), 0, False, CONTAINER_MQTT_HOST, PORT)
    a = open('data/bench_time.txt','w+')
    a.write(str(dtm.datetime.now())) # write the starting time of the cycle
    a.close()
    print("\n")
    logging.info("Batch: %s - Request initiated at %s", i,str(dtm.datetime.now()))
    # sleep_Time = int(sys.argv[3])
    #sleep_Time = waiting
    tm.sleep(waiting)

def encrypt(data):
    cipherTxt = asymcrypt.encrypt_data(data, "deciderPub.pem")
    hexStr = cipherTxt.hex()
    return hexStr

#call(["python", "Subscribe.py", HOST])
startProcess()
