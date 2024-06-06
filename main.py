import tkinter as tk
import requests
from io import BytesIO
from datetime import datetime
from tkinter import font
from PIL import Image, ImageTk
from api.weather_api import obtain_weather_data
from utils.data_parser import parse_weather_data
from utils.error_handler import handle_api_error, handle_parsing_error



#Colors
SEA_WHITE = "#FFF7FC"
FACEBOOK_BLUE = "#306EB8"
SAND_COLOR = "#DAB692"
SKY_BLUE = "#8CA6CD"
SKY_GREEN = "#5AA1A8"
HIGH_YELLOW = "#FFF455"



#A function that will fetch weather icon code
def fetch_weather_icon(icon_code):
    """
    Fetch and display the weather icon.
    
    Args:
        icon_code (str): The code of the weather icon.
    """
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)
    icon_image_label.config(image=photo)
    icon_image_label.image = photo  # Keep a reference to avoid garbage collection


#A functions that gets the current day and time and updates the time and day label in the GUI
def update_time():
    """
    Update the current day and time
    """
    now = datetime.now()
    current_time = now.strftime('%I:%M %p')
    current_day = now.strftime('%a, %b %d, %Y')
    day_label.config(text=current_day)
    time_label.config(text=current_time)
    root.after(1000, update_time) #Updates every second



#Weather app functions and error handling
def fetch_weather_data(location):
    """
    Fetch and display weather data for the given location.
    
    Args:
        location (str): The location for which to fetch weather data.
    """

    loading_label.config(text="Fetching data, please wait.....", bg=SKY_GREEN)
    root.update_idletasks()

    try:
        weather_data = obtain_weather_data(location)

        if weather_data:
            parsed_data = parse_weather_data(weather_data)

            if parsed_data:
                temperature = parsed_data['temperature']
                humidity = parsed_data['humidity']
                description = parsed_data['description']
                country = parsed_data['country']
                city_name = parsed_data['city_name']
                icon = parsed_data['icon']

                temperature_description_label.config(text=f"Temperature: {temperature} °C")
                temp_degree_label.config(text=f"{temperature}°C")

                humidity_description_label.config(text=f"Humidity: {humidity} %")
                humidity_percentage_label.config(text=f"{humidity}%")

                weather_description_label.config(text=f"Weather description: {description.capitalize()}")
                loading_label.config(text="Data fetched, see weather conditions below.")

                today_weather_label.config(text=f"Today's weather in {city_name},{country},")

                #Fetch and display the weather icon
                fetch_weather_icon(icon)
            else:
                raise ValueError("Parsing error")
        else:
            raise ValueError("API error")
    except requests.exceptions.RequestException as e:
        error_message = handle_api_error(e)
        loading_label.config(bg='red', text=error_message)
    except (KeyError, TypeError) as e:
        error_message = handle_parsing_error(e)
        loading_label.config(bg='red', text=error_message)
    except ValueError as e:
        loading_label.config(bg='red', text=str(e))



#Create a function to add placeholder
def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg="#FDE7C0", font=('Arial', 12))

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0,tk.END)
            entry.config(fg='#FDE7C0')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg='lightgrey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)



root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")


#Load background image
background_image_path = "images/weather-app-bg-image.png"
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)


#Create a label to hold the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


#Create a frame
frame = tk.Frame(root, bg=SKY_BLUE, bd=5, relief="sunken")
frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.65)


#Create the search location Entry
location_entry = tk.Entry(root, bg=SKY_GREEN, fg=SEA_WHITE, font=('Merriweather', 12))
location_entry.place(relx=0.5, rely=0.05, anchor="center", relwidth=0.7, relheight=0.05)
add_placeholder(location_entry, 'Enter location....')


#Create the search location button
location_button = tk.Button(root, text="Fetch", bg=FACEBOOK_BLUE, command=lambda: fetch_weather_data(location_entry.get()), fg=SEA_WHITE, font=('Merriweather', 14))
location_button.place(relx=0.85, rely=0.05, anchor="center", relwidth=0.15, relheight=0.05)


#Create the search location button
loading_label = tk.Label(root, text=" ", fg=SEA_WHITE, font=('Merriweather', 10))
loading_label.place(relx=0.5, rely=0.13, anchor="center", relwidth=0.64, relheight=0.04)


