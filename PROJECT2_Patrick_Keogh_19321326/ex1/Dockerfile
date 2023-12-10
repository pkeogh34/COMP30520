# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install pika, or any other dependencies you might have
RUN pip install pika

# Keep the container running
CMD ["tail", "-f", "/dev/null"]
