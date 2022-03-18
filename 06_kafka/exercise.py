from kafka import KafkaProducer, KafkaConsumer

# producer
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

for _ in range(10):
    producer.send('foobar', b'some_message_bytes')

consumer = KafkaConsumer('test_topic', bootstrap_servers='localhost:9092')

for message in consumer:
    print(message.topic, message.partition, message.offset, message.key, message.value)