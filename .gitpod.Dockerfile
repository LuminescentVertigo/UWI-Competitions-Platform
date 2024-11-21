# Use an official Python runtime as a parent image
FROM python:3.10-slim  # Or python:3.9-slim if needed

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for git and mysqlclient
RUN apt-get update && apt-get install -y \
    git \
    default-libmysqlclient-dev gcc pkg-config && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8085 for the Flask app
EXPOSE 8085

# Run gunicorn when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
