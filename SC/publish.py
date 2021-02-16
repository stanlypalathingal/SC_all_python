import paho.mqtt.client as mqtt
import sys
mqtt_host=sys.argv[1]
#print("in publish", mqtt_host)

def publish(topic,value):
    def on_connect(client, userdata, flags, rc):
        if rc != mqtt.CONNACK_ACCEPTED:
            raise IOError("Couldn't establish a connection with the MQTT server")
    def publish_value(client, topic, value):
        client.publish(topic=topic, payload=value, qos=0)
        print("publishing",topic)

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.connect(host=mqtt_host, port=1883)
    client.loop_start()
    topic=topic
    value=value
    publish_value(client,topic, value)
    client.disconnect()
    client.loop_stop()
