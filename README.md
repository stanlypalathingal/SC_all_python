The findings of this work are published in "Decision tree based user-centric security solution for critical IoT infrastructure" and it is avilable at https://doi.org/10.1016/j.compeleceng.2022.107754
HTe work simulates a reallife scenario and uses Machine learning methods to identify threats.

Use the following step for replication.
# 1. For ordinary demo 
In order to reproduce the system, the required system and software requirements are
* Three SSH Raspberry Pi with Docker installed and SSH enabled
* A static IP (Broker) for MQTT. 

The three components must run parallelly to reproduce the model. Docker images for the components are uploaded in the **www.dockerhub.com** and one must pull it to the system to execute it

The first execution might take some time since EDC takes time for Machine Learning modeling.

The docker images are in public repositories and can be accessed by anyone.

### a) SC
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc ip_address
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc 3.192.180.215
```

### b) IoTD

docker run -it stanlysac/sc_all_python:iotd ip_address duration
```bash
docker run -it stanlysac/sc_all_python:iotd 3.192.180.215   2
```
here 2 is the **number of days** for which you can collect the data. For demo purpose use it as 1 or 2.

### c) EDC

docker run -it stanlysac/sc_all_python:edc ip_address duration
```bash
docker run -it stanlysac/sc_all_python:edc 3.192.180.215 120
```
Here 120 is the **time** between each request and it is in **seconds**. With 120 as teh duration every two minutes data will reach to EDC.

# 2. For Benchmarking purpose
All the required benchmarking details from the three components can be access as *csv* files from system where EDC gets executed. 
### a) SC
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc ip_address
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc 3.192.180.215
```

### b) IoTD

docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:iotd_benchmarking ip_address duration
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:iotd_benchmarking 3.192.180.215   8
```
here 8 is the **number of days** for which you can collect the data. This will generate more than 50K records.
For the benchmarking the system uses records of 1K,2K,5K,10K,20K and 40K.

### c) EDC

docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:edc ip_address duration
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:edc 3.192.180.215   420
```
Here 420 is the **time** between each request and it is in **seconds**. With 420 as the duration every 7 minutes data will reach to EDC.
