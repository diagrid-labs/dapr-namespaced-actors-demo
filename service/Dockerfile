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

# Copy the Uvicorn app code
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["uvicorn", "smartbulb_actor_service:app", "--host", "0.0.0.0", "--port", "5000"]
