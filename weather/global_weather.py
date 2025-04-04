from typing import Any, Dict
import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
WEATHERAPI_BASE_URL = "http://api.weatherapi.com/v1"
API_KEY = os.environ.get("WEATHERAPI_KEY", "")  # Get API key from environment variable

async def make_weather_api_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to the WeatherAPI.com with proper error handling."""
    # Always include the API key in requests
    params["key"] = API_KEY
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WEATHERAPI_BASE_URL}/{endpoint}", params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP Error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg = f"API Error: {error_data['error']['message']} (Code: {error_data['error']['code']})"
            except:
                pass
            raise ValueError(error_msg)
        except Exception as e:
            raise ValueError(f"Request Error: {str(e)}")

@mcp.tool()
async def get_current_weather(location: str) -> str:
    """Get current weather for any location worldwide.
    
    Args:
        location: Location name, latitude/longitude, IP address, US/UK/Canada postal code
                 Examples: 'London', '48.8567,2.3508', '90210', 'auto:ip'
    """
    try:
        data = await make_weather_api_request("current.json", {"q": location, "aqi": "yes"})
        
        # Format the response in a readable way
        location_info = data["location"]
        current = data["current"]
        condition = current["condition"]["text"]
        
        response = "Current Weather for {}, {}, {}\n".format(
            location_info['name'], location_info['region'], location_info['country'])
        response += "Local time: {}\n\n".format(location_info['localtime'])
        response += "Temperature: {}°C / {}°F\n".format(current['temp_c'], current['temp_f'])
        response += "Feels like: {}°C / {}°F\n".format(current['feelslike_c'], current['feelslike_f'])
        response += "Condition: {}\n".format(condition)
        response += "Wind: {} km/h ({} mph) from {}\n".format(
            current['wind_kph'], current['wind_mph'], current['wind_dir'])
        response += "Humidity: {}%\n".format(current['humidity'])
        response += "Precipitation: {} mm\n".format(current['precip_mm'])
        response += "Cloud cover: {}%\n".format(current['cloud'])
        response += "UV Index: {}\n".format(current['uv'])

        # Add air quality data if available
        if "air_quality" in current:
            aqi = current["air_quality"]
            response += "\nAir Quality:\n"
            response += "US EPA Index: {} ({})\n".format(
                aqi.get('us-epa-index', 'N/A'), get_aqi_description(aqi.get('us-epa-index')))
            response += "CO: {} μg/m3\n".format(aqi.get('co', 'N/A'))
            response += "NO2: {} μg/m3\n".format(aqi.get('no2', 'N/A'))
            response += "O3: {} μg/m3\n".format(aqi.get('o3', 'N/A'))
            response += "SO2: {} μg/m3\n".format(aqi.get('so2', 'N/A'))
            response += "PM2.5: {} μg/m3\n".format(aqi.get('pm2_5', 'N/A'))
            response += "PM10: {} μg/m3\n".format(aqi.get('pm10', 'N/A'))
            
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> str:
    """Get weather forecast for any location worldwide.
    
    Args:
        location: Location name, latitude/longitude, IP address, US/UK/Canada postal code
                 Examples: 'London', '48.8567,2.3508', '90210', 'auto:ip'
        days: Number of days to forecast (1-14, default 3)
    """
    if days < 1 or days > 14:
        return "Error: 'days' parameter must be between 1 and 14"
    
    try:
        data = await make_weather_api_request("forecast.json", {"q": location, "days": days, "aqi": "yes", "alerts": "yes"})
        
        location_info = data["location"]
        forecast_days = data["forecast"]["forecastday"]
        
        response = "Weather Forecast for {}, {}, {}\n\n".format(
            location_info['name'], location_info['region'], location_info['country'])
        
        for day in forecast_days:
            date = day["date"]
            day_data = day["day"]
            astro = day["astro"]
            
            response += "Date: {}\n".format(date)
            response += "Temperature: {}°C to {}°C / {}°F to {}°F\n".format(
                day_data['mintemp_c'], day_data['maxtemp_c'], 
                day_data['mintemp_f'], day_data['maxtemp_f'])
            response += "Condition: {}\n".format(day_data['condition']['text'])
            response += "Chance of Rain: {}%\n".format(day_data['daily_chance_of_rain'])
            response += "Chance of Snow: {}%\n".format(day_data['daily_chance_of_snow'])
            response += "Total Precipitation: {} mm\n".format(day_data['totalprecip_mm'])
            response += "Max Wind: {} km/h\n".format(day_data['maxwind_kph'])
            response += "Humidity: {}%\n".format(day_data['avghumidity'])
            response += "UV Index: {}\n\n".format(day_data['uv'])
            response += "Sunrise: {} | Sunset: {}\n".format(astro['sunrise'], astro['sunset'])
            response += "Moonrise: {} | Moonset: {}\n".format(astro['moonrise'], astro['moonset'])
            response += "Moon Phase: {}\n\n".format(astro['moon_phase'])
            response += "----- Hourly Breakdown -----\n"
            
            # Include a few key hours rather than all 24
            hours = [0, 6, 12, 18]  # Midnight, 6am, Noon, 6pm
            for hour_idx in hours:
                hour_data = day["hour"][hour_idx]
                time = hour_data["time"].split()[1]  # Get just the time part
                response += "{}: {}°C, {}, Wind: {} km/h\n".format(
                    time, hour_data['temp_c'], hour_data['condition']['text'], hour_data['wind_kph'])
            
            response += "\n---\n\n"
        
        # Add alerts if present
        if "alerts" in data and "alert" in data["alerts"] and data["alerts"]["alert"]:
            response += "WEATHER ALERTS\n\n"
            for alert in data["alerts"]["alert"]:
                response += "Alert: {}\n".format(alert.get('event', 'Unknown'))
                response += "Severity: {}\n".format(alert.get('severity', 'Unknown'))
                response += "Effective: {}\n".format(alert.get('effective', 'Unknown'))
                response += "Expires: {}\n".format(alert.get('expires', 'Unknown'))
                desc = alert.get('desc', 'No description')
                if desc and '\n' in desc:
                    desc = desc.split('\n')[0]
                response += "Description: {}\n\n".format(desc)
        
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

@mcp.tool()
async def get_astronomy(location: str, date: str = "") -> str:
    """Get astronomy information for any location.
    
    Args:
        location: Location name, latitude/longitude, IP address, postal code
        date: Date in yyyy-MM-dd format (default is today)
    """
    params = {"q": location}
    if date:
        params["dt"] = date
    
    try:
        data = await make_weather_api_request("astronomy.json", params)
        
        location_info = data["location"]
        astronomy = data["astronomy"]["astro"]
        
        response = "Astronomy Information for {}, {}, {}\n".format(
            location_info['name'], location_info['region'], location_info['country'])
        response += "Date: {}\n\n".format(data['astronomy'].get('date', 'Today'))
        response += "Sunrise: {}\n".format(astronomy['sunrise'])
        response += "Sunset: {}\n".format(astronomy['sunset'])
        response += "Moonrise: {}\n".format(astronomy['moonrise'])
        response += "Moonset: {}\n".format(astronomy['moonset'])
        response += "Moon Phase: {}\n".format(astronomy['moon_phase'])
        response += "Moon Illumination: {}%\n".format(astronomy['moon_illumination'])
        
        if 'is_sun_up' in astronomy:
            is_sun_up_text = 'up' if astronomy['is_sun_up'] == 1 else 'down'
            response += "Sun is currently {}\n".format(is_sun_up_text)
        if 'is_moon_up' in astronomy:
            is_moon_up_text = 'up' if astronomy['is_moon_up'] == 1 else 'down'
            response += "Moon is currently {}\n".format(is_moon_up_text)
        
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

@mcp.tool()
async def search_locations(query: str) -> str:
    """Search for locations that match a query string.
    
    Args:
        query: Location search term (e.g. 'London', 'San Fran')
    """
    try:
        data = await make_weather_api_request("search.json", {"q": query})
        
        if not data:
            return "No locations found matching '{}'".format(query)
        
        response = "Locations matching '{}':\n\n".format(query)
        
        for location in data:
            response += "Name: {}\n".format(location.get('name', 'Unknown'))
            response += "Region: {}\n".format(location.get('region', 'Unknown'))
            response += "Country: {}\n".format(location.get('country', 'Unknown'))
            response += "Latitude: {}\n".format(location.get('lat', 'Unknown'))
            response += "Longitude: {}\n\n".format(location.get('lon', 'Unknown'))
        
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

@mcp.tool()
async def get_alerts(location: str) -> str:
    """Get weather alerts/warnings for a location.
    
    Args:
        location: Location name, latitude/longitude, IP address, postal code
    """
    try:
        # We use the forecast endpoint with alerts=yes to get alert data
        data = await make_weather_api_request("forecast.json", {"q": location, "days": 1, "alerts": "yes"})
        
        location_info = data["location"]
        
        if "alerts" not in data or "alert" not in data["alerts"] or not data["alerts"]["alert"]:
            return "No active weather alerts for {}, {}.".format(location_info['name'], location_info['country'])
        
        alerts = data["alerts"]["alert"]
        response = "Weather Alerts for {}, {}, {}\n\n".format(
            location_info['name'], location_info['region'], location_info['country'])
        
        for alert in alerts:
            response += "Event: {}\n".format(alert.get('event', 'Unknown'))
            response += "Severity: {}\n".format(alert.get('severity', 'Unknown'))
            response += "Urgency: {}\n".format(alert.get('urgency', 'Unknown'))
            response += "Areas: {}\n".format(alert.get('areas', 'Unknown'))
            response += "Category: {}\n".format(alert.get('category', 'Unknown'))
            response += "Effective: {}\n".format(alert.get('effective', 'Unknown'))
            response += "Expires: {}\n".format(alert.get('expires', 'Unknown'))
            
            desc = alert.get('desc', 'No description available')
            if len(desc) > 300:
                desc = desc[:300] + "..."
            response += "Description: {}\n".format(desc)
            
            instruction = alert.get('instruction', 'No specific instructions provided')
            if len(instruction) > 300:
                instruction = instruction[:300] + "..."
            response += "Instructions: {}\n\n---\n\n".format(instruction)
        
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

@mcp.tool()
async def get_historical_weather(location: str, date: str) -> str:
    """Get historical weather for a location on a specific date.
    
    Args:
        location: Location name, latitude/longitude, IP address, postal code
        date: Date in yyyy-MM-dd format (must be on or after 1st Jan, 2010)
    """
    try:
        data = await make_weather_api_request("history.json", {"q": location, "dt": date})
        
        location_info = data["location"]
        history_day = data["forecast"]["forecastday"][0]["day"]
        
        response = "Historical Weather for {}, {}, {}\n".format(
            location_info['name'], location_info['region'], location_info['country'])
        response += "Date: {}\n\n".format(data['forecast']['forecastday'][0]['date'])
        
        response += "Temperature: {}°C to {}°C / {}°F to {}°F\n".format(
            history_day['mintemp_c'], history_day['maxtemp_c'], 
            history_day['mintemp_f'], history_day['maxtemp_f'])
        response += "Average Temperature: {}°C / {}°F\n".format(history_day['avgtemp_c'], history_day['avgtemp_f'])
        response += "Condition: {}\n".format(history_day['condition']['text'])
        response += "Max Wind: {} km/h ({} mph)\n".format(history_day['maxwind_kph'], history_day['maxwind_mph'])
        response += "Total Precipitation: {} mm ({} in)\n".format(history_day['totalprecip_mm'], history_day['totalprecip_in'])
        response += "Average Humidity: {}%\n".format(history_day['avghumidity'])
        response += "UV Index: {}\n\n".format(history_day['uv'])

        # Add some hourly data
        response += "Hourly Breakdown (selected hours):\n"
        hours = [0, 6, 12, 18]  # Midnight, 6am, Noon, 6pm
        for hour_idx in hours:
            hour_data = data["forecast"]["forecastday"][0]["hour"][hour_idx]
            time = hour_data["time"].split()[1]  # Get just the time part
            response += "{}: {}°C, {}, Wind: {} km/h\n".format(
                time, hour_data['temp_c'], hour_data['condition']['text'], hour_data['wind_kph'])
            
        return response
    except ValueError as e:
        return "Error: {}".format(str(e))
    except Exception as e:
        return "Unexpected error occurred: {}".format(str(e))

# Helper functions
def get_aqi_description(aqi_index):
    """Return a description based on the US EPA AQI index."""
    if not aqi_index:
        return "Unknown"
        
    descriptions = {
        1: "Good",
        2: "Moderate",
        3: "Unhealthy for sensitive groups",
        4: "Unhealthy",
        5: "Very Unhealthy",
        6: "Hazardous"
    }
    return descriptions.get(aqi_index, "Unknown")

if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: No WeatherAPI.com API key provided. Set the WEATHERAPI_KEY environment variable.")
        print("You can sign up for a free API key at https://www.weatherapi.com/")
    
    # Initialize and run the server
    mcp.run(transport='stdio')