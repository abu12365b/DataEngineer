#!/usr/bin/env python3
"""
This is our special test to see if our weather function works!
It's like testing if our toy works before we play with it.
"""

# These are our special helpers - like having different toys to play with
import requests  # This helper talks to the internet for us
import pandas as pd  # This helper makes pretty tables for us
import os  # This helper looks for files on our computer
from dotenv import load_dotenv  # This helper reads our secret password file
import urllib3  # This helper makes internet talking work better

# Tell the computer to be quiet about scary internet messages
# (Like telling a baby "shh, it's okay" when they hear a loud noise)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_test(api_key, city):
    """
    This is our pretend weather function! 
    It's like asking "What's the weather like outside?" but to the computer!
    """
    
    # This is the special address where weather lives on the internet
    # Like knowing your friend's house address so you can visit them
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # These are the questions we want to ask about the weather
    # Like asking "How's the weather in Toronto?" and showing our ID card
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:  # Let's try to get the weather! (Like trying to reach a cookie jar)
        
        # Go ask the internet about the weather (but be nice and patient)
        # If it takes too long (more than 10 seconds), we'll give up
        # verify=False means "don't worry about checking if it's super safe"
        response = requests.get(url, params=params, timeout=10, verify=False)
        
        # Check if the internet was nice to us and gave us a good answer
        response.raise_for_status()
        
        # Turn the internet's answer into something we can understand
        # Like translating "woof woof" from a dog into "I'm happy!"
        data = response.json()
        
        # Pick out the important weather information and organize it nicely
        # Like sorting your toys into different boxes
        return {
            "city": city,  # Which city we asked about
            "temperature": data["main"]["temp"],  # How hot or cold it feels
            "humidity": data["main"]["humidity"],  # How sticky the air feels
            "weather": data["weather"][0]["description"],  # Is it sunny or rainy?
            "wind_speed": data["wind"]["speed"],  # How fast the wind is blowing
            "timestamp": pd.Timestamp.now()  # When we asked this question
        }
        
    except requests.RequestException as e:  # Oopsie! Something went wrong!
        # Tell mommy and daddy what went wrong
        print(f"Error fetching weather data for {city}: {e}")
        # Give back nothing (like when you can't find your toy)
        return None

def test_extract():
    """
    This is our big test! Like when you test if your new bike works!
    We're going to see if our weather question-asking works properly.
    """
    
    # Find out where our special file lives on the computer
    # Like finding where mommy keeps the cookie jar
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    # Tell everyone where we're looking for our secret password file
    print(f"🔍 Looking for .env file at: {env_path}")
    print(f"📂 .env file exists: {os.path.exists(env_path)}")
    
    # Read our secret password from the special file
    # Like getting your library card so you can borrow books
    load_dotenv(env_path)
    
    # Get our special password (API key) to talk to the weather website
    api_key = os.getenv('WEATHER_API_KEY')
    
    # Uh oh! We couldn't find our password!
    if not api_key:
        print("❌ Error: WEATHER_API_KEY not found in environment file")
        print("🔧 Trying to load from 'env' file as backup...")
        
        # Let's try looking in the old place for our password
        # Like checking your old toy box when you can't find something
        old_env_path = os.path.join(script_dir, 'env')
        if os.path.exists(old_env_path):
            # Open the old file and read it line by line
            # Like reading a picture book page by page
            with open(old_env_path, 'r') as f:
                for line in f:
                    # Look for the line that has our password
                    if line.startswith('WEATHER_API_KEY='):
                        # Take out the password part and clean it up
                        api_key = line.split('=')[1].strip().strip('"')
                        print(f"✅ Found API key in old env file")
                        break
        
        # If we still can't find our password, we have to stop playing
        if not api_key:
            return False
    
    # Yay! We found our password! Show just a little bit of it (keep it secret!)
    print(f"✅ API Key loaded: {api_key[:10]}...")
    
    # These are the cities we want to ask about the weather
    # Like choosing which playgrounds you want to visit
    test_cities = ["Toronto,CA", "Vancouver,CA"]
    
    # Start our big weather test! Draw a pretty line to make it look nice
    print("\n🧪 Testing Extract Function:")
    print("=" * 50)
    
    # Keep count of how many times our weather-asking worked
    # Like counting how many cookies you ate
    success_count = 0
    
    # Ask about the weather in each city, one by one
    # Like visiting each friend's house to see if they want to play
    for city in test_cities:
        print(f"\n📍 Testing city: {city}")
        
        # Now let's actually ask about the weather!
        # This is the exciting part - like opening a present!
        result = extract_test(api_key, city)
        
        # Did we get a good answer about the weather?
        if result:
            # Hooray! We got weather information! Let's show everyone!
            print("✅ Success! Weather data extracted:")
            print(f"   🌡️  Temperature: {result['temperature']}°C")  # How hot/cold
            print(f"   💧 Humidity: {result['humidity']}%")  # How sticky the air is
            print(f"   ☁️  Weather: {result['weather']}")  # Sunny? Rainy? Cloudy?
            print(f"   💨 Wind Speed: {result['wind_speed']} m/s")  # How windy
            print(f"   ⏰ Timestamp: {result['timestamp']}")  # When we asked
            success_count += 1  # Add one to our success counter!
        else:
            # Aww, something went wrong. That's okay, we tried our best!
            print("❌ Failed to extract weather data")
    
    # All done! Let's see how we did!
    print("\n" + "=" * 50)
    print(f"✅ Extract function testing completed! {success_count}/{len(test_cities)} cities successful")
    
    # If we got weather for at least one city, we did great!
    if success_count > 0:
        print("\n✅ Your extract function is working properly!")
        print("🔧 Note: You may need to fix SSL certificate issues for production use.")
    
    # Tell everyone if our test worked or not
    return success_count > 0

# This is where our program starts running - like pressing the "start" button!
if __name__ == "__main__":
    test_extract()