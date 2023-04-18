
# Base image
FROM python:3.9.0

# Set the working directory
WORKDIR /app/consumer

# Copy the socket server file to the container
COPY . /app/consumer

#run installation of libraries 
RUN pip install -r requirements.txt 
#run consumer.py
CMD python -u consumer.py

