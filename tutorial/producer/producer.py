from kafka import KafkaProducer
import json
import random
from time import sleep
from datetime import datetime
from kafka import KafkaConsumer

# Create an instance of the Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Call the producer.send method with a producer-record
print("Ctrl+c to Stop")
while True:
    producer.send('python-topic-1', random.randint(1,999))

# sudo docker-compose up -d
# sudo docker-compose ps
# -- create topic --
# sudo docker-compose exec kafka \
# kafka-topics --create --topic kafka-python-topic --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092