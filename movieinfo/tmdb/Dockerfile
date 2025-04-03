FROM python:3.11-slim

WORKDIR /app

COPY tmdb.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a .env file in the container for the API key
# The actual API key will be provided at runtime
RUN touch .env

ENTRYPOINT ["python", "tmdb.py"]