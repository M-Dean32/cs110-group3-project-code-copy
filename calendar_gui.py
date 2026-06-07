# This is Michael's portion for the GUI, I'm trying to work on the presentation side of things and help with the GUI as

#Group 3's Project!
#Michael Dean's portion

import calendar
import tkinter as tk

#Starts the main window
main_w = tk.Tk()
main_w.title("Team 3's Event Calendar!")
main_w.geometry("900x650")

#month list for the calendar
months = [ "January", "February", "March", "April", "May", "June",
 "July", "August", "September", "October", "November", "December",]

#sets the year
current_year = 2026

#this makes the grid frame
cal_frame = tk.Frame(main_w)
cal_frame.pack(pady=20)

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

                #this creates the button for each day. Will make it do something later!
                day_btn = tk.Button( cal_frame, text=str(day_num), width=6, height=4, relief="raised")
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
