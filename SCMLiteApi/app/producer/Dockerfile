
# Base image
FROM python:3.9.0

# Copy the socket server file to the container
COPY . /exfProject/SCMLiteApi/app/producer

# Set the working directory
WORKDIR /exfProject/SCMLiteApi/app/producer
#install dottenv and kafka-python
RUN pip3 install python-dotenv kafka-python

# Run the socket server
CMD ["python3", "producer.py"]
