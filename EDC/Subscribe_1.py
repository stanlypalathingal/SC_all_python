# load initial packages
import paho.mqtt.subscribe as sub
import pandas as pd
import asymcrypt
import paho.mqtt.publish as pb
import datetime as dtm
import sys
import socket
import operator
from cryptography.fernet import Fernet
import time

HOST = sys.argv[1]
mqtt_host = sys.argv[1]
PORT = 1883

#socket programing
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9012))
s.listen()

KIE = b'dummy154value' # dummy value of KIE for first instance
number_of_records=0
encrypt_time=0

def on_message_print(client, userdata, message):
    if message.topic == "dc1": # for colecting  the KIE from SC
        global KIE
        encrypted_data = message.payload.decode()
        new_rnd_bytes = bytes.fromhex(encrypted_data)
        key = asymcrypt.decrypt_data(new_rnd_bytes, "priv.pem")  # Asymm decryption
        print("Received the Key")
        KIE=Fernet(key)
    
    elif message.topic== "sc_time": # for accepting SC time duration
        sc_time=message.payload.decode("utf-8")
        sc_bench = open("/benchmarking/sc_benchmark.csv","a+")
        sc_bench.write(str(sc_time)+"\n")
        sc_bench.close()
        
    elif message.topic== "encrypt_time": # for accepting IoT encryption time duration
        global encrypt_time
        #print(message.payload.decode("utf-8"))
        encrypt_time=message.payload.decode("utf-8")
        
    elif message.topic== "decrypt_time": # for accepting EDC decryption time duration
        global number_of_records
        #print(message.payload.decode("utf-8"))
        number_of_records=message.payload.decode("utf-8")
        f=open('data/time.txt',"w+")
        f.write(str(dtm.datetime.now()))
        f.close()

    elif message.topic == "usbdata_EDC":
        mess=(KIE.decrypt(message.payload)).decode("utf-8")
        #print(mess)
        with open('data/test.csv','a+') as f:
            # for calculating encryption and decryption time time duration
            if(operator.contains(mess,"done")): 
                clientsocket,address = s.accept()
                clientsocket.send(bytes("done","utf-8"))
                #print("All data written to file")
                mess=""
                a = open('data/time.txt').read().replace('\n', '')
                a = pd.to_datetime(a, infer_datetime_format=True)
                c = (dtm.datetime.now() - a)
                print("Time taken for decrypt  ", c.total_seconds())
                decrypt_bench = open("/benchmarking/decrypt_benchmark.csv","a+")
                decrypt_bench.write(str(number_of_records)+" , "+str(c.total_seconds())+"\n")
                decrypt_bench.close()
                
                encrypt_bench = open("/benchmarking/encrypt_benchmark.csv","a+")
                encrypt_bench.write(str(number_of_records)+" , "+str(encrypt_time)+"\n")
                encrypt_bench.close()
            f.write("\n"+str(mess))
        f.close()
            
sub.callback(on_message_print, ["dc1", "usbdata_EDC","decrypt_time","encrypt_time","sc_time"], hostname=HOST, port=PORT)
