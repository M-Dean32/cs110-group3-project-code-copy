# Group 3 CS110 Project - Spring 2026
# Combined program: Event Calendar + Event Preparation Guide + Weather
#
# Michael Dean ... Calendar GUI (months, holidays, color coding, toggles)
# Adam ........... Event Preparation Guide
# Jimmy Weather App .... Live weather lookup (OpenWeather)
#
# How it all fits together:
#   - The calendar is the main display. Pick a month, toggle which event types
#     to highlight, and the matching holidays show up colored on their day.
#   - Click any day to slide out a narrow prep panel on the left (Apple-style).
#   - In that panel you can look up live weather for a city (which auto-fills
#     the real temperature and condition), or enter them by hand.
#   - The program then generates preparation tips based on the event category,
#     weather, temperature, and indoor/outdoor setting.

import calendar
import tkinter as tk
from tkinter import messagebox, ttk

# requests is only needed for the live weather lookup. If it isn't installed,
# the program still runs and the user can enter the weather manually.
try:
    import requests
except ImportError:
    requests = None

# Paste your OpenWeather API key here to enable live weather lookups.
# Replace ONLY the part inside the quotes on the API_KEY line below.
API_KEY = "bef66e7d82c2e83f05b81b83e68dc283"
PLACEHOLDER_KEY = "PASTE_API_KEY_HERE"


# ---------------------------------------------------------------------------
# Weather lookup (from weather.py)
# ---------------------------------------------------------------------------

# OpenWeather "main" conditions mapped to the categories the prep guide uses.
WEATHER_MAP = {
    "Clear": "Clear",
    "Rain": "Rainy",
    "Drizzle": "Rainy",
    "Thunderstorm": "Rainy",
    "Clouds": "Cloudy",
    "Snow": "Snowy",
    "Mist": "Cloudy",
    "Fog": "Cloudy",
    "Haze": "Cloudy",
}


def get_weather(city):
    """Looks up live weather for a city.

    Returns a (temperature_f, condition) tuple on success, or raises a
    RuntimeError with a friendly message if something goes wrong.
    """
    if requests is None:
        raise RuntimeError(
            "The 'requests' library is not installed, so live weather is "
            "unavailable.\nInstall it with:  pip install requests\n"
            "For now, enter the weather and temperature by hand."
        )

    if not API_KEY or API_KEY == PLACEHOLDER_KEY:
        raise RuntimeError(
            "No OpenWeather API key set.\nPaste your key into the API_KEY "
            "line near the top of the program, or enter the weather by hand."
        )

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        "&units=imperial"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise RuntimeError(data.get("message", "Could not get weather"))

    temp_f = data["main"]["temp"]
    main_condition = data["weather"][0]["main"]
    # Translate OpenWeather's condition into one of our guide categories.
    condition = WEATHER_MAP.get(main_condition, "Clear")

    # Treat very warm clear/cloud days as "Hot" so the heat tips show up.
    if temp_f >= 85 and condition in ("Clear", "Cloudy"):
        condition = "Hot"

    return temp_f, condition


# ---------------------------------------------------------------------------
# Preparation tips (from event_prep_guide.py)
# ---------------------------------------------------------------------------

