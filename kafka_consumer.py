from confluent_kafka import Consumer, KafkaException, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka server
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest'  # Change to 'latest' if you want to start from the latest message
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to a topic
consumer.subscribe(['ecommerce-events'])  # Replace with your Kafka topic

def consume_messages():
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Timeout in seconds
            if msg is None:
                # No message available within timeout
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    print(f"End of partition: {msg.partition}, offset: {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                print(f"Received message: {msg.value().decode('utf-8')}")
               

    except KeyboardInterrupt:
        print("Consuming interrupted.")
    finally:
        # Close the consumer to commit offsets and clean up
        consumer.close()

# Start consuming messages
consume_messages()
