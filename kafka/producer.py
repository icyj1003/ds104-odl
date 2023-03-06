from kafka import KafkaProducer
import json
import random
from faker import Faker
import time
import uuid

faker = Faker()


def get_post():
    return {
        'content': faker.text(),
        'from_user': faker.name(),
        'label': random.randint(0, 2)
    }


def serializer(message):
    return json.dumps(message).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer,
    key_serializer=serializer,

)

count = 0
while True:
    producer.send('messages', key=str(uuid.uuid4()), value=get_post())
    count += 1
    time.sleep(2)