def generate_preparation_tips(category, weather, temperature, location_type):
    """Creates a list of preparation tips based on the user's answers."""
    tips = []

    # General event tips
    tips.append("Check the event time, location, and any posted rules before going.")
    tips.append("Bring your phone fully charged in case you need directions or updates.")

    # Category-based tips
    if category == "Cultural":
        tips.append("Take time to learn a little about the culture or tradition before attending.")
        tips.append("Be respectful of customs, clothing expectations, food, music, or ceremonies.")

    elif category == "Religious":
        tips.append("Be respectful of religious customs, quiet spaces, and dress expectations.")
        tips.append("Check if there are any rules about photography, food, or participation.")

    elif category == "Holiday":
        tips.append("Expect larger crowds and plan extra time for parking or transportation.")
        tips.append("Check if the event has special activities, food, or scheduled performances.")

    elif category == "Awareness":
        tips.append("Read the purpose of the event so you understand what cause is being supported.")
        tips.append("Consider bringing questions or being ready to learn from speakers or displays.")

    elif category == "Community":
        tips.append("Look for chances to meet people, volunteer, or support local groups.")
        tips.append("Bring any needed items if the event includes donations, sign-ups, or activities.")

    else:
        tips.append("Look up the event details ahead of time so you know what to expect.")

    # Weather-based tips
    if weather == "Rainy":
        tips.append("Bring an umbrella or rain jacket.")
        tips.append("Wear shoes that can handle wet ground.")

    elif weather == "Snowy":
        tips.append("Wear warm layers and shoes with good grip.")
        tips.append("Give yourself extra travel time because roads and sidewalks may be slippery.")

    elif weather == "Windy":
        tips.append("Wear a jacket or hoodie that blocks wind.")
        tips.append("Avoid bringing loose papers or items that could blow away.")

    elif weather == "Hot":
        tips.append("Bring water and try to stay in shaded areas when possible.")
        tips.append("Wear lighter clothing if the event setting allows it.")

    elif weather == "Cloudy":
        tips.append("Bring a light jacket just in case the temperature drops.")

    elif weather == "Clear":
        tips.append("Check if sunglasses, sunscreen, or water would be useful.")

    # Temperature-based tips
    if temperature <= 40:
        tips.append("Dress warmly because the temperature is very cold.")
        tips.append("Consider gloves, a hat, or extra layers.")

    elif temperature <= 55:
        tips.append("Bring a jacket or hoodie because it may feel chilly.")

    elif temperature >= 85:
        tips.append("Prepare for heat by bringing water and avoiding too much direct sun.")

    elif temperature >= 70:
        tips.append("The temperature should be comfortable, but water is still a good idea.")

    # Indoor/outdoor tips
    if location_type == "Outdoors":
        tips.append("Since the event is outdoors, check the weather again before leaving.")
        tips.append("Plan for walking, standing, or sitting outside.")

    elif location_type == "Indoors":
        tips.append("Since the event is indoors, check if there are building rules or entry requirements.")

    else:
        tips.append("Since the event location type is unclear, prepare for both indoor and outdoor conditions.")

    return tips


# ---------------------------------------------------------------------------
# Calendar data (from the updated calendar_gui.py)
# ---------------------------------------------------------------------------

# Sunday is the first day of the week on this calendar.
calendar.setfirstweekday(calendar.SUNDAY)

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Holiday list in (month, day) format -> name, grouped by event type.
holidays = {
    "Japanese": {
        (7, 20): "Marine Day"
    },
    "Chinese": {
        (2, 17): "Chinese New Year"
    },
    "Christian": {
        (6, 24): "Nativity of St John",
        (7, 24): "Pioneer Day"
    },
    "USA Holidays": {
        (7, 4): "Fourth of July"
    },
    "Islam": {
        (2, 18): "Start of Ramadan",
        (3, 19): "End of Ramadan"
    },
    "LGBT": {
        (3, 31): "Trans Day of Visibility",
        (6, 1): "Start of Pride Month"
    },
    "African American": {
        (2, 1): "Black History Month",
        (1, 19): "MLK JR Day",
        (6, 19): "Juneteenth"
    },
    "Hispanic": {
        (11, 1): "Día de los Muertos",
        (9, 15): "Hispanic Heratige Month"
    }
}

# Color palettes for highlighted holiday days.
category_colors = {
    "Japanese": {"bg": "lightpink", "fg": "darkred"},
    "Chinese": {"bg": "deep pink", "fg": "mint cream"},
    "Christian": {"bg": "yellow", "fg": "purple"},
    "USA Holidays": {"bg": "lightblue", "fg": "darkblue"},
    "Islam": {"bg": "dark orange", "fg": "seashell3"},
    "LGBT": {"bg": "orchid1", "fg": "royalblue1"},
    "African American": {"bg": "OrangeRed4", "fg": "navajo white"},
    "Hispanic": {"bg": "coral", "fg": "peach puff"}
}

