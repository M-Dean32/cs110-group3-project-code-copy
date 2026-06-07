# Weather App project CS110 Spring 2026

import requests

API_KEY = "PASTE_API_KEY_HERE"

if not API_KEY:
    raise ValueError("Missing OpenWeather API key")

city = input("Enter a city: ")

url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}"
    f"&appid={API_KEY}"
    "&units=imperial"
)

response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print("Error:", data.get("message", "Could not get weather"))
else:
    temp_f = data["main"]["temp"]
    temp_c = (temp_f - 32) * 5 / 9

    print(f"Weather in {city}:")
    print(f"Temperature: {temp_f:.1f}°F")
    print(f"Temperature: {temp_c:.1f}°C")
    print(f"Condition: {data['weather'][0]['description']}")
