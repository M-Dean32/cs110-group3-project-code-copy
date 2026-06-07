# Group 3 CS110 Project
# Adam's portion: Event Preparation Guide
#
# This program gives preparation tips for attending an event.
# It connects to the group's main ideas by using:
# - event category
# - weather condition
# - temperature
# - indoor/outdoor setting


def get_temperature():
    """Gets temperature from the user and makes sure it is a number."""
    while True:
        try:
            temperature = float(input("Enter the temperature in Fahrenheit: "))
            return temperature
        except ValueError:
            print("Please enter a valid number for the temperature.")


def get_event_category():
    """Lets the user choose an event category."""
    print("\nChoose an event category:")
    print("1. Cultural")
    print("2. Religious")
    print("3. Holiday")
    print("4. Awareness")
    print("5. Community")
    print("6. Other")

    categories = {
        "1": "Cultural",
        "2": "Religious",
        "3": "Holiday",
        "4": "Awareness",
        "5": "Community",
        "6": "Other"
    }

    choice = input("Enter your choice: ")

    while choice not in categories:
        print("Invalid choice. Please choose a number from 1 to 6.")
        choice = input("Enter your choice: ")

    return categories[choice]


def get_weather_condition():
    """Lets the user choose the weather condition."""
    print("\nChoose the weather condition:")
    print("1. Clear")
    print("2. Rainy")
    print("3. Cloudy")
    print("4. Snowy")
    print("5. Windy")
    print("6. Hot")

    weather_options = {
        "1": "Clear",
        "2": "Rainy",
        "3": "Cloudy",
        "4": "Snowy",
        "5": "Windy",
        "6": "Hot"
    }

    choice = input("Enter your choice: ")

    while choice not in weather_options:
        print("Invalid choice. Please choose a number from 1 to 6.")
        choice = input("Enter your choice: ")

    return weather_options[choice]


def get_event_location_type():
    """Checks if the event is indoors or outdoors."""
    print("\nIs the event indoors or outdoors?")
    print("1. Indoors")
    print("2. Outdoors")
    print("3. Not sure")

    location_options = {
        "1": "Indoors",
        "2": "Outdoors",
        "3": "Not sure"
    }

    choice = input("Enter your choice: ")

    while choice not in location_options:
        print("Invalid choice. Please choose 1, 2, or 3.")
        choice = input("Enter your choice: ")

    return location_options[choice]


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


def display_preparation_guide(category, weather, temperature, location_type, tips):
    """Displays the final preparation guide."""
    print("\n" + "=" * 50)
    print("EVENT PREPARATION GUIDE")
    print("=" * 50)

    print(f"Event Category: {category}")
    print(f"Weather: {weather}")
    print(f"Temperature: {temperature:.1f}°F")
    print(f"Event Setting: {location_type}")

    print("\nSuggested Preparation Tips:")
    for number, tip in enumerate(tips, start=1):
        print(f"{number}. {tip}")

    print("=" * 50)


def main():
    """Main program function."""
    print("Welcome to the Event Preparation Guide!")

    category = get_event_category()
    weather = get_weather_condition()
    temperature = get_temperature()
    location_type = get_event_location_type()

    tips = generate_preparation_tips(category, weather, temperature, location_type)
    display_preparation_guide(category, weather, temperature, location_type, tips)


main()
