# These are like tools we need to use
import requests  # This helps us talk to websites on the internet
import pandas as pd  # This helps us organize data like a spreadsheet
import json  # This helps us work with JSON data structures
import urllib3  # This helps us handle SSL certificate warnings

# Disable SSL warnings (safe for trusted APIs like OpenWeather)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract(api_key, city):
    """
    This function extracts ALL available weather data from OpenWeather API
    and organizes it into a comprehensive pandas DataFrame.
    """
    
    # This is the website address where we ask about weather
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # These are the questions we're asking the weather website:
    # "q" = which city do you want to know about?
    # "appid" = this is like our ID card to prove we're allowed to ask
    # "units" = we want temperature in Celsius (not Fahrenheit)
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:  # Let's try to get the weather info, but be ready if something goes wrong
        
        # Go to the weather website and ask our questions
        # timeout=10 means "if it takes more than 10 seconds, give up"
        # verify=False bypasses SSL certificate issues (safe for OpenWeather API)
        response = requests.get(url, params=params, timeout=10, verify=False)
        
        # Check if the website gave us a good answer (not an error)
        response.raise_for_status()
        
        # Take the answer from the website and turn it into something we can use
        data = response.json()

        # Extract ALL available data from the API response
        record = {
            # Basic info
            "city_name": data.get("name", ""),
            "country_code": data.get("sys", {}).get("country", ""),
            "city_id": data.get("id", ""),
            "timezone": data.get("timezone", 0),
            "query_city": city,  # Original query for reference
            
            # Coordinates
            "longitude": data.get("coord", {}).get("lon", None),
            "latitude": data.get("coord", {}).get("lat", None),
            
            # Main weather data
            "temperature": data.get("main", {}).get("temp", None),
            "feels_like": data.get("main", {}).get("feels_like", None),
            "temp_min": data.get("main", {}).get("temp_min", None),
            "temp_max": data.get("main", {}).get("temp_max", None),
            "pressure": data.get("main", {}).get("pressure", None),  # hPa
            "humidity": data.get("main", {}).get("humidity", None),  # %
            "sea_level_pressure": data.get("main", {}).get("sea_level", None),  # hPa
            "ground_level_pressure": data.get("main", {}).get("grnd_level", None),  # hPa
            
            # Weather description
            "weather_main": data.get("weather", [{}])[0].get("main", "") if data.get("weather") else "",
            "weather_description": data.get("weather", [{}])[0].get("description", "") if data.get("weather") else "",
            "weather_icon": data.get("weather", [{}])[0].get("icon", "") if data.get("weather") else "",
            "weather_id": data.get("weather", [{}])[0].get("id", None) if data.get("weather") else None,
            
            # Wind data
            "wind_speed": data.get("wind", {}).get("speed", None),  # m/s
            "wind_direction": data.get("wind", {}).get("deg", None),  # degrees
            "wind_gust": data.get("wind", {}).get("gust", None),  # m/s
            
            # Clouds
            "cloudiness": data.get("clouds", {}).get("all", None),  # %
            
            # Rain data (if available)
            "rain_1h": data.get("rain", {}).get("1h", None) if data.get("rain") else None,  # mm
            "rain_3h": data.get("rain", {}).get("3h", None) if data.get("rain") else None,  # mm
            
            # Snow data (if available)
            "snow_1h": data.get("snow", {}).get("1h", None) if data.get("snow") else None,  # mm
            "snow_3h": data.get("snow", {}).get("3h", None) if data.get("snow") else None,  # mm
            
            # Visibility
            "visibility": data.get("visibility", None),  # meters
            
            # System data
            "sunrise": pd.to_datetime(data.get("sys", {}).get("sunrise", 0), unit='s', utc=True) if data.get("sys", {}).get("sunrise") else None,
            "sunset": pd.to_datetime(data.get("sys", {}).get("sunset", 0), unit='s', utc=True) if data.get("sys", {}).get("sunset") else None,
            
            # Timestamp data
            "data_timestamp": pd.to_datetime(data.get("dt", 0), unit='s', utc=True) if data.get("dt") else None,
            "extraction_timestamp": pd.Timestamp.now(tz='UTC'),
            
            # Raw data for reference (as JSON string)
            "raw_api_response": json.dumps(data)
        }

        # Turn our organized notes into a nice table (like a spreadsheet row)
        df = pd.DataFrame([record])
        return df  # Give back the table with weather information

    except requests.RequestException as e:  # Oops! Something went wrong
        # Tell someone what went wrong
        print(f"Error fetching weather data for {city}: {e}")
        # Give back an empty table instead of breaking everything
        return pd.DataFrame()
