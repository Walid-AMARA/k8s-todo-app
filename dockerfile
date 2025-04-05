# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create the SQLite database directory with proper permissions
RUN mkdir -p /app/data && chmod 777 /app/data

# Expose port
EXPOSE $PORT

# Command to run the application
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
