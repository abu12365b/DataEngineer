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
    Test the actual extract function with comprehensive data extraction
    """
    # Import the updated extract function
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))
    
    try:
        from ETL.Extract import extract
        
        # Use the actual extract function
        df = extract(api_key, city)
        
        if not df.empty:
            # Convert DataFrame to dictionary for display
            record = df.iloc[0].to_dict()
            return record
        else:
            return None
            
    except Exception as e:
        print(f"Error testing extract function for {city}: {e}")
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
            print("✅ Success! Comprehensive weather data extracted:")
            print(f"   �️  City: {result.get('city_name', 'N/A')}, {result.get('country_code', 'N/A')}")
            print(f"   🌍 Coordinates: {result.get('latitude', 'N/A')}, {result.get('longitude', 'N/A')}")
            print(f"   �🌡️  Temperature: {result.get('temperature', 'N/A')}°C (feels like {result.get('feels_like', 'N/A')}°C)")
            print(f"   🌡️  Min/Max: {result.get('temp_min', 'N/A')}°C / {result.get('temp_max', 'N/A')}°C")
            print(f"   💧 Humidity: {result.get('humidity', 'N/A')}%")
            print(f"   📊 Pressure: {result.get('pressure', 'N/A')} hPa")
            print(f"   ☁️  Weather: {result.get('weather_main', 'N/A')} - {result.get('weather_description', 'N/A')}")
            print(f"   ☁️  Cloudiness: {result.get('cloudiness', 'N/A')}%")
            print(f"   💨 Wind: {result.get('wind_speed', 'N/A')} m/s at {result.get('wind_direction', 'N/A')}°")
            if result.get('wind_gust'):
                print(f"   💨 Wind Gust: {result.get('wind_gust', 'N/A')} m/s")
            print(f"   👁️  Visibility: {result.get('visibility', 'N/A')} meters")
            if result.get('rain_1h') or result.get('rain_3h'):
                print(f"   🌧️  Rain: {result.get('rain_1h', 0)}mm (1h), {result.get('rain_3h', 0)}mm (3h)")
            if result.get('snow_1h') or result.get('snow_3h'):
                print(f"   ❄️  Snow: {result.get('snow_1h', 0)}mm (1h), {result.get('snow_3h', 0)}mm (3h)")
            print(f"   🌅 Sunrise: {result.get('sunrise', 'N/A')}")
            print(f"   🌇 Sunset: {result.get('sunset', 'N/A')}")
            print(f"   ⏰ Data Time: {result.get('data_timestamp', 'N/A')}")
            print(f"   📥 Extracted: {result.get('extraction_timestamp', 'N/A')}")
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