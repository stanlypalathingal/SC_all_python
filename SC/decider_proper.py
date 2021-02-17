import time
time.sleep(1) # to make sure it will not start before subscribe.py

# Load the publish and subscribe files
from sym_key_generator import sym_key # sym_key_generator.py
from client import subscribeStatus # client.py
from publish import publish # publish.py
from sym_key_generator import encrypt_public #sym_key_generator.py

# Load the packages
import datetime
import pandas as pd
# load the training dataset
df = pd.read_csv("data/training_data.csv")

# the original combination of sensor, type and units
a = df.groupby(["Sensor", "Type", "Units"])["Sensor"].unique().to_frame(name="1").reset_index().drop("1",1)

# Function 1
'''
accepts two parameters.
    First is the dataframe of combinations of original dataset
    second is the test dataset
It then uses the group by to create the combinations
Both are merged using the inner. So it will have the common ones in original and test
Combine the new (c) with that of test (b).
use duplicates only to keep the differnces
'''
def spoof_detect(a, b):
    c = (b.merge(a, how="inner"))
    fake = pd.concat([c, b], sort=False)
    # print(fake)
    # print(fake.drop_duplicates(keep=False))
    return fake.drop_duplicates(keep=False)

# Function 2
'''
function to find the time duration. 
# This duration is from the time the request reach in SC till the publish of Symmetric keys
The parameter name_of_dc provides the id of the EDC requested for data
'''
def benchmark():
    name_of_dc=open('data/temporary_store.txt').read().replace('\n','')
    #print("name of DC is",name_of_dc)
    df1 = pd.read_csv("data/register_dc.csv", delimiter=",",names=["topic", "time"])
    df1["time"] = pd.to_datetime(df1["time"], infer_datetime_format=True) # convert the object to datetime format
    #print(df1)
    #print("name of DC in bench",name_of_dc)
    #print(type(name_of_dc))
    a = (df1.loc[df1.topic == name_of_dc, "time"].iloc[0])
    #print("a  ",a)
    c = (datetime.datetime.now()-a)
    print("Time taken benchmark ",c.total_seconds())
    publish("sc_time",str(c.total_seconds()))
    print("*************************************************")
    f = open("data/temporary_store.txt","w")
    f.truncate()
    f.close()

# function for log files for later analysis
def abort_reason(file,reason):
	text_file = open("/logs/"+file+".log", "a+") 
	text_file.write("\n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+","+ reason) # write the time and reason
	text_file.close()

# function for clearing files of the real-time data
def clearFiles():
	f = open("data/test.csv", "w")
	f.truncate()
	f.close()

# function to create the log files for tracking the abort processes 
def abort_process(original_combination,temp_data,start):
	publish("sensor_sym_key","abort")
	encrypt_public("nodata")
	benchmark()
	abort_reason("error"," \n")
	spoof_detect(original_combination,temp_data).to_csv("/logs/error.log",mode="a",index=False) # save the error details with time
	end=time.time()
	print("Time taken for the analysis after receving the data ",end-start)
	clearFiles()

'''
The while loop below is infinite.
First it will call the function subscribeStatus() which will inform the completion of data collection.
Once the status is true, then the function perfrom the analysis
'''
while(True):
	mess=subscribeStatus()
	if(mess=="done"):
		start=time.time()
		
		# collect the id of the EDC
		#name_of_dc=open('data/temporary_store.txt').read().replace('\n','')
		#print("name of DC is",name_of_dc)
		#load the data for testing and remove the dulicates
		temp_data=pd.read_csv("data/test.csv",delimiter=",",names=["Sensor","Type","Units"])
		b=temp_data.groupby(["Sensor","Type","Units"])["Sensor"].unique().to_frame(name="1").reset_index().drop("1",1)
		if(temp_data.shape[0]>0):
			temp_data=temp_data.drop_duplicates()
			print("Number of rows for testing",temp_data.shape[0])
			# Checking  the existance of dummy or spoof data. Each level it call the function and process that data
			if(len(spoof_detect(a[["Sensor"]],b[["Sensor"]]))==0):
				print("The sensors are all authentic")
				if(len(spoof_detect(a[["Sensor","Type"]],b[["Sensor","Type"]]))==0):
					print("		The types are all authentic")
					if(len(spoof_detect(a[["Sensor","Type","Units"]],b[["Sensor","Type","Units"]]))==0):
						print("			The units are all authentic")
						sym_key() # generate the symmetric key
						benchmark() # benchmark process
						clearFiles()
					else:
						print("there are fake units")
						publish("sensor_sym_key","abort") # publish abort data message to IoTD
						abort_process(a,b,start)
						clearFiles()
				else:
					print("there are fake categories")
					publish("sensor_sym_key","abort") # publish abort data message to IoTD
					abort_process(a,b,start)
					clearFiles()
			else:
				print("there are fake sensors")
				publish("sensor_sym_key","abort") # publish abort data message to IoTD
				abort_process(a,b,start)
				clearFiles()

		else:
			publish("sensor_sym_key","abort") # publish abort data message to IoTD
			print("nodata")
			benchmark()
			abort_reason("no_data","no data available in the sensors")
			clearFiles()
		#f = open("data/temporary_store.txt","w")
		#f.truncate()
		#f.close()
		mess=None # keep the status as none for the new data

