from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda value: json.dumps(value).encode('utf-8')
)

producer.send('test_topic', {'id': 1, 'name': 'Alice'})

#### 컨슈머 코드
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda value: json.loads(value.decode('utf-8'))
)

for message in consumer:
    print(message.value)