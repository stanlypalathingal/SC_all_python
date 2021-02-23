## SC
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc ip_address
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:sc 3.192.180.215
```

## IoTD

docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:iotd ip_address duration
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:iotd 3.192.180.215   2
```
here 2 is the **number of days** for which you can collect the data

## EDC

docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:edc ip_address duration
```bash
docker run -it -v /home/pi/Documents:/benchmarking stanlysac/sc_all_python:edc 3.192.180.215   400
```
Here 400 is the **time** between each request and it is in **seconds**
