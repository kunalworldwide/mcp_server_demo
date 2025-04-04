# Global Weather MCP Server

A Model Context Protocol (MCP) server that provides Claude with comprehensive global weather data using the WeatherAPI.com service.

## 🌦️ Features

- **Global Coverage**: Get weather for any location worldwide (not just US)
- **Current Weather**: Real-time weather conditions with temperature, wind, humidity, etc.
- **Forecasts**: Up to 14 days of detailed weather forecasts
- **Historical Weather**: Access historical weather data back to January 1, 2010
- **Astronomy**: Sunrise/sunset times, moon phases, and other astronomical data
- **Air Quality**: Pollution levels and air quality indices
- **Weather Alerts**: Warnings and advisories for severe weather conditions
- **Location Search**: Find locations matching a search query

## 📋 Prerequisites

- Python 3.11 or higher
- WeatherAPI.com API key (sign up for free at [weatherapi.com](https://www.weatherapi.com/))
- `httpx` for HTTP requests
- `mcp` package for the Model Context Protocol implementation

## 🚀 Installation

1. Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🛠️ Usage

### Setting Up Your API Key

You need to set your WeatherAPI.com API key as an environment variable:

```bash
# On Linux/macOS
export WEATHERAPI_KEY="your_api_key_here"

# On Windows (Command Prompt)
set WEATHERAPI_KEY=your_api_key_here

# On Windows (PowerShell)
$env:WEATHERAPI_KEY="your_api_key_here"
```

### Running the Server

```bash
python global_weather.py
```

### Running with Docker

```bash
# Build the Docker image
docker build -t weather-api-mcp .

# Run the container with your API key
docker run -e WEATHERAPI_KEY="your_api_key_here" weather-api-mcp
```

## 🌐 Available Tools

This server provides the following tools for Claude:

### 1. `get_current_weather`

Get real-time weather conditions for any location worldwide.

**Parameters**:
- `location`: Location name, latitude/longitude, IP address, or postal code (e.g., 'London', '48.8567,2.3508', '90210')

**Example response**:
```
Current Weather for London, City of London, United Kingdom
Local time: 2025-04-04 14:30

Temperature: 12.5°C / 54.5°F
Feels like: 10.2°C / 50.4°F
Condition: Partly cloudy
Wind: 15 km/h (9.3 mph) from W
Humidity: 76%
Precipitation: 0.1 mm
Cloud cover: 25%
UV Index: 4

Air Quality:
US EPA Index: 1 (Good)
CO: 250.3 μg/m³
NO₂: 12.5 μg/m³
O₃: 52.1 μg/m³
SO₂: 8.2 μg/m³
PM2.5: 4.8 μg/m³
PM10: 8.3 μg/m³
```

### 2. `get_forecast`

Get detailed weather forecasts for up to 14 days.

**Parameters**:
- `location`: Location name, latitude/longitude, IP address, or postal code
- `days` (optional): Number of days to forecast (1-14, default 3)

### 3. `get_astronomy`

Get astronomical data like sunrise, sunset, and moon phases.

**Parameters**:
- `location`: Location name, latitude/longitude, IP address, or postal code
- `date` (optional): Date in yyyy-MM-dd format (default is today)

### 4. `get_alerts`

Get weather alerts and warnings for a location.

**Parameters**:
- `location`: Location name, latitude/longitude, IP address, or postal code

### 5. `search_locations`

Search for locations that match a query string.

**Parameters**:
- `query`: Location search term (e.g., 'London', 'San Fran')

### 6. `get_historical_weather`

Get historical weather data for a specific date.

**Parameters**:
- `location`: Location name, latitude/longitude, IP address, or postal code
- `date`: Date in yyyy-MM-dd format (must be on or after January 1, 2010)

## 🔍 Troubleshooting

- **API Key Issues**: Ensure your WeatherAPI.com API key is correctly set as an environment variable.
- **Rate Limiting**: The free tier of WeatherAPI.com has usage limits. Check your dashboard if you're experiencing issues.
- **Location Not Found**: Try using latitude/longitude coordinates if a location name isn't recognized.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.