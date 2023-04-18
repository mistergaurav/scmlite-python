import socket   
import os 
import time    
import pymongo   
import json 
import sys
from kafka import KafkaConsumer
from dotenv import load_dotenv
load_dotenv()

# Getting environment variables
mongo_uri = os.getenv("mongodbUri")
topic_name = os.getenv("topic_name")
bootstrap_servers = os.getenv("bootstrap_servers")
# Connecting to MongoDB
CLIENT = pymongo.MongoClient(os.getenv("mongodbUri"))
DB = CLIENT['scmxpertlite']
DATA_STREAM = DB["datastream"]

topicName = os.getenv("topic_name")    
# Retrieve topic name from environment variable
print(topicName)


try:
    # Initializeing Kafka consumer
    consumer = KafkaConsumer(topicName,bootstrap_servers = bootstrap_servers,auto_offset_reset = 'latest')
    # Consume messages from Kafka topic
    for message in consumer:
        try:
            # Load message value as JSON
            message_data = json.loads(message.value)
            print(message_data)
            # Insert message data into MongoDB
            DATA_STREAM.insert_one(message_data)
        except json.decoder.JSONDecodeError:
            continue
except KeyboardInterrupt:
    # Exit gracefully on keyboard interrupt
    sys.exit()
finally:
    # Close MongoDB client on completion
    CLIENT.close()