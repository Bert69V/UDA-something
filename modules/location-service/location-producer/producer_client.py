import grpc
import location_pb2
import location_pb2_grpc
import random
import time
from kafka import KafkaProducer

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=['kafka-headless:9092'],
    value_serializer=lambda v: v.SerializeToString()
)

def generate_random_location():
    """Generate a random location."""
    user_id = random.randint(1, 100)
    latitude = random.uniform(-90, 90)  # Use float for latitude/longitude
    longitude = random.uniform(-180, 180)
    return location_pb2.LocationMessage(userId=user_id, latitude=latitude, longitude=longitude)

def send_to_kafka(message):
    """Send message to Kafka."""
    producer.send('location-topic', message)
    producer.flush()

def run():
    """Main function to send random locations via gRPC and Kafka."""
    while True:
        # Generate a random location
        location = generate_random_location()
        print(f"Generated location: {location}")

        # Use gRPC channel with context manager
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = location_pb2_grpc.LocationServiceStub(channel)
            try:
                # Send the location using gRPC
                response = stub.Create(location)
                print(f"gRPC Response: {response}")

                # Send the same location to Kafka
                send_to_kafka(location)
            except grpc.RpcError as e:
                print(f"gRPC Error: {e.details()}")

        time.sleep(1)  # Sleep for 1 second before sending the next location

if __name__ == "__main__":
    run()
