import time
import json
import random
import ssl
import paho.mqtt.client as mqtt

BROKER = "9df424bbfbee438987271df66864e402.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "***************"
PASSWORD = "**************"

DEVICE_ID = "temperature_sensor_01"

DATA_TOPIC = f"devices/{DEVICE_ID}/data"
CMD_TOPIC  = f"devices/{DEVICE_ID}/command"

running = True

def on_connect(client, userdata, flags, rc):
    print("Connected with code", rc)
    client.subscribe(CMD_TOPIC)

def on_message(client, userdata, msg):
    global running
    command = msg.payload.decode()


    if command == "STOP":
        running = False
        print("🛑 Sensor stopped")

    elif command == "START":
        running = True
        print("▶ Sensor started")

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()

while True:
    if running:
        temperature = round(random.uniform(20, 35), 2)
        payload = {
            "device_id": DEVICE_ID,
            "temperature": temperature,
            "unit": "C"
        }
        client.publish(DATA_TOPIC, json.dumps(payload))
        print("📤", payload)

    time.sleep(5)
