# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y gcc curl

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8000

 # Start the application using Gunicorn with Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.main:app", "--bind", "0.0.0.0:8000"]