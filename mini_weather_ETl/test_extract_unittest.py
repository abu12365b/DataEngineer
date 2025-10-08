#!/usr/bin/env python3
"""
Unit tests for the Extract function
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the ETL directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ETL'))

class TestExtractFunction(unittest.TestCase):
    """Unit tests for the extract function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api_key = "test_api_key"
        self.city = "Toronto,CA"
        
        # Mock response data
        self.mock_response_data = {
            "main": {
                "temp": 25.5,
                "humidity": 60
            },
            "weather": [
                {
                    "description": "clear sky"
                }
            ],
            "wind": {
                "speed": 5.5
            }
        }
    
    @patch('Extract.requests.get')
    def test_extract_success(self, mock_get):
        """Test successful extraction"""
        from Extract import extract
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response
        
        # Call the function
        result = extract(self.api_key, self.city)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['city'], self.city)
        self.assertEqual(result['temperature'], 25.5)
        self.assertEqual(result['humidity'], 60)
        self.assertEqual(result['weather'], 'clear sky')
        self.assertEqual(result['wind_speed'], 5.5)
        self.assertIsInstance(result['timestamp'], pd.Timestamp)
    
    @patch('Extract.requests.get')
    def test_extract_api_error(self, mock_get):
        """Test API error handling"""
        from Extract import extract
        
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        # Call the function
        result = extract(self.api_key, self.city)
        
        # Should return None on error
        self.assertIsNone(result)
    
    def test_extract_data_structure(self):
        """Test that extract returns the expected data structure"""
        from Extract import extract
        
        # This is more of an integration test, but we can check the structure
        expected_keys = ['city', 'temperature', 'humidity', 'weather', 'wind_speed', 'timestamp']
        
        # We'll mock this test since we don't want to make real API calls in unit tests
        with patch('Extract.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = self.mock_response_data
            mock_get.return_value = mock_response
            
            result = extract(self.api_key, self.city)
            
            # Check that all expected keys are present
            for key in expected_keys:
                self.assertIn(key, result)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)