import json
from datetime import datetime
import time
import paho.mqtt.client as mqtt



################################################################
########################## JSON FILES ##########################
################################################################
input_file = open('intinerary.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']
data = {}
data['vehicule_1'] = {}
data['vehicule_1']['class'] = "navette"

input_file_person = open('intinerary_person.json')
json_array_person = json.load(input_file_person)
coordinates_person = json_array_person['features'][0]['geometry']['coordinates']
data['vehicule_2'] = {}
data['vehicule_2']['class'] = "person"



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
    min = min(len(coordinates), len(coordinates_person))
    while i < min:
        # data['id'] = i
        # data['timestamp'] = str(datetime.now())
        data['vehicule_1']['latitude'] = coordinates[i][1]
        data['vehicule_1']['longitude'] = coordinates[i][0]
        data['vehicule_2']['latitude'] = coordinates_person[i][1]
        data['vehicule_2']['longitude'] = coordinates_person[i][0]

        message = json.dumps(data)
        result = client.publish(topic, message)
        
        status = result[0]
        if status != 0:
            print("Échec de l'envoi du message!")
            
        if i == min - 1:
            i = 0
        else:
            i += 1
            
        time.sleep(1)

except KeyboardInterrupt:
    print("Interruption par l'utilisateur")

finally:
    client.loop_stop()
    client.disconnect()

