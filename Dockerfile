# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and application files
COPY requirements.txt ./
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8080

# Command to run the application
CMD ["python", "receipt-processor.py"]

# docker build -t receipt-processor .
# docker run -p 8080:8080 receipt-processor