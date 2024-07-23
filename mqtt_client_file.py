import paho.mqtt.client as mqtt
import time
import random

broker = 'localhost'
port = 1883
topic = "status_zero_to_six"

client = mqtt.Client()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        status = random.randint(0, 6)
        result = client.publish(topic, status)
        status_code = result[0]
        if status_code == 0:
            print(f"Send `{status}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(1)

if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    publish(client)
