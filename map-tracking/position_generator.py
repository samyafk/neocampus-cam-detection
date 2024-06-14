import json
from datetime import datetime
import time
import paho.mqtt.client as mqtt



###############################################################
########################## JSON FILE ##########################
###############################################################
input_file = open('intinerary.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']
data = {}
data['type'] = "navette"



############################################################
######################## MQTT SETUP ########################
############################################################
broker = "autocampus.fr"
port = 1883
topic = "TestTopic/testStage/"
username = "test"
password = "test"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker")
    else:
        print("Échec de connexion, code retour : ", rc)

def on_publish(client, userdata, mid):
    print("Message publié avec ID : ", mid)

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker, port, 60)

client.loop_start()

try:
    i = 0
    while i < len(coordinates):
        data['id'] = i
        data['timestamp'] = str(datetime.now())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]

        message = json.dumps(data)
        result = client.publish(topic, message)
        
        status = result[0]
        if status != 0:
            print("Échec de l'envoi du message!")
            
        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1
            
        time.sleep(1)

except KeyboardInterrupt:
    print("Interruption par l'utilisateur")

finally:
    client.loop_stop()
    client.disconnect()

