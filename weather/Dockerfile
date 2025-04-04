FROM python:3.11-slim

WORKDIR /app

COPY global_weather.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# The API key should be provided as an environment variable at runtime
# Example: docker run -e WEATHERAPI_KEY=your_api_key_here weather-api-mcp

ENTRYPOINT ["python", "global_weather.py"]