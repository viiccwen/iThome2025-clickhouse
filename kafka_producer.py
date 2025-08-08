import json
import time
from kafka import KafkaProducer
from datetime import datetime
import random

# Kafka Config
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'user_events_topic'

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Generate Random Events
def generate_event():
    return {
        "EventDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "UserID": random.randint(0, 10),
        "Action": random.choice(["click", "view", "purchase"]),
        "Version": 1
    }

# Produce Events Continuously
def produce():
    print("Starting Kafka Producer...")
    try:
        while True:
            event = generate_event()
            producer.send(TOPIC, value=event)
            producer.flush()
            print(f"Produced: {event}")
            time.sleep(0.01)  # Send 1 message per second (adjust as needed)
    except KeyboardInterrupt:
        print("Stopped Producer.")
    finally:
        producer.close()

if __name__ == "__main__":
    produce()