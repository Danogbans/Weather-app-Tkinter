import unittest
import requests
from unittest.mock import patch
from api.weather_api import obtain_weather_data


class TestWeatherApi(unittest.TestCase):

    @patch('api.weather_api.requests.get')
    def obtain_weather_data_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        expected_data = {
            'main': {'temp': 25, 'humidity': 50},
            'weather': [{'description': 'clear sky'}]
        }
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        location = "New York"
        result = obtain_weather_data(location)
        self.assertIsNotNone(result)
        self.assertEqual(result['main']['temp'], 25)
        self.assertEqual(result['main']['humidity'], 50)
        self.assertEqual(result['weather'][0]['description'], 'clear sky')


    #Testing errors
    @patch('api.weather_api.requests.get')
    def test_obtain_weather_data_http_error(self, mock_get):
        mock_get.side_effect = unittest.mock.Mock(side_effect=requests.exceptions.HTTPError)

        location = "New York"
        result = obtain_weather_data(location)
        self.assertIsNone(result)

    
    @patch('api.weather_api.requests.get')
    def test_obtain_weather_data_connection_error(self, mock_get):
        mock_get.side_effect = unittest.mock.Mock(side_effect=requests.exceptions.ConnectionError)

        location = "New York"
        result = obtain_weather_data(location)
        self.assertIsNone(result)


    @patch('api.weather_api.requests.get')
    def test_obtain_weather_data_timeout_error(self, mock_get):
        mock_get.side_effect = unittest.mock.Mock(side_effect=requests.exceptions.Timeout)

        location = "New York"
        result = obtain_weather_data(location)
        self.assertIsNone(result)


    @patch('api.weather_api.requests.get')
    def test_obtain_weather_data_request_exception(self, mock_get):
        mock_get.side_effect = unittest.mock.Mock(side_effect=requests.exceptions.RequestException)

        location = "New York"
        result = obtain_weather_data(location)
        self.assertIsNone(result) 


if __name__ == '__main__':
    unittest.main()      