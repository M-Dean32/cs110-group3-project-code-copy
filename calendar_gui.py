import calendar
import tkinter as tk

#Sets sunday as the starting day for the calendar
calendar.setfirstweekday(calendar.SUNDAY)

#Starts up the main window
main_w = tk.Tk()
main_w.title("Team 3's Event Calendar")
main_w.geometry("900x900")

#month list for the calendar
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

#holiday list in dictionary (X,Y) format. X=month Y=day
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
        (3, 19): 'End of Ramadan'    
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



# Color Palettes
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

#Month Color Palettes
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

#sets the current year
current_year = 2026

#makes the grid frame for calendar days
cal_frame = tk.Frame(main_w)
cal_frame.pack(pady=20)

#stores on and off toggle
check_tog = {}

#makes frame for the checkmark toggles
check_frame = tk.LabelFrame(main_w, text="Event Types", padx=5, pady=5)
check_frame.pack(pady=5)

def update_calendar(*args):
    #clears widget frames when changing months
    for widget in cal_frame.winfo_children():
        widget.destroy()

    #gets the selected month string and converts to index (1-12)
    month_name = click.get()
    month_index = months.index(month_name) + 1

    current_bg = month_colors.get(month_name, "SystemButtonFace")

    main_w.config(bg=current_bg)
    cal_frame.config(bg=current_bg)
    check_frame.config(bg=current_bg)

    #makes the day headers and sets them
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for col, day in enumerate(days):
        lbl = tk.Label(cal_frame, text=day, font=("Arial", 12, "bold"), bg=current_bg)
        lbl.grid(row=0, column=col, padx=10, pady=5)

    month_cal = calendar.monthcalendar(current_year, month_index)

    #gives the grid day buttons
    for row_idx, week in enumerate(month_cal):
        for col_idx, day_num in enumerate(week):
            if day_num != 0:
                button_text = str(day_num)
                button_fg = "black"
                button_bg = "SystemButtonFace"

                #checks the toggle, and gives it the color indicated in category_colors
                for cat, var in check_tog.items():
                    if var.get():
                        if (month_index, day_num) in holidays[cat]:
                            holiday_name = holidays[cat][(month_index, day_num)]
                            button_text = f"{day_num}\n{holiday_name}"

                            button_bg = category_colors[cat]["bg"]
                            button_fg = category_colors[cat]["fg"]

                #makes each day a button
                day_btn = tk.Button(cal_frame, text=button_text, fg=button_fg, bg=button_bg, width=15, height=4, relief="raised")
                day_btn.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

#sets up the toggleboxes taken from holidays
for category in holidays.keys():
    check_tog[category] = tk.BooleanVar(value=True)
    check = tk.Checkbutton(
        check_frame,
        text=category,
        variable=check_tog[category],
        command=update_calendar
    )
    check.pack(side="right", padx=5)

#configures the drop down menu for months
click = tk.StringVar()
click.set(months[0])
click.trace_add("write", update_calendar)

drop_m = tk.OptionMenu(main_w, click, *months)
drop_m.pack(pady=10)

#generates calendar
update_calendar()

#starts the window for the program
main_w.mainloop()

#makes the calender for the program
update_calendar()

#starts the window for the program
main_w.mainloop()
