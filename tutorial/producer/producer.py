from kafka import KafkaProducer, KafkaConsumer, KafkaClient
import json
import random
from time import sleep
from datetime import datetime
import pandas as pd
import numpy as np
import time


df = pd.read_json('forest_fire.json')
print(df)
js = df.to_json()
obj = json.loads(js)

id = obj['id']

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
while True:
    producer.send('python-topic-1', js)
    time.sleep(10)
    print("BEEP BEEP")
# sudo docker-compose up -d
# sudo docker-compose ps
# -- create topic --
# sudo docker-compose exec kafka \
# kafka-topics --create --topic kafka-python-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
"""virtualenv -p python3 .env3
source .env3/bin/activate"""