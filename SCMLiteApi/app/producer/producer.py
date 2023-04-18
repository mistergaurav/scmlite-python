
import socket    
import json 
import os
import sys
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
bootstrap_servers = os.getenv("bootstrap_servers")
topic_name = os.getenv("topic_name")
# Initialize KafkaProducer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    retries=5,
    value_serializer=lambda m: m.encode('utf-8')
)
try:
    # Connect to socket
    with socket.socket() as sock:
        sock.connect((host, port))
        while True:
            # Receive data from socket
            data = sock.recv(70240)
            # Send data to Kafka topic
            producer.send(topic_name, data.decode('utf-8'))
except KeyboardInterrupt:
    # Exit gracefully on keyboard interrupt
    sys.exit()
finally:
    # Close KafkaProducer on completion
    producer.close()