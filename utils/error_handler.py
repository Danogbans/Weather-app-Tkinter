import requests


def handle_api_error(error):
    """
    Handle errors related to the API request.
    
    Args:
        error (Exception): The exception raised during the API request.
    
    Returns:
        str: A user-friendly error message.
    """
     
    if isinstance(error, requests.exceptions.HTTPError):
        return "HTTP error occurred. Please check the location and try again."
    elif isinstance(error, requests.exceptions.ConnectionError):
        return "Connection error occurred. Please, check your internet connection."
    elif isinstabce(error, requests.exceptions.Timeout):
        return "The request timed out. Please try again later."
    elif isinstance(error, requests.exceptions.RequestException):
        return "An error occurred while handling your request. Please try again later."
    else:
        return "An unexpected error occurred. Please try again."



def handle_parsing_error(error):
    """
    Handle errors related to parsing the JSON response.
    
    Args:
        error (Exception): The exception raised during JSON parsing.
    
    Returns:
        str: A user-friendly error message.
    """
    if isinstance(error, KeyError):
        return "Missing data in the response. Please try again later."
    elif isinstance(error, TypeError):
        return "Incorrect data format received. Please try again later."
    else:
        return "An error occurred while parsing the data. Please try again."