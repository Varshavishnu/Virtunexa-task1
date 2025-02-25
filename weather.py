import requests
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import logging
from io import BytesIO
from PIL import Image, ImageTk

# API Configuration
API_KEY = "6b654b601d8ed1ae225136ef5b72d096"  # Replace with a valid OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"

# Logging Configuration
logging.basicConfig(filename="weather.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Database Setup
def init_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(city, weather):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather (city, temperature, humidity, wind_speed) VALUES (?, ?, ?, ?)",
                   (city, weather["temperature"], weather["humidity"], weather["wind_speed"]))
    conn.commit()
    conn.close()

def log_weather(city, weather):
    logging.info(f"City: {city}, Temp: {weather['temperature']}°C, Humidity: {weather['humidity']}%, Wind: {weather['wind_speed']} m/s")

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)  # Debugging: Print the API response

        # Ensure required keys exist
        if "main" not in data or "weather" not in data:
            return None
        
        # Extract wind speed, defaulting to 0 if "wind" or "speed" is missing
        wind_speed = data.get("wind", {}).get("speed", 0)
        print("Wind Speed:", wind_speed)  # Debugging: Print the extracted wind speed
        
        weather = {
            "temperature": data["main"].get("temp", "N/A"),
            "humidity": data["main"].get("humidity", "N/A"),
            "wind_speed": wind_speed,  # Use the extracted wind speed
            "icon": data["weather"][0]["icon"]
        }
        return weather
    return None

def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    weather = get_weather(city)
    if weather:
        # Update the result string to include wind speed
        result.set(f"🌡 Temperature: {weather['temperature']}°C\n"
                   f"💧 Humidity: {weather['humidity']}%\n"
                   f"💨 Wind Speed: {weather['wind_speed']} m/s")
        
        save_to_db(city, weather)
        log_weather(city, weather)
        update_weather_icon(weather['icon'])
    else:
        messagebox.showerror("Error", f"City '{city}' not found!")

def update_weather_icon(icon_code):
    try:
        response = requests.get(ICON_URL.format(icon_code))
        if response.status_code == 200:
            image_data = Image.open(BytesIO(response.content))
            image_resized = image_data.resize((80, 80))
            weather_icon = ImageTk.PhotoImage(image_resized)
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon
    except Exception as e:
        print("Error loading weather icon:", e)

# Initialize Database
init_db()

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("450x400")
root.configure(bg="#2C3E50")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 14), background="#2C3E50", foreground="white")

frame = ttk.Frame(root, padding=20, relief="groove")
frame.pack(pady=20)

# Title Label
title_label = ttk.Label(frame, text="Weather App", font=("Arial", 16, "bold"))
title_label.pack()

# City Entry
tt = ttk.Label(frame, text="Enter City:")
tt.pack(pady=5)
city_entry = ttk.Entry(frame, font=("Arial", 12))
city_entry.pack(pady=5)

# Weather Icon
icon_label = ttk.Label(frame)
icon_label.pack(pady=5)

# Get Weather Button
get_weather_btn = ttk.Button(frame, text="Get Weather", command=show_weather)
get_weather_btn.pack(pady=10)

# Result Label
result = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result, font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()