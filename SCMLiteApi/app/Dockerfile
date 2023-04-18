FROM python:3.9.0

# Copy the requirements file to the container
COPY . /exfproject/SCMLiteApi/app

# # Copy the requirements file to the container
COPY ./requirements.txt exfproject/SCMLiteApi/app/requirements.txt

# Set the working directory to /app
WORKDIR /exfproject/SCMLiteApi/app

# Install the dependencies
RUN apt-get update && apt-get install -y python3-pip && pip3 install -r requirements.txt

# Expose port 80 for the API
EXPOSE 8000

# Run the app
CMD [ "uvicorn", "main:APP", "--reload", "--host=0.0.0.0","--port= 8000"]