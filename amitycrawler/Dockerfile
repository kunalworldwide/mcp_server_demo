FROM python:3.11-slim

WORKDIR /app

# Copy the server script
COPY amity_crawler.py /app/

# Create requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for storing crawled information
RUN mkdir -p /app/amity_data

# Set the entrypoint
ENTRYPOINT ["python", "amity_crawler.py"]