# Per-month background colors.
month_colors = {
    "January": "#8E8E8E",    # Grey
    "February": "#BE132D",   # Chinese New Year Red
    "March": "#B5C7EB",      # Marchy Blue
    "April": "#55C233",      # Grassy Green
    "May": "#50C878",        # Emerald
    "June": "#C2E4FA",       # Summer Blue
    "July": "#00B2DA",       # Ocean Blue
    "August": "#5d8ac0",     # Grey Blue
    "September": "#ce796b",  # Brown Red for Fall
    "October": "#ED820E",    # Orange for Halloween
    "November": "#EFBF04",   # Gold/Earth Color for Thanksgiving
    "December": "#8ABB6D"    # Green for Christmas
}

current_year = 2026

# Options used by the event preparation panel.
CATEGORIES = ["Cultural", "Religious", "Holiday", "Awareness", "Community", "Other"]
WEATHER_OPTIONS = ["Clear", "Rainy", "Cloudy", "Snowy", "Windy", "Hot"]
LOCATION_OPTIONS = ["Indoors", "Outdoors", "Not sure"]


# ---------------------------------------------------------------------------
# Main window layout: prep panel (left, hidden) + calendar (main display)
# ---------------------------------------------------------------------------

main_w = tk.Tk()
main_w.title("Team 3's Event Calendar")
main_w.geometry("1300x900")

# Holds the pop-in prep panel (left) and the calendar area (main).
content = tk.Frame(main_w)
content.pack(fill="both", expand=True)

# The prep panel is built now but NOT shown yet. It only slides out on the left
# (next to the calendar) once the user clicks a day -- similar to how the Apple
# Calendar app shows a narrow detail panel. The fixed width keeps it slim.
panel_frame = tk.LabelFrame(content, text="Event Preparation Guide",
                            font=("Arial", 12, "bold"), padx=10, pady=10,
                            width=320)
panel_frame.pack_propagate(False)

# The calendar area stays the main focus and fills the rest of the window.
cal_area = tk.Frame(content)
cal_area.pack(side="right", fill="both", expand=True)


# ---------------------------------------------------------------------------
# Event preparation panel (narrow side widget, Apple-style)
# ---------------------------------------------------------------------------

# The date currently selected on the calendar (updated when a day is clicked).
selected_date = tk.StringVar(value="No day selected yet")
holiday_note = tk.StringVar(value="")


def hide_panel():
    """Closes the side panel so the calendar is the only thing shown."""
    panel_frame.pack_forget()


# Top row of the panel: the selected date plus a button to close the panel.
header_row = tk.Frame(panel_frame)
header_row.pack(fill="x", pady=(0, 2))

tk.Label(header_row, textvariable=selected_date,
         font=("Arial", 12, "bold")).pack(side="left", anchor="w")
tk.Button(header_row, text="✕", font=("Arial", 10, "bold"),
          relief="flat", command=hide_panel).pack(side="right")

# Shows the holiday name(s) on the selected day, if any are toggled on.
tk.Label(panel_frame, textvariable=holiday_note, font=("Arial", 10, "italic"),
         fg="darkred", wraplength=290, justify="left").pack(anchor="w", pady=(0, 8))

form = tk.Frame(panel_frame)
form.pack(fill="x")

# Each label sits on its own line above its field so everything fits the
# narrow panel (Apple-style stacked layout). Fields fill the column width.

# --- Event category ---
tk.Label(form, text="Event category", font=("Arial", 10, "bold")).pack(anchor="w")
category_var = tk.StringVar(value=CATEGORIES[0])
ttk.Combobox(form, textvariable=category_var, values=CATEGORIES,
             state="readonly").pack(fill="x", pady=(0, 8))

