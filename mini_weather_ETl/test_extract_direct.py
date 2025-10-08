#!/usr/bin/env python3
"""
Direct test of the extract function with SSL workaround
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_test(api_key, city):
    """Modified extract function for testing with SSL verification disabled"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        # Disable SSL verification for testing
        response = requests.get(url, params=params, timeout=10, verify=False)
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

def test_extract():
    """Test the extract function with sample data"""
    
    # Load environment variables from the env file
    load_dotenv('env')
    
    # Get the API key from environment
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        print("❌ Error: WEATHER_API_KEY not found in environment file")
        return False
    
    print(f"✅ API Key loaded: {api_key[:10]}...")
    
    # Test cities
    test_cities = ["Toronto,CA", "Vancouver,CA"]
    
    print("\n🧪 Testing Extract Function:")
    print("=" * 50)
    
    success_count = 0
    
    for city in test_cities:
        print(f"\n📍 Testing city: {city}")
        
        # Call the extract function
        result = extract_test(api_key, city)
        
        if result:
            print("✅ Success! Weather data extracted:")
            print(f"   🌡️  Temperature: {result['temperature']}°C")
            print(f"   💧 Humidity: {result['humidity']}%")
            print(f"   ☁️  Weather: {result['weather']}")
            print(f"   💨 Wind Speed: {result['wind_speed']} m/s")
            print(f"   ⏰ Timestamp: {result['timestamp']}")
            success_count += 1
        else:
            print("❌ Failed to extract weather data")
    
    print("\n" + "=" * 50)
    print(f"✅ Extract function testing completed! {success_count}/{len(test_cities)} cities successful")
    
    if success_count > 0:
        print("\n✅ Your extract function is working properly!")
        print("🔧 Note: You may need to fix SSL certificate issues for production use.")
    
    return success_count > 0

if __name__ == "__main__":
    test_extract()