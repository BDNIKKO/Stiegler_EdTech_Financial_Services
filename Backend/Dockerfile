# Use official Python slim image for smaller footprint
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Install required dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the backend code and models into the container
COPY . /app

# Expose Flask port (5000) for communication
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
