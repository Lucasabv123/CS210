# etl_consumer.py
import json
from kafka import KafkaConsumer
from models import Interaction, Session
from datetime import datetime


def main():
    # Configure Kafka consumer
    consumer = KafkaConsumer(
        'interactions',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m)
    )
    session = Session()
    print("✅ ETL Consumer started. Listening for 'interactions' events...")

    for msg in consumer:
        data = msg.value
        # Parse and insert into Postgres
        interaction = Interaction(
            contact_id=data['contact_id'],
            type=data['type'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            notes=data.get('notes')
        )
        session.add(interaction)
        session.commit()
        print(f"Inserted Interaction: {interaction.interaction_id} for Contact {interaction.contact_id}")


if __name__ == '__main__':
    main()
