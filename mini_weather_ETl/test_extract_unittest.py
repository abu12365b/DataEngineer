#!/usr/bin/env python3
"""
These are our super special tests! 
Like when you test if all your toys work before you play with them!
We're going to pretend to ask about weather and see if our function is a good listener.
"""

# These are our helper friends that make testing fun!
import unittest  # This helper makes sure our tests work properly
import sys  # This helper talks to the computer system  
import os  # This helper finds files on our computer
from unittest.mock import patch, MagicMock  # These helpers let us pretend and play make-believe
import pandas as pd  # This helper makes pretty tables for us

# Tell the computer where to find our weather function
# Like telling your friend where you keep your favorite toys
sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))

class TestExtractFunction(unittest.TestCase):
    """
    This is our special test playground! 
    Like a sandbox where we play pretend to see if our weather function works!
    """
    
    def setUp(self):
        """
        This gets our toys ready before we start playing!
        Like getting your crayons and paper ready before you draw!
        """
        # Our pretend password and city to test with
        # Like choosing which toy cars to play with
        self.api_key = "test_api_key"
        self.city = "Toronto,CA"
        
        # This is our pretend comprehensive weather answer that we'll use for testing
        # Like having a detailed conversation about all aspects of weather
        self.mock_response_data = {
            "coord": {"lon": -79.3832, "lat": 43.6532},
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 25.5,
                "feels_like": 27.2,
                "temp_min": 23.1,
                "temp_max": 28.0,
                "pressure": 1013,
                "humidity": 60,
                "sea_level": 1013,
                "grnd_level": 1008
            },
            "visibility": 10000,
            "wind": {
                "speed": 5.5,
                "deg": 220,
                "gust": 8.2
            },
            "clouds": {
                "all": 20
            },
            "rain": {
                "1h": 0.5,
                "3h": 1.2
            },
            "dt": 1696867200,
            "sys": {
                "type": 2,
                "id": 2043265,
                "country": "CA",
                "sunrise": 1696848600,
                "sunset": 1696890000
            },
            "timezone": -14400,
            "id": 6167865,
            "name": "Toronto",
            "cod": 200
        }
    
    @patch('ETL.Extract.requests.get')
    def test_extract_success(self, mock_get):
        """
        This test checks if our weather function works when everything goes perfectly!
        Like testing if your bike works when you have good weather and a smooth road!
        """
        from ETL.Extract import extract
        
        # Let's pretend the internet gives us a perfect answer
        # Like when you ask "Can I have a cookie?" and mommy says "Yes!"
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None  # No problems here!
        mock_response.json.return_value = self.mock_response_data  # Give our pretend weather
        mock_get.return_value = mock_response  # This is our pretend internet answer
        
        # Now let's actually test our weather function!
        # Like finally trying to ride your bike after checking all the parts!
        result = extract(self.api_key, self.city)
        
        # Time to check if everything worked perfectly!
        # Like checking if your drawing has all the right colors
        self.assertIsNotNone(result)  # Make sure we got something back (not nothing!)
        self.assertFalse(result.empty)  # Make sure our table isn't empty (has stuff in it!)
        self.assertEqual(len(result), 1)  # Make sure we got exactly one row of weather info
        
        # Check basic info
        self.assertEqual(result.iloc[0]['query_city'], self.city)  # Check original query
        self.assertEqual(result.iloc[0]['city_name'], 'Toronto')  # Check actual city name
        self.assertEqual(result.iloc[0]['country_code'], 'CA')  # Check country code
        
        # Check coordinates
        self.assertEqual(result.iloc[0]['longitude'], -79.3832)
        self.assertEqual(result.iloc[0]['latitude'], 43.6532)
        
        # Check temperature data
        self.assertEqual(result.iloc[0]['temperature'], 25.5)
        self.assertEqual(result.iloc[0]['feels_like'], 27.2)
        self.assertEqual(result.iloc[0]['temp_min'], 23.1)
        self.assertEqual(result.iloc[0]['temp_max'], 28.0)
        
        # Check atmospheric data
        self.assertEqual(result.iloc[0]['humidity'], 60)
        self.assertEqual(result.iloc[0]['pressure'], 1013)
        
        # Check weather description
        self.assertEqual(result.iloc[0]['weather_description'], 'clear sky')
        self.assertEqual(result.iloc[0]['weather_main'], 'Clear')
        
        # Check wind data
        self.assertEqual(result.iloc[0]['wind_speed'], 5.5)
        self.assertEqual(result.iloc[0]['wind_direction'], 220)
        self.assertEqual(result.iloc[0]['wind_gust'], 8.2)
        
        # Check other data
        self.assertEqual(result.iloc[0]['cloudiness'], 20)
        self.assertEqual(result.iloc[0]['visibility'], 10000)
        self.assertEqual(result.iloc[0]['rain_1h'], 0.5)
        
        # Check timestamps
        self.assertIsInstance(result.iloc[0]['extraction_timestamp'], pd.Timestamp)
        self.assertIsInstance(result.iloc[0]['data_timestamp'], pd.Timestamp)
        self.assertIsInstance(result.iloc[0]['sunrise'], pd.Timestamp)
        self.assertIsInstance(result.iloc[0]['sunset'], pd.Timestamp)
    
    @patch('ETL.Extract.requests.get')
    def test_extract_api_error(self, mock_get):
        """
        This test checks what happens when something goes wrong!
        Like testing what happens if your bike chain breaks while you're riding!
        """
        from ETL.Extract import extract
        import requests
        
        # Let's pretend the internet is having a bad day and can't help us
        # Like when you ask for a cookie but the cookie jar is empty
        mock_get.side_effect = requests.RequestException("API Error")
        
        # Now let's see what our function does when things go wrong
        # Like seeing if you cry or if you try to fix your broken toy
        result = extract(self.api_key, self.city)
        
        # Check that our function handled the problem nicely
        # Like checking that you didn't break anything else when your toy broke
        self.assertIsInstance(result, pd.DataFrame)  # Make sure we still got a table back
        self.assertTrue(result.empty)  # But the table should be empty (no weather info)
    
    def test_extract_data_structure(self):
        """
        This test checks if our weather table has all the right columns!
        Like checking if your coloring book has all the right pictures to color!
        """
        from ETL.Extract import extract
        
        # These are all the things we expect to see in our comprehensive weather table
        # Like a list of all the toys that should be in your expanded toy box
        expected_columns = [
            'city_name', 'country_code', 'city_id', 'timezone', 'query_city',
            'longitude', 'latitude',
            'temperature', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity',
            'sea_level_pressure', 'ground_level_pressure',
            'weather_main', 'weather_description', 'weather_icon', 'weather_id',
            'wind_speed', 'wind_direction', 'wind_gust',
            'cloudiness', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h', 'visibility',
            'sunrise', 'sunset', 'data_timestamp', 'extraction_timestamp', 'raw_api_response'
        ]
        
        # Let's pretend to get weather info so we can check the table structure
        # Like playing pretend restaurant to see if you know how to set the table
        with patch('ETL.Extract.requests.get') as mock_get:
            # Set up our pretend internet answer (like preparing pretend food)
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None  # Everything is okay!
            mock_response.json.return_value = self.mock_response_data  # Here's our pretend weather
            mock_get.return_value = mock_response  # Give this pretend answer to our function
            
            # Ask our function for weather info
            result = extract(self.api_key, self.city)
            
            # Now let's check if our weather table looks right!
            # Like checking if you put all the forks and spoons in the right places
            self.assertIsInstance(result, pd.DataFrame)  # Make sure it's a proper table
            self.assertFalse(result.empty)  # Make sure the table has something in it
            for column in expected_columns:  # Check each column one by one
                self.assertIn(column, result.columns)  # Make sure each column is there!

if __name__ == '__main__':
    # Time to start all our tests! Like pressing the "start" button on your favorite game!
    # verbosity=2 means "tell us everything that happens" (like being a chatty friend)
    unittest.main(verbosity=2)