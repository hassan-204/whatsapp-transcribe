# Use an official Python runtime as a base image
FROM python:3.10-slim

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 9999 to the outside world
EXPOSE 9999

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9999"]
