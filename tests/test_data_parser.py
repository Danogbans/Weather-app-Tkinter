import unittest
from utils.data_parser import parse_weather_data



class TestDataParser(unittest.TestCase):

    def test_parse_weather_data_success(self):
        raw_data = {
            'main': {'temperature': 25, 'humidity': 50},
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'sys': {'country': 'ES'},
            'city_name': {'Madrid'}
        }
        expected_output = {
            'temperature': 25,
            'humidity': 50,
            'description': 'clear sky',
            'icon': '01d',
            'country': 'ES',
            'city_name': 'Madrid'
        }
        result = parse_weather_data(raw_data)

        self.assertEqual(result, expected_output)


    def test_parse_weather_data_key_error(self):
        raw_data = {
            'main': {'humidity': 50},
            'weather': [{'description': 'clear sky'}]
        }
        result = parse_weather_data(raw_data)
        self.assertIsNone(result)


    def test_parse_weather_data_type_error(self):
        raw_data = None
        result = parse_weather_data(raw_data)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()