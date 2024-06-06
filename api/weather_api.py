import os
import requests




API_KEY = os.environ.get("WEATHER_API")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def obtain_weather_data(location):

    """Obtain weather data for a given location.
    
    Args:
        location (str): The location for which to fetch weather data.
    
    Returns:
        dict: Weather data if the request is successful, else None."""
    

    try:
        parameters = {
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=parameters)
        response.raise_for_status() # Raise HTTPError for bad response(4xx or 5 xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data:{e}")
        return None