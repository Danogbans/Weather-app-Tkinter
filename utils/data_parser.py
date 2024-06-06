def parse_weather_data(weather_data):
    """
    Parse the JSON response from the weather API and extract relevant data.
    
    Args:
        weather_data (dict): JSON response from the weather API.
    
    Returns:
        dict: Parsed weather data containing temperature, humidity, and description.
              Returns None if there is a parsing error.
    """

    try:
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        temperature = weather_data['main']['temp']
        country = weather_data['sys']['country']
        city_name = weather_data['name']
        icon = weather_data['weather'][0]['icon']

        
        parsed_data = {
            'description': description,
            'humidity': humidity,
            'temperature': temperature,
            'country': country,
            'city_name': city_name,
            'icon': icon
        }
        return parsed_data
    except (KeyError, TypeError) as e:
        print(f"Error parsing data: {e}")
        return None

