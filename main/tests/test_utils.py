import unittest
from unittest.mock import patch, MagicMock

from main.utils import get_coordinates, get_weather_value, get_weather_by_city, get_weather_data


class TestWeatherFunctions(unittest.TestCase):
    
    @patch('main.utils.requests.get')
    def test_get_coordinates(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.json.return_value = [{"lat": 1.23, "lon": 4.56}]
        mock_get.return_value = mock_response
        
        
        result = get_coordinates("London", "fake_api_key")
        
        
        self.assertEqual(result, (1.23, 4.56))

    @patch('main.utils.requests.get')
    def test_get_weather_value(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"example_weather_data": "example"}
        mock_get.return_value = mock_response
        
        
        result = get_weather_value((1.23, 4.56), "fake_api_key")
        
        
        self.assertEqual(result, {"example_weather_data": "example"})
    
    @patch('main.utils.get_coordinates')
    @patch('main.utils.get_weather_value')
    def test_get_weather_by_city(self, mock_get_weather_value, mock_get_coordinates):
        
        mock_get_coordinates.return_value = (1.23, 4.56)
        mock_get_weather_value.return_value = {"example_weather_data": "example"}
        
        
        result = get_weather_by_city("London")
        
        
        self.assertEqual(result, {"example_weather_data": "example"})
    
    def test_get_weather_data(self):
        
        weather_raw_data = {
            "dt": 1708041600,
            "name": "London",
            "main": {"temp": 20, "pressure": 1015},
            "weather": [{"description": "Cloudy", "icon": "04d"}],
        }
        
        
        result = get_weather_data(weather_raw_data)
        
        
        self.assertEqual(result["today"], "16-02-2024")
        self.assertEqual(result["city"], "London")
        self.assertEqual(result["temperature"], 20)
        self.assertEqual(result["pressure"], 1015)
        self.assertEqual(result["description"], "Cloudy")
        self.assertEqual(result["icon"], "04d")


if __name__ == '__main__':
    unittest.main()

