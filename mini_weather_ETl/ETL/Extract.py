# These are like tools we need to use
import requests  # This helps us talk to websites on the internet
import pandas as pd  # This helps us organize data like a spreadsheet

def extract(api_key, city):
    """
    This function is like asking the weather website: "What's the weather like in Toronto?"
    It gets the answer and puts it in a nice table for us to use.
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
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the website gave us a good answer (not an error)
        response.raise_for_status()
        
        # Take the answer from the website and turn it into something we can use
        data = response.json()

        # Now let's pick out the important weather information and organize it
        # It's like taking notes from a long weather report
        record = {
            "city": city,  # Which city this weather is for
            "temperature": data["main"]["temp"],  # How hot or cold it is
            "humidity": data["main"]["humidity"],  # How wet the air feels
            "weather": data["weather"][0]["description"],  # Is it sunny, cloudy, rainy?
            "wind_speed": data["wind"]["speed"],  # How fast the wind is blowing
            "timestamp": pd.Timestamp.now()  # What time we got this information
        }

        # Turn our organized notes into a nice table (like a spreadsheet row)
        df = pd.DataFrame([record])
        return df  # Give back the table with weather information

    except requests.RequestException as e:  # Oops! Something went wrong
        # Tell someone what went wrong
        print(f"Error fetching weather data for {city}: {e}")
        # Give back an empty table instead of breaking everything
        return pd.DataFrame()
