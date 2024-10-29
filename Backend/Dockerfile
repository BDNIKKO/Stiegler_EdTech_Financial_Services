# Use official Python slim image for smaller footprint
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code and models into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose Flask port (5000) for communication
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]