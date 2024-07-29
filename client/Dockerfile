# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a directory for the app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code
COPY . /app

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "3000"]