#Create the description labels

#Today's weather label
today_weather_font = font.Font(family="merriweather", size=16, weight="bold")
today_weather_label = tk.Label(frame, text=" ", bg=SKY_BLUE, fg=HIGH_YELLOW, font=(today_weather_font))
today_weather_label.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.9, relheight=0.09)


#Create day label
day_font = font.Font(family="merriweather", size=12, weight="bold")
day_label = tk.Label(frame, text=" ", bg=SKY_BLUE, fg=SEA_WHITE, font=(day_font))
day_label.place(relx=0.02, rely=0.22, anchor="w", relwidth=0.6, relheight=0.04)


#Create a label to hold the cloudy image
icon_image_label = tk.Label(frame)
icon_image_label.place(relx=0.15, rely=0.42, anchor="w", relwidth=0.28, relheight=0.28)


#Create time label
time_font = font.Font(family="merriweather", size=12, weight="bold")
time_label = tk.Label(frame, text=" ", bg=SKY_BLUE, fg=HIGH_YELLOW, font=(time_font))
time_label.place(relx=0.58, rely=0.22, anchor="w", relwidth=0.3, relheight=0.06)


#Create temperature label
temp_font = font.Font(family="merriweather", size=12, weight="bold")
temp_label = tk.Label(frame, text="Temp ", bg=SKY_BLUE, fg=SEA_WHITE, font=(temp_font))
temp_label.place(relx=0.59, rely=0.32, anchor="w", relwidth=0.3, relheight=0.06)


#Create temperature degrees label
temp_degree_font = font.Font(family="merriweather", size=14, weight="bold")
temp_degree_label = tk.Label(frame, text=" ", bg=SKY_BLUE, fg=HIGH_YELLOW, font=(temp_degree_font))
temp_degree_label.place(relx=0.59, rely=0.39, anchor="w", relwidth=0.3, relheight=0.06)


#Create humidity label
humidity_font = font.Font(family="merriweather", size=12, weight="bold")
humidity_label = tk.Label(frame, text="Humidity", bg=SKY_BLUE, fg=SEA_WHITE, font=(humidity_font))
humidity_label.place(relx=0.59, rely=0.46, anchor="w", relwidth=0.3, relheight=0.06)


#Create humidity percentage label
humidity_percentage_font = font.Font(family="merriweather", size=14, weight="bold")
humidity_percentage_label = tk.Label(frame, text=" ", bg=SKY_BLUE, fg=HIGH_YELLOW, font=(humidity_percentage_font))
humidity_percentage_label.place(relx=0.59, rely=0.53, anchor="w", relwidth=0.3, relheight=0.06)


#Create tickets

#Create weather description ticket
weather_description_font = font.Font(family="merriweather", size=12, weight="bold")
weather_description_label = tk.Label(frame, text=" ", bg=SKY_GREEN, fg=HIGH_YELLOW, font=(weather_description_font))
weather_description_label.place(relx=0.5, rely=0.67, anchor="center", relwidth=0.96, relheight=0.09)


#Create humidity ticket
humidity_description_font = font.Font(family="merriweather", size=12, weight="bold")
humidity_description_label = tk.Label(frame, text=" ", bg=SKY_GREEN, fg=HIGH_YELLOW, font=(humidity_description_font))
humidity_description_label.place(relx=0.5, rely=0.77, anchor="center", relwidth=0.96, relheight=0.09)


#Create temperature ticket
temperature_description_font = font.Font(family="merriweather", size=12, weight="bold")
temperature_description_label = tk.Label(frame, text=" ", bg=SKY_GREEN, fg=HIGH_YELLOW, font=(temperature_description_font))
temperature_description_label.place(relx=0.5, rely=0.87, anchor="center", relwidth=0.96, relheight=0.09)


#Create the Refresh button
refresh_button = tk.Button(root, text="Refresh", command=lambda: fetch_weather_data(location_entry.get()), bg=FACEBOOK_BLUE, fg=SEA_WHITE, font=('Merriweather', 14))
refresh_button.place(relx=0.5, rely=0.88, anchor="center", relwidth=0.3, relheight=0.07)


update_time() #Call the function


root.mainloop()