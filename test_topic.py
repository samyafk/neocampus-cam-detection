import paho.mqtt.client as mqtt
import time

# Configuration MQTT
broker = "autocampus.fr"
port = 1883
topic = "TestTopic/testStage/"
username = "test"
password = "test"

# Fonction callback quand la connexion au broker est établie
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker")
    else:
        print("Échec de connexion, code retour : ", rc)

# Fonction callback pour la publication d'un message
def on_publish(client, userdata, mid):
    print("Message publié avec ID : ", mid)

# Création d'une instance du client MQTT
client = mqtt.Client()

# Configuration des identifiants de connexion
client.username_pw_set(username, password)

# Assignation des fonctions callback
client.on_connect = on_connect
client.on_publish = on_publish

# Connexion au broker MQTT
client.connect(broker, port, 60)

# Boucle principale pour maintenir la connexion et envoyer des messages
client.loop_start()

try:
    count = 0
    while True:
        message = f"Message {count}"
        result = client.publish(topic, message)
        
        # Vérifier si la publication a réussi
        status = result[0]
        if status == 0:
            print(f"Message {count} envoyé sur le topic {topic}")
        else:
            print(f"Échec de l'envoi du message {count}")

        count += 1
        time.sleep(1)  # Pause d'une seconde entre chaque message

except KeyboardInterrupt:
    print("Interruption par l'utilisateur")

finally:
    client.loop_stop()
    client.disconnect()

