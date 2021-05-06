# initial packages required for the program
import requests as r
import pandas as pd
import time
import json
import sys
from csv import reader
from datetime import date
import datetime as day
from threading import *
import paho.mqtt.client as mqtt
import paho.mqtt.publish as pb
from cryptography.fernet import Fernet

#import from the client program
from client import subscribeStatus

today = date.today()

#assigning the dynamic parameters
mqtt_host=sys.argv[1]
duration= int(sys.argv[2])

# symmetric key (KIS)
symmetricKey_KIS = b'aQOQxINtlrXU_HkbJywoMxfiFMXC-OToihHK2ApIeCs='
KIS = Fernet(symmetricKey_KIS)

# arranges the starting nad ending dates  for the data collection
endtime = today - day.timedelta(days=1)
endtime = endtime.strftime("%Y%m%d")
starttime = today - day.timedelta(days = (duration+1))
starttime = starttime.strftime("%Y%m%d")

# the data points to extract data. For the demo the data is collected from the urban repository of Newcastle University, UK
url1="http://uoweb3.ncl.ac.uk/api/v1.1/sensors/PER_AIRMON_MESH1911150/data/json/?starttime="+starttime+"&endtime="+endtime+""
url2="http://uoweb3.ncl.ac.uk/api/v1.1/sensors/PER_AIRMON_MESH301245/data/json/?starttime="+starttime+"&endtime="+endtime+""
url3="http://uoweb3.ncl.ac.uk/api/v1.1/sensors/PER_EMOTE_1309/data/json/?starttime="+starttime+"&endtime="+endtime+""

number_of_rows = 0
df = pd.DataFrame()

#data collection function. Accept the url as input
def dataCollection(url):
    start = time.time()
    global df
    global number_of_rows
    response=r.get(url)
    content=[]
    values= response.json()

    for item in values['sensors']:    # used to split the stream data into dictionary valeus for further processing
        variable =list(item['data'].keys())
        variableLength= len(item['data'].keys())
        for x in range(0,variableLength):
            a=variable[x]
            subitem=item['data'][a]
            for item1 in subitem:
                mydict={'Sensor':item1['Sensor Name'],'Type':item1['Variable'],'Units':item1['Units'],
                        'time':item1['Timestamp'],'Value':item1['Value'],
                        'Flag':item1['Flagged as Suspect Reading']}
                content.append(mydict)
    
    # if ther eare any values in the URL then they are appended to the dataframe
    if(len(content)>0):
        df = df.append(content, ignore_index=True)
    end = time.time()
    print(df.shape[0])
    number_of_rows= df.shape[0]
    print(end-start)

# fuction that publish values through MQTT, It accepts values and the topic of publication
def publishResult(value,publish_topic):
    host=mqtt_host 
    port=1883
    pb.single(publish_topic, value, 0, False, host, port)

# this is the threading function that simultaneous collects data from URL
def datThread(url1,url2,url3):
    global df
    thread1=Thread(target=dataCollection,args=(url1,))
    thread2=Thread(target=dataCollection,args=(url2,))
    thread3=Thread(target=dataCollection,args=(url3,))

    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    
    #collected data are then saved to a file.
    df.to_csv("test1.csv",mode='w+',index=False,header= None)

    # for the analysis in SC the combinations are collected and saved
    a = df.groupby(["Sensor", "Type", "Units"])["Sensor"].unique().to_frame(name="1").reset_index().drop("1", 1)
    a.to_csv("combination.csv",mode='w+',index=False,header= None)
    print(a)

datThread(url1,url2,url3)

#fucntion to prepare the data for publish. The data is sent as streams (one row after other) no encryption
def prepareForPublish(fileName,publish_topic):
    with open(fileName,'r') as lines:
        row_reader = reader(lines)
        for row in row_reader:
            line = ','.join(row)
            message=((line).encode())
            publishResult(message,publish_topic)
    publishResult((("done").encode()),publish_topic)

#fucntion to prepare the data for publish. The data is sent as streams (one row after other) and encrypted
def prepareForPublish1(fileName,publish_topic,key):
    symmetricKey_KIE = key
    KIE = Fernet(symmetricKey_KIE)
    with open(fileName,'r') as lines:
        row_reader = reader(lines)
        for row in row_reader:
            line = ','.join(row)
            message=KIE.encrypt((line).encode())
            publishResult(message,publish_topic)
    publishResult(KIE.encrypt(("done").encode()),publish_topic)

i=0  # for data count

# it is a continuous function and executes indefinitely
while(True):
    mess=subscribeStatus()
    if(mess=="usbdata"):
        prepareForPublish("combination.csv","usbdata1")
        print("SC asked for data")
    elif(mess=="abort"):
        df = pd.DataFrame()
        print("SC says abort the data and collect new data")
        datThread(url1,url2,url3)
    else:
        start3 = time.time()
        print("Received the Key")
        
        symmetricKey_KIS = b'aQOQxINtlrXU_HkbJywoMxfiFMXC-OToihHK2ApIeCs='
        KIS = Fernet(symmetricKey_KIS)
        encrypted=mess.encode()
        mess=KIS.decrypt(encrypted)
        
        # as per the count it sends data records from 1k to 40k
        if i==0:
            df[0:1000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(1000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=1000
            i=i+1
        elif i==1:
            df[0:2000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(2000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=2000
            i=i+1
        elif i==2:
            df[0:5000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(5000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=5000
            i=i+1
        elif i==3:
            df[0:10000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(10000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=10000
            i=i+1
        elif i==4:
            df[0:20000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(20000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=20000
            i=i+1
        elif i==5:
            df[0:40000].to_csv("test2.csv",mode='w+',index=False,header= None)
            publishResult(str(40000),"decrypt_time")
            prepareForPublish1("test2.csv","usbdata_EDC",mess)
            print("send to EDC")
            number_of_rows=40000
            i=0
        
        # value=False
        end3 = time.time()
        print(end3-start3)
        
        publishResult(str(end3-start3),"encrypt_time")
        #bench = open("/benchmarking/encrypt_benchmark.csv","a+")
        #bench.write(str(number_of_rows)+" , "+str(end3-start3)+"\n")
        #bench.close()
        df = pd.DataFrame()
        datThread(url1,url2,url3)