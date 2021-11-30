import json
from kafka import KafkaConsumer
import numpy as np
import pandas as pd

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

consumer.subscribe('python-topic-1')
for message in consumer:
    message = message.value;
    print('{}'.format(message))
    #df = pd.read_json('{}'.format(message))
    #print(df)

