import requests

def extract(api_key, city="Montreal,CA"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an error if request failed
    return response.json()
