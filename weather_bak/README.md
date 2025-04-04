# Weather Service MCP Server

A Model Context Protocol (MCP) server that provides Claude with real-time weather forecasts and alerts using the National Weather Service (NWS) API.

## 🌦️ Features

- **Weather Forecasts**: Get detailed forecasts for any US location by latitude and longitude
- **Weather Alerts**: Retrieve active weather alerts for any US state
- **Free Access**: Uses the public National Weather Service API (no API key required)

## 📋 Prerequisites

- Python 3.11 or higher
- `httpx` for HTTP requests
- `mcp` package for the Model Context Protocol implementation

## 🚀 Installation

1. Create and activate a virtual environment:

```bash
# Navigate to the weather directory
cd weather

# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
uv pip install -r requirements.txt
```

## 🛠️ Usage

### Running the Server

```bash
uv run weather.py
```

### Available Tools

This server provides the following tools for Claude:

#### 1. `get_forecast`

Get a detailed weather forecast for a specific location.

**Parameters**:
- `latitude`: Latitude of the location (float)
- `longitude`: Longitude of the location (float)

**Example response**:
```
Tonight:
Temperature: 45°F
Wind: 5 to 10 mph S
Forecast: Partly cloudy, with a low around 45. South wind 5 to 10 mph.

---

Monday:
Temperature: 68°F
Wind: 5 to 10 mph S
Forecast: Mostly sunny, with a high near 68. South wind 5 to 10 mph.
```

#### 2. `get_alerts`

Get active weather alerts for a specific US state.

**Parameters**:
- `state`: Two-letter US state code (e.g., CA, NY, TX)

**Example response**:
```
Event: Flood Watch
Area: Northern California Coast
Severity: Moderate
Description: The National Weather Service has issued a Flood Watch...
Instructions: Monitor forecasts and be prepared to take action...

---

Event: High Wind Warning
Area: San Francisco Bay Area
Severity: Severe
Description: Strong winds expected with gusts up to 60 mph...
Instructions: Secure outdoor objects and be prepared for power outages...
```

## 🔄 How It Works

1. When Claude needs weather information, it calls the appropriate tool on this server.
2. The server makes requests to the National Weather Service API.
3. The data is formatted into a human-readable format and returned to Claude.
4. Claude can then provide this weather information to the user.

## 🔍 Troubleshooting

- **"Unable to fetch forecast data for this location"**: The provided coordinates may be outside of the United States (the NWS API only covers US territories).
- **"Unable to fetch detailed forecast"**: This can happen if the NWS API is experiencing issues or if the specific forecast endpoint is unavailable.
- **"Unable to fetch alerts or no alerts found"**: Check that you've used a valid two-letter US state code.

## 🔧 Extending the Server

You can extend this weather server by:

1. Adding more NWS API endpoints as new tools
2. Implementing location search by city name (would require a geocoding service)
3. Adding historical weather data functionality

## 📜 License

This project is licensed under the MIT License - see the LICENSE file in the root directory for details.