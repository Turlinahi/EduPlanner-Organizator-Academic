from tkinter import Label, Entry, Button, StringVar, Frame, OptionMenu, Toplevel, messagebox
from tkcalendar import Calendar
from database import add_schedule, get_schedule, get_tasks_by_date

def add_schedule_ui(schedule_frame):
    subject_var = StringVar()
    day_var = StringVar(value="Monday")
    start_time_var = StringVar()
    end_time_var = StringVar()

    subject_entry = Entry(schedule_frame, textvariable=subject_var, width=15)
    subject_entry.pack(side="left", padx=5)

    day_menu = OptionMenu(schedule_frame, day_var, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
    day_menu.pack(side="left", padx=5)

    start_time_entry = Entry(schedule_frame, textvariable=start_time_var, width=10)
    start_time_entry.pack(side="left", padx=5)

    end_time_entry = Entry(schedule_frame, textvariable=end_time_var, width=10)
    end_time_entry.pack(side="left", padx=5)

    def handle_add_schedule():
        subject = subject_var.get().strip()
        day = day_var.get()
        start_time = start_time_var.get().strip()
        end_time = end_time_var.get().strip()
        if subject and day and start_time and end_time:
            add_schedule(subject, day, start_time, end_time)
            messagebox.showinfo("Success", "Schedule added successfully!")
        else:
            messagebox.showwarning("Error", "All fields are required!")

    add_schedule_button = Button(schedule_frame, text="Add to Schedule", command=handle_add_schedule)
    add_schedule_button.pack(side="left", padx=5)

def add_calendar_ui(schedule_tab):
    def open_calendar():
        calendar_window = Toplevel(schedule_tab)
        calendar_window.title("Calendar")
        calendar_window.geometry("500x500")

        calendar = Calendar(calendar_window, selectmode='day', date_pattern="yyyy-mm-dd")
        calendar.pack(fill="both", expand=True)

        list_frame = Frame(calendar_window)
        list_frame.pack(fill="both", expand=True, pady=10)

        def on_date_selected(event):
            selected_date = calendar.selection_get()
            update_task_and_schedule_list(selected_date)

        calendar.bind("<<CalendarSelected>>", on_date_selected)

        def update_task_and_schedule_list(selected_date):
            for widget in list_frame.winfo_children():
                widget.destroy()

            tasks = get_tasks_by_date(str(selected_date))
            if tasks:
                Label(list_frame, text="Tasks:", font=("Helvetica", 14, "bold")).pack(anchor="w")
                for task in tasks:
                    _, name, priority, subject, _, completed = task
                    task_label = Label(list_frame, text=f"- {name} (Priority: {priority}, Subject: {subject or 'None'}, {'Done' if completed else 'Pending'})")
                    task_label.pack(anchor="w")

            schedules = get_schedule()
            schedules_for_date = [
                schedule for schedule in schedules if schedule[2] == selected_date.strftime("%A")
            ]
            if schedules_for_date:
                Label(list_frame, text="Schedules:", font=("Helvetica", 14, "bold")).pack(anchor="w")
                for schedule in schedules_for_date:
                    _, subject, day, start_time, end_time = schedule
                    schedule_label = Label(list_frame, text=f"- {subject} ({start_time} - {end_time})")
                    schedule_label.pack(anchor="w")

    open_calendar_button = Button(schedule_tab, text="Open Calendar", command=open_calendar)
    open_calendar_button.pack(pady=10)