# --- Indoor / outdoor ---
tk.Label(form, text="Indoors or outdoors", font=("Arial", 10, "bold")).pack(anchor="w")
location_var = tk.StringVar(value=LOCATION_OPTIONS[0])
ttk.Combobox(form, textvariable=location_var, values=LOCATION_OPTIONS,
             state="readonly").pack(fill="x", pady=(0, 8))

# --- Weather condition ---
tk.Label(form, text="Weather condition", font=("Arial", 10, "bold")).pack(anchor="w")
weather_var = tk.StringVar(value=WEATHER_OPTIONS[0])
ttk.Combobox(form, textvariable=weather_var, values=WEATHER_OPTIONS,
             state="readonly").pack(fill="x", pady=(0, 8))

# --- Temperature ---
# Starts blank; it gets filled in automatically after a city weather lookup,
# but can also be typed in by hand.
tk.Label(form, text="Temperature (°F)", font=("Arial", 10, "bold")).pack(anchor="w")
temp_var = tk.StringVar(value="")
tk.Entry(form, textvariable=temp_var).pack(fill="x", pady=(0, 4))

# --- Live weather lookup ---
lookup_frame = tk.LabelFrame(panel_frame, text="Look up live weather (optional)", font=("Arial", 10))
lookup_frame.pack(pady=10, fill="x")

tk.Label(lookup_frame, text="City").pack(anchor="w", padx=8, pady=(6, 0))
city_var = tk.StringVar()
tk.Entry(lookup_frame, textvariable=city_var).pack(fill="x", padx=8, pady=4)


def fetch_weather():
    city = city_var.get().strip()
    if not city:
        messagebox.showinfo("Enter a city", "Please type a city name first.")
        return
    try:
        temp_f, condition = get_weather(city)
    except RuntimeError as error:
        messagebox.showerror("Weather lookup failed", str(error))
        return
    # Auto-fill the form with the looked-up values.
    temp_var.set(f"{temp_f:.1f}")
    weather_var.set(condition)
    messagebox.showinfo("Weather found", f"{city}: {temp_f:.1f}°F, {condition}")


tk.Button(lookup_frame, text="Get Weather", command=fetch_weather).pack(
    padx=8, pady=(2, 8))

# --- Results area ---
result_box = tk.Text(panel_frame, height=12, width=30, wrap="word", font=("Arial", 10))
result_box.pack(pady=10, fill="both", expand=True)


def show_tips():
    # A day must be picked before we can prep for it.
    date_text = selected_date.get()
    if date_text == "No day selected yet":
        messagebox.showinfo("Pick a day", "Click a day on the calendar first.")
        return

    # Validate the temperature before generating tips.
    try:
        temperature = float(temp_var.get())
    except ValueError:
        messagebox.showerror("Invalid temperature",
                             "Please enter a valid number for the temperature.")
        return

    category = category_var.get()
    weather = weather_var.get()
    location_type = location_var.get()
    tips = generate_preparation_tips(category, weather, temperature, location_type)

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, "=" * 50 + "\n")
    result_box.insert(tk.END, "EVENT PREPARATION GUIDE\n")
    result_box.insert(tk.END, "=" * 50 + "\n")
    result_box.insert(tk.END, f"Date: {date_text}\n")
    result_box.insert(tk.END, f"Event Category: {category}\n")
    result_box.insert(tk.END, f"Weather: {weather}\n")
    result_box.insert(tk.END, f"Temperature: {temperature:.1f}°F\n")
    result_box.insert(tk.END, f"Event Setting: {location_type}\n\n")
    result_box.insert(tk.END, "Suggested Preparation Tips:\n")
    for number, tip in enumerate(tips, start=1):
        result_box.insert(tk.END, f"{number}. {tip}\n")
    result_box.insert(tk.END, "=" * 50 + "\n")


