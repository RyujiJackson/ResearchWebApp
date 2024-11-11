# Use Python 3.7.13 as the base image
FROM python:3.7.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 to match Cloud Run's expected port
EXPOSE 8080

# Command to run your app
CMD ["python", "main.py"]
