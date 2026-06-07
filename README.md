# CS110 Group 3 Project Code Copy

This repository is a safe copy of our CS110 Group 3 project code. I made this version so we can organize the current code, test different parts, and avoid changing the main group project before everyone is ready to add things together.

Our project idea is an event calendar that helps users find events and prepare for them. The main parts of the project connect calendar events, weather information, and planning for different types of events.

## Project Files

### `calendar_gui.py`

This file has Michael's calendar GUI code. It uses `tkinter` and `calendar` to create the main event calendar window.

Right now, this file can:

* Open a calendar window
* Show the project title
* Create a month dropdown menu
* Display the days of the week
* Build day buttons for each month
* Refresh the calendar when the month is changed

This file is the base calendar layout for the project.

### `weather.py`

This file has Jimmy's weather code. It uses the OpenWeather API to get weather information for a city.

Right now, this file can:

* Ask the user to enter a city
* Send a request to OpenWeather
* Get the current temperature
* Show the temperature in Fahrenheit
* Convert the temperature to Celsius
* Show the weather condition

This file is still separate from the calendar GUI, but it connects to the main project because weather can help users plan for events.

### `event_prep_guide.py`

This file is my separate part of the project.

My feature is called the **Event Preparation Guide**. It does not directly change the calendar GUI or the weather code. Instead, it connects to the same overall idea by helping users prepare for an event based on the event type, weather, temperature, and whether the event is indoors or outdoors.

The program asks the user for:

* Event category
* Weather condition
* Temperature in Fahrenheit
* Indoor or outdoor event setting

After that, it prints a preparation guide with useful tips.

Example:

If the user chooses:

* Cultural event
* Rainy weather
* 48°F
* Outdoor setting

The program may suggest:

* Bringing an umbrella or rain jacket
* Wearing shoes that can handle wet ground
* Bringing a jacket or hoodie
* Learning about the culture or tradition before attending
* Checking the weather again before leaving

This feature fits with the main project because the calendar helps users find events, the weather code gives weather information, and the preparation guide helps users think about what they should bring or know before going.

## How to Run the Files

These are Python files, so they need to be run with Python.

### Run the event preparation guide

```bash
python3 event_prep_guide.py
```

### Run the calendar GUI

```bash
python3 calendar_gui.py
```

### Run the weather code

```bash
python3 weather.py
```

## Notes About the Weather API

The weather file uses an API key. For safety, the API key should not be posted publicly. In this copy, the API key should either be replaced with a placeholder or kept private.

Example:

```python
API_KEY = "PASTE_API_KEY_HERE"
```

## Adam's Contribution

My contribution is the `event_prep_guide.py` file.

I wanted my part to connect to the group project without taking over or rewriting what my teammates already made. Michael's part focuses on the calendar GUI, and Jimmy's part focuses on the weather. My part adds a separate helper feature that uses those same ideas in a different way.

The Event Preparation Guide helps users figure out what they might need before attending an event. It gives suggestions based on the event category, weather, temperature, and event setting.

This adds to the overall project because the app is not only about finding events. It can also help users prepare for the events they want to attend.

## Future Improvements

Some future improvements could include:

* Connecting the preparation guide to the calendar GUI
* Using live weather data from the weather file instead of manual weather input
* Adding more event categories
* Adding more specific preparation tips
* Making the preparation guide appear inside the main app window
* Letting users save or copy the preparation tips

## Current Purpose of This Repository

This repository is mainly for safe testing and organization. It helps keep the current group code separate from new feature testing, so changes can be reviewed before being added to the main project.
