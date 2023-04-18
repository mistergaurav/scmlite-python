import random
import json
import time
import socket

# Define the data structure
data = {
    "Battery_Level": 0.0,
    "Device_Id": 0,
    "First_Sensor_temperature": 0.0,
    "Route_From": "",
    "Route_To": ""
}


cities = ["Hyderabad, India", "Louisville, USA", "Paris, France", "Sydney, Australia", "Beijing, China"]

# Create a socket and start listening
s = socket.socket()
s.bind(('', 12345))
s.listen(3)
print("Waiting for connections...")
c, addr = s.accept()
print("Connected with", addr)

# Loop to generate and send random data
while True:
    # Generate random data
    data["Battery_Level"] = round(random.uniform(2.5, 4.0), 1)
    data["Device_Id"] = random.randint(1000000000, 9999999999)
    data["First_Sensor_temperature"] = round(random.uniform(18.0, 25.0), 1)
    data["Route_From"] = random.choice(cities)
    data["Route_To"] = random.choice(cities)

    # Convert data to JSON and encode it as UTF-8
    userdata = (json.dumps(data) + "\n").encode('utf-8')

    # Send the data and wait for 5 seconds
    c.send(userdata)
    print(userdata)
    time.sleep(5)

# Close the connection
c.close()
