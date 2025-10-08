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
    
    @patch('ETL.Extract.requests.get')
    def test_extract_success(self, mock_get):
        """Test successful extraction"""
        from ETL.Extract import extract
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response
        
        # Call the function
        result = extract(self.api_key, self.city)
        
        # Assertions - result is now a DataFrame
        self.assertIsNotNone(result)
        self.assertFalse(result.empty)  # DataFrame should not be empty
        self.assertEqual(len(result), 1)  # Should have one row
        self.assertEqual(result.iloc[0]['city'], self.city)
        self.assertEqual(result.iloc[0]['temperature'], 25.5)
        self.assertEqual(result.iloc[0]['humidity'], 60)
        self.assertEqual(result.iloc[0]['weather'], 'clear sky')
        self.assertEqual(result.iloc[0]['wind_speed'], 5.5)
        self.assertIsInstance(result.iloc[0]['timestamp'], pd.Timestamp)
    
    @patch('ETL.Extract.requests.get')
    def test_extract_api_error(self, mock_get):
        """Test API error handling"""
        from ETL.Extract import extract
        import requests
        
        # Mock API error - use proper requests exception
        mock_get.side_effect = requests.RequestException("API Error")
        
        # Call the function
        result = extract(self.api_key, self.city)
        
        # Should return empty DataFrame on error
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
    
    def test_extract_data_structure(self):
        """Test that extract returns the expected data structure"""
        from ETL.Extract import extract
        
        # This is more of an integration test, but we can check the structure
        expected_columns = ['city', 'temperature', 'humidity', 'weather', 'wind_speed', 'timestamp']
        
        # We'll mock this test since we don't want to make real API calls in unit tests
        with patch('ETL.Extract.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = self.mock_response_data
            mock_get.return_value = mock_response
            
            result = extract(self.api_key, self.city)
            
            # Check that result is a DataFrame with expected columns
            self.assertIsInstance(result, pd.DataFrame)
            self.assertFalse(result.empty)
            for column in expected_columns:
                self.assertIn(column, result.columns)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)