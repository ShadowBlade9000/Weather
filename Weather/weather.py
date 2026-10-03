import os
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageDraw

def generate_weather_icon(condition="clear_day"):
    """Generate a 64x64 PNG icon matching the current weather condition."""
    filename = f"icon_{condition}.png"
    if os.path.exists(filename):
        return filename

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if condition == "clear_night":
        # Crescent Moon
        draw.ellipse([14, 10, 50, 46], fill="#f1c40f")
        draw.ellipse([22, 6, 54, 38], fill=(0, 0, 0, 0))
        # Stars
        draw.ellipse([10, 10, 14, 14], fill="#f39c12")
        draw.ellipse([48, 12, 51, 15], fill="#f39c12")
        draw.ellipse([44, 46, 48, 50], fill="#f39c12")

    elif condition == "rain":
        # Dark Cloud
        draw.ellipse([8, 20, 30, 42], fill="#7f8c8d")
        draw.ellipse([20, 12, 48, 40], fill="#7f8c8d")
        draw.ellipse([34, 20, 56, 42], fill="#7f8c8d")
        draw.rectangle([18, 28, 46, 42], fill="#7f8c8d")
        # Rain Drops
        draw.line([20, 46, 16, 56], fill="#3498db", width=3)
        draw.line([32, 46, 28, 56], fill="#3498db", width=3)
        draw.line([44, 46, 40, 56], fill="#3498db", width=3)

    elif condition == "snow":
        # Light Cloud
        draw.ellipse([8, 18, 30, 40], fill="#bdc3c7")
        draw.ellipse([20, 10, 48, 38], fill="#bdc3c7")
        draw.ellipse([34, 18, 56, 40], fill="#bdc3c7")
        draw.rectangle([18, 26, 46, 40], fill="#bdc3c7")
        # Snowflakes
        draw.ellipse([18, 46, 24, 52], fill="#ecf0f1")
        draw.ellipse([30, 48, 36, 54], fill="#ecf0f1")
        draw.ellipse([42, 46, 48, 52], fill="#ecf0f1")

    elif condition == "clouds":
        # Grey Cloud
        draw.ellipse([8, 22, 30, 44], fill="#95a5a6")
        draw.ellipse([20, 14, 48, 42], fill="#95a5a6")
        draw.ellipse([34, 22, 56, 44], fill="#95a5a6")
        draw.rectangle([18, 30, 46, 44], fill="#95a5a6")

    else:  # clear_day
        # Yellow Sun
        draw.ellipse([16, 16, 48, 48], fill="#f1c40f")
        # Sun Rays
        draw.line([32, 4, 32, 12], fill="#f39c12", width=3)
        draw.line([32, 52, 32, 60], fill="#f39c12", width=3)
        draw.line([4, 32, 12, 32], fill="#f39c12", width=3)
        draw.line([52, 32, 60, 32], fill="#f39c12", width=3)
        draw.line([12, 12, 18, 18], fill="#f39c12", width=3)
        draw.line([46, 46, 52, 52], fill="#f39c12", width=3)
        draw.line([52, 12, 46, 18], fill="#f39c12", width=3)
        draw.line([18, 46, 12, 52], fill="#f39c12", width=3)

    img.save(filename, "PNG")
    return filename

def parse_weather_condition(code, is_day):
    """Map WMO Weather Interpretation Codes to condition categories."""
    if code in [0, 1]:  # Clear / Mainly Clear
        return "clear_day" if is_day == 1 else "clear_night"
    elif code in [2, 3, 45, 48]:  # Cloudy / Fog
        return "clouds"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:  # Rain / Drizzle / Thunderstorm
        return "rain"
    elif code in [71, 73, 75, 77, 85, 86]:  # Snow
        return "snow"
    return "clear_day" if is_day == 1 else "clear_night"

def set_window_icon(condition_name):
    """Update window icon dynamically."""
    try:
        icon_path = generate_weather_icon(condition_name)
        app_icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(False, app_icon)
        # Prevent garbage collection of image
        root.app_icon = app_icon
    except Exception:
        pass

def get_coordinates(city_name):
    """Fetch latitude and longitude for a given city name."""
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    try:
        response = requests.get(geocoding_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "name": result["name"],
                "country": result.get("country", ""),
                "lat": result["latitude"],
                "lon": result["longitude"]
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")
        return None

def fetch_weather(event=None):
    """Fetch weather data and update icon dynamically."""
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    search_btn.config(state=tk.DISABLED, text="Loading...")
    root.update()

    location = get_coordinates(city)
    
    if location is None:
        messagebox.showerror("Error", f"City '{city}' not found.")
        search_btn.config(state=tk.NORMAL, text="Get Weather")
        return

    # Fetch weather data including condition code and day/night state
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={location['lat']}&longitude={location['lon']}"
        f"&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph"
    )

    try:
        response = requests.get(weather_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        current = data.get("current_weather", {})

        temp = current.get("temperature", "N/A")
        wind = current.get("windspeed", "N/A")
        code = current.get("weathercode", 0)
        is_day = current.get("is_day", 1)
        
        # Determine condition and update window icon dynamically
        condition = parse_weather_condition(code, is_day)
        set_window_icon(condition)

        # Display weather info
        location_label.config(text=f"{location['name']}, {location['country']}")
        temp_label.config(text=f"{temp} °F")
        wind_label.config(text=f"Wind Speed: {wind} mph")
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not retrieve weather data: {e}")
    finally:
        search_btn.config(state=tk.NORMAL, text="Get Weather")

# --- UI Setup ---
root = tk.Tk()
root.title("Weather")
root.geometry("350x400")
root.resizable(False, False)
root.configure(bg="#f0f4f8")

# Default window icon on startup
set_window_icon("clear_day")

# Title Header
header = tk.Label(root, text="🌤 Weather Search", font=("Helvetica", 18, "bold"), bg="#f0f4f8", fg="#2c3e50")
header.pack(pady=20)

# Input Field
city_entry = tk.Entry(root, font=("Helvetica", 14), width=20, justify="center", bd=2, relief="groove")
city_entry.pack(pady=10)

# Bind Enter key
city_entry.bind("<Return>", fetch_weather)

# Search Button
search_btn = tk.Button(
    root, text="Get Weather", font=("Helvetica", 12, "bold"), 
    bg="#3498db", fg="white", activebackground="#2980b9", 
    relief="flat", cursor="hand2", command=fetch_weather
)
search_btn.pack(pady=10)

# Weather Results Frame
result_frame = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
result_frame.pack(pady=20, fill="both", expand=True, padx=20)

location_label = tk.Label(result_frame, text="Enter a city above", font=("Helvetica", 12), bg="#ffffff", fg="#7f8c8d")
location_label.pack(pady=(20, 5))

temp_label = tk.Label(result_frame, text="-- °F", font=("Helvetica", 28, "bold"), bg="#ffffff", fg="#e74c3c")
temp_label.pack(pady=5)

wind_label = tk.Label(result_frame, text="Wind Speed: -- mph", font=("Helvetica", 11), bg="#ffffff", fg="#7f8c8d")
wind_label.pack(pady=(5, 15))

root.mainloop()