tk.Button(panel_frame, text="Generate Preparation Tips", font=("Arial", 11, "bold"),
          command=show_tips).pack(pady=(0, 5))


def select_day(date_text, holiday_text=""):
    """Called when a calendar day is clicked: reveals and fills the side panel."""
    selected_date.set(date_text)
    holiday_note.set(holiday_text)
    # Clear any tips from the previously selected day.
    result_box.delete("1.0", tk.END)
    # Slide the panel out on the left (before the calendar) if it's hidden.
    if not panel_frame.winfo_ismapped():
        panel_frame.pack(side="left", fill="y", padx=(0, 10), before=cal_area)


# ---------------------------------------------------------------------------
# Calendar GUI (from the updated calendar_gui.py)
# ---------------------------------------------------------------------------

# Month dropdown sits at the top of the calendar area.
click = tk.StringVar()
click.set(months[0])

drop_m = tk.OptionMenu(cal_area, click, *months)
drop_m.pack(pady=10)

# Grid frame for the calendar days.
cal_frame = tk.Frame(cal_area)
cal_frame.pack(pady=20)

# On/off toggles for each event type.
check_tog = {}

# Frame holding the event-type toggle checkboxes.
check_frame = tk.LabelFrame(cal_area, text="Event Types", padx=5, pady=5)
check_frame.pack(pady=5)


def update_calendar(*args):
    # Clear widget frames when changing months.
    for widget in cal_frame.winfo_children():
        widget.destroy()

    # Get the selected month string and convert to index (1-12).
    month_name = click.get()
    month_index = months.index(month_name) + 1

    # Recolor the calendar area to match the month.
    current_bg = month_colors.get(month_name, "SystemButtonFace")
    main_w.config(bg=current_bg)
    content.config(bg=current_bg)
    cal_area.config(bg=current_bg)
    cal_frame.config(bg=current_bg)
    check_frame.config(bg=current_bg)

    # Make the day headers.
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for col, day in enumerate(days):
        lbl = tk.Label(cal_frame, text=day, font=("Arial", 12, "bold"), bg=current_bg)
        lbl.grid(row=0, column=col, padx=10, pady=5)

    month_cal = calendar.monthcalendar(current_year, month_index)

    # Build the grid of day buttons.
    for row_idx, week in enumerate(month_cal):
        for col_idx, day_num in enumerate(week):
            if day_num != 0:
                button_text = str(day_num)
                button_fg = "black"
                button_bg = "SystemButtonFace"

                # Collect holiday names for this day from the toggled-on types,
                # and color the button using the matching category palette.
                day_holidays = []
                for cat, var in check_tog.items():
                    if var.get() and (month_index, day_num) in holidays[cat]:
                        holiday_name = holidays[cat][(month_index, day_num)]
                        day_holidays.append(holiday_name)
                        button_text = f"{day_num}\n{holiday_name}"
                        button_bg = category_colors[cat]["bg"]
                        button_fg = category_colors[cat]["fg"]

                date_text = f"{month_name} {day_num}, {current_year}"
                holiday_text = ", ".join(day_holidays)

                # Clicking a day opens the prep panel for that date.
                day_btn = tk.Button(
                    cal_frame, text=button_text, fg=button_fg, bg=button_bg,
                    width=15, height=4, relief="raised",
                    command=lambda d=date_text, h=holiday_text: select_day(d, h))
                day_btn.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)


# Set up the toggle checkboxes from the holiday categories.
for category in holidays.keys():
    check_tog[category] = tk.BooleanVar(value=True)
    check = tk.Checkbutton(
        check_frame,
        text=category,
        variable=check_tog[category],
        command=update_calendar
    )
    check.pack(side="right", padx=5)

# Refresh the calendar automatically whenever the month changes.
click.trace_add("write", update_calendar)

# Build the initial calendar and start the program.
update_calendar()
main_w.mainloop()
