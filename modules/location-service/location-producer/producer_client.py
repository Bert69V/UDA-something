import grpc
import LocationEvent_pb2
import LocationEvent_pb2_grpc

# gRPC client setup
channel = grpc.insecure_channel('localhost:50051')
stub = location_pb2_grpc.LocationServiceStub(channel)

def generate_random_location():
    user_id = random.randint(1, 100)
    latitude = random.randint(-90, 90)
    longitude = random.randint(-180, 180)
    return location_pb2.LocationMessage(userId=user_id, latitude=latitude, longitude=longitude)

def send_to_kafka(message):
    producer.send('location-topic', message)

def run():
    while True:
        # Create a random location and send it to Kafka
        location = generate_random_location()
        print(f"Sending location: {location}")
        send_to_kafka(location)
        time.sleep(1)  # Sleep for 1 second before sending the next location

if __name__ == "__main__":
    run()
