import ssl
import json
import paho.mqtt.client as mqtt

BROKER = "9df424bbfbee438987271df66864e402.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "*************"
PASSWORD = "*************"

TOPIC = "devices/temperature_sensor_01/data"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    print(f"🌡 Temperature: {data['temperature']} {data['unit']}")

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()