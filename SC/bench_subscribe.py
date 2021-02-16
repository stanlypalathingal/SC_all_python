# Subscribing the data  from broker. Running forever
import paho.mqtt.client as mqtt
import sys

mqtt_host = sys.argv[1]


def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:
        # client.subscribe("machine_learning")
        client.subscribe("bench_subscribe")


def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    print("I am subscribing benchmark data")


def print_received_message_mqtt(msg):
    print("Message received. Payload: {}".format(str(msg.payload)))


def on_message_mqtt(client, userdata, msg):
    # print_received_message_mqtt(msg)
    mess = msg.payload.decode("utf-8")
    with open('data/bench_time.txt', 'w+') as f:
        f.write("\n" + str(mess))
    f.close()


if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message = on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()
