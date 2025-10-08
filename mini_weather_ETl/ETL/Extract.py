import requests
import pandas as pd

def extract(api_key, city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": pd.Timestamp.now()
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data for {city}: {e}")
        return None

