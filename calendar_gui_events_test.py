# This is Michael's portion for the GUI, with Adam's event-details test feature added

#Group 3's Project!
#Michael Dean's portion
#Adam's test addition: clickable event details

import calendar
import tkinter as tk

#Starts the main window
main_w = tk.Tk()
main_w.title("Team 3's Event Calendar!")
main_w.geometry("900x750")

#month list for the calendar
months = [ "January", "February", "March", "April", "May", "June",
 "July", "August", "September", "October", "November", "December",]

#sets the year
current_year = 2026

#Adam's test event data
#Format: (month number, day number): event information
events = {
    (1, 1): {
        "name": "New Year's Day",
        "category": "Holiday",
        "description": "A general holiday marking the start of the new year."
    },
    (1, 19): {
        "name": "Martin Luther King Jr. Day",
        "category": "Cultural / Historical",
        "description": "A U.S. holiday honoring Dr. Martin Luther King Jr. and his civil rights work."
    },
    (2, 17): {
        "name": "Lunar New Year",
        "category": "Cultural",
        "description": "A celebration of the start of the lunar calendar year in several Asian cultures."
    },
    (3, 8): {
        "name": "International Women's Day",
        "category": "Awareness",
        "description": "A day focused on recognizing women's achievements and discussing gender equality."
    },
    (6, 19): {
        "name": "Juneteenth",
        "category": "Cultural / Historical",
        "description": "A U.S. holiday recognizing the end of slavery in the United States."
    },
    (9, 16): {
        "name": "Mexican Independence Day",
        "category": "Cultural",
        "description": "A celebration of Mexico's independence from Spain."
    },
    (12, 25): {
        "name": "Christmas",
        "category": "Religious / Holiday",
        "description": "A Christian holiday that is also widely celebrated as a general holiday."
    }
}

#this makes the grid frame
cal_frame = tk.Frame(main_w)
cal_frame.pack(pady=20)

#Adam's event details section
details_label = tk.Label(main_w, text="Event Details", font=("Arial", 14, "bold"))
details_label.pack(pady=5)

details_box = tk.Text(main_w, height=7, width=85, wrap="word")
details_box.pack(pady=5)
details_box.insert(tk.END, "Click a date to see event details.")
details_box.config(state="disabled")

#Adam's function to update the event details box
def show_event_details(month_index, day_num):
    details_box.config(state="normal")
    details_box.delete("1.0", tk.END)

    month_name = months[month_index - 1]
    event_key = (month_index, day_num)

    if event_key in events:
        event = events[event_key]

        details_box.insert(tk.END, f"Date: {month_name} {day_num}, {current_year}\n")
        details_box.insert(tk.END, f"Event: {event['name']}\n")
        details_box.insert(tk.END, f"Category: {event['category']}\n")
        details_box.insert(tk.END, f"Description: {event['description']}")
    else:
        details_box.insert(tk.END, f"Date: {month_name} {day_num}, {current_year}\n\n")
        details_box.insert(tk.END, "No saved event for this date yet.")

    details_box.config(state="disabled")

#the def for the calendar logic
def update_calendar(*args):
    #clears out any previous month's grid widgets
    for widget in cal_frame.winfo_children():
        widget.destroy()

    #gets selected month string and convert to index (1-12)
    month_name = click.get()
    month_index = months.index(month_name) + 1

    #draws day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for col, day in enumerate(days):
        lbl = tk.Label(cal_frame, text=day, font=("Arial", 12, "bold"))
        lbl.grid(row=0, column=col, padx=10, pady=5)

    #fetch calculation matrix for the specific month
    month_cal = calendar.monthcalendar(current_year, month_index)

    #populates grid with day buttons or labels
    for row_idx, week in enumerate(month_cal):
        for col_idx, day_num in enumerate(week):
            if day_num != 0: #0 represents empty space padding the week

                #Adam's addition: marks dates that have saved events
                button_text = str(day_num)
                if (month_index, day_num) in events:
                    button_text += "\n★"

                #this creates the button for each day. Will make it do something later!
                #Adam's addition: command makes the button show event details
                day_btn = tk.Button(
                    cal_frame,
                    text=button_text,
                    width=6,
                    height=4,
                    relief="raised",
                    command=lambda m=month_index, d=day_num: show_event_details(m, d)
                )

                day_btn.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

#This makes the drop down menu for each month
click = tk.StringVar()
click.set(months[0])

#automatically refreshes calander whenever click variable changes in the app
click.trace_add("write", update_calendar)

#embeds optionmenu
drop_m = tk.OptionMenu(main_w, click, *months)
drop_m.pack(pady=10)

#makes the calender for the program
update_calendar()

#starts the window for the program
main_w.mainloop()
