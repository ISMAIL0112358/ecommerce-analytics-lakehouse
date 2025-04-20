import random
import uuid
import json
from datetime import datetime
import time
from kafka import KafkaProducer
import pandas as pd
import os

# --- Configs ---
KAFKA_ENABLED = True
PARQUET_ENABLED = False
KAFKA_TOPIC = "ecommerce-events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
PARQUET_DIR = "data/parquet_output"

EVENT_TYPES = ["view", "add_to_cart", "purchase", "remove_from_cart"]
PRODUCTS = ["laptop", "smartphone", "headphones", "tablet", "camera"]

# --- Setup Kafka Producer ---
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
) if KAFKA_ENABLED else None

def generate_event():
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 100)}",
        "event_type": random.choice(EVENT_TYPES),
        "product_id": random.choice(PRODUCTS),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def write_parquet(events):
    os.makedirs(PARQUET_DIR, exist_ok=True)
    df = pd.DataFrame(events)
    filename = f"{PARQUET_DIR}/events_{int(time.time())}.parquet"
    df.to_parquet(filename, index=False)
    print(f"[PARQUET] Wrote {len(events)} events to {filename}")

def main(batch_size=10, interval=5):
    while True:
        events = [generate_event() for _ in range(batch_size)]

        # Print preview
        for e in events:
            print(json.dumps(e))

        if KAFKA_ENABLED:
            for event in events:
                producer.send(KAFKA_TOPIC, event)
            print(f"[KAFKA] Sent {len(events)} events to topic '{KAFKA_TOPIC}'")

        if PARQUET_ENABLED:
            write_parquet(events)

        time.sleep(interval)

if __name__ == "__main__":
    main()
