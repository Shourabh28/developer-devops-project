# Use a minimal base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Set the working directory
COPY requirements.txt ./

# Install necessary packages
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose necessary ports
EXPOSE 4000

# Run the application
CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]