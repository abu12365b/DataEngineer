import requests

def extract(api_key, city):
    """
    Fetch current weather data for a city from OpenWeatherMap API.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # raise error if API call fails
    return response.json()


data = extract("c3ad1f1d0028cb8c255bc023fa21d67a", "Montreal,CA")
print(data)