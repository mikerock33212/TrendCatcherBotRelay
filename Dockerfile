# Start with a standard, lightweight Python base image.
FROM python:3.11-slim

# Set an environment variable to ensure Python outputs logs immediately.
ENV PYTHONUNBUFFERED True

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install the libraries.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code.
COPY . .

# --- The Command to Start Your Application ---
# This starts the Gunicorn web server and tells it to listen on the port
# provided by Cloud Run's $PORT environment variable. It serves the 'app'
# object from your 'main.py' file.
CMD gunicorn main:app --bind 0.0.0.0:$PORT
