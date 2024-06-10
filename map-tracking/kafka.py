from pykafka import KafkaClient
import json
from datetime import datetime
from time import sleep

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geodata']
producer = topic.get_sync_producer()

# count = 1
# while count < 100:
#     producer.produce(('test message' + str(count)).encode('ascii'))
#     count += 1

input_file = open('intinerary.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

i = 0
data = {}
data['type'] = "navette"

while i < len(coordinates):
    data['id'] = i
    data['timestamp'] = str(datetime.now())
    data['latitude'] = coordinates[i][0]
    data['longitude'] = coordinates[i][1]
    
    message = json.dumps(data)
    producer.produce(message.encode('ascii'))
    sleep(1)
    
    
    if i == len(coordinates) - 1:
        i = 0
    else:
        i += 1
