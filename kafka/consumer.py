import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)
for message in consumer:
    key = message.key.decode('utf8').replace("'", '"')
    value = message.value.decode('utf8').replace("'", '"')
    print(key, value)
