from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# 1) Configure the producer to connect to your local Redpanda broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 2) Define some example contacts and event types
contact_ids = list(range(1, 101))  # assuming you have contacts 1–100 seeded
event_types = ['email', 'phone_call', 'meeting']

# 3) Continuously emit random log_interaction events
try:
    while True:
        event = {
            'contact_id': random.choice(contact_ids),
            'type':       random.choice(event_types),
            'timestamp':  datetime.utcnow().isoformat(),
            'notes':      'Automated test interaction'
        }
        # send to the 'interactions' topic
        producer.send('interactions', event)
        print(f"Sent: {event}")
        time.sleep(random.uniform(0.5, 2.0))  # 0.5–2 second pause
except KeyboardInterrupt:
    print("Stopping producer.")
finally:
    producer.flush()
    producer.close()
