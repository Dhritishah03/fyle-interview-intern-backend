# Use an official Python image as the base image
FROM python:3.8-slim

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variable for Flask
ENV FLASK_APP=core/server.py

# Expose the Flask default port
EXPOSE 5000

# Command to reset the database (optional, depending on your use case)
RUN rm -f core/store.sqlite3
RUN flask db upgrade -d core/migrations/

# Make the run.sh script executable
RUN chmod +x run.sh

# Set the entry point to bash and pass the script as argument
ENTRYPOINT ["bash", "run.sh"]
