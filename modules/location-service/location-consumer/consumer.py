from kafka import KafkaConsumer
import location_pb2
import psycopg2
import json
import os


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# Kafka consumer setup
consumer = KafkaConsumer(
    'location-topic',
    bootstrap_servers='kafka-headless:9092',
    group_id='location-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    port=DB_PORT
)
cur = conn.cursor()

def insert_location_to_db(location):
    query = """
        INSERT INTO location (person_id, coordinate, creation_time)
        VALUES (%s, ST_SetSRID(ST_Point(%s, %s), 4326), NOW())
    """
    cur.execute(query, (location['userId'], location['longitude'], location['latitude']))
    conn.commit()

def run():
    for message in consumer:
        location = message.value
        print(f"Received location: {location}")
        insert_location_to_db(location)

if __name__ == "__main__":
    run()
