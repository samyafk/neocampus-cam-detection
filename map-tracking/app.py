import threading
from flask import Flask, render_template, Response
import paho.mqtt.client as mqtt



app = Flask(__name__)

############################################################
######################## MQTT SETUP ########################
############################################################
broker = "autocampus.fr"
port = 1883
topic = "TestTopic/testStage/"
username = "test"
password = "test"
messages = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker")
        client.subscribe(topic)
    else:
        print("Échec de connexion, code retour : ", rc)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    messages.append(message)

client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
def mqtt_thread():
    client.connect(broker, port)
    client.loop_forever()
mqtt_thread = threading.Thread(target=mqtt_thread)
mqtt_thread.start()



@app.route('/')
def index():
    return (render_template('index.html'))

@app.route('/messages', methods=['GET'])
def get_messages():
    def events():
        current_length = len(messages)
        while True:
            if len(messages) > current_length:
                for i in range(current_length, len(messages)):
                    yield f'data:{messages[i]}\n\n'
                current_length = len(messages)
    return Response(events(), mimetype='text/event-stream')
            

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)