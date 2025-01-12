from tkinter import Label, Entry, Button, StringVar, Frame, OptionMenu, Toplevel, messagebox
from tkcalendar import Calendar
from database import add_schedule, get_schedule, get_tasks_by_date


def add_schedule_ui(schedule_frame):
    """Create the UI for adding a schedule."""
    subject_var = StringVar()
    day_var = StringVar(value="Monday")
    start_time_var = StringVar()
    end_time_var = StringVar()

    # Subject Entry
    Label(schedule_frame, text="Subject:", font=("Helvetica", 10)).pack(side="left", padx=5)
    subject_entry = Entry(schedule_frame, textvariable=subject_var, width=15)
    subject_entry.pack(side="left", padx=5)

    # Day Selection
    Label(schedule_frame, text="Day:", font=("Helvetica", 10)).pack(side="left", padx=5)
    day_menu = OptionMenu(schedule_frame, day_var, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
    day_menu.pack(side="left", padx=5)

    # Start Time Entry
    Label(schedule_frame, text="Start Time:", font=("Helvetica", 10)).pack(side="left", padx=5)
    start_time_entry = Entry(schedule_frame, textvariable=start_time_var, width=10)
    start_time_entry.pack(side="left", padx=5)

    # End Time Entry
    Label(schedule_frame, text="End Time:", font=("Helvetica", 10)).pack(side="left", padx=5)
    end_time_entry = Entry(schedule_frame, textvariable=end_time_var, width=10)
    end_time_entry.pack(side="left", padx=5)

    # Add Schedule Button
    def handle_add_schedule():
        subject = subject_var.get().strip()
        day = day_var.get()
        start_time = start_time_var.get().strip()
        end_time = end_time_var.get().strip()
        if subject and day and start_time and end_time:
            add_schedule(subject, day, start_time, end_time)
            messagebox.showinfo("Success", "Schedule added successfully!")
            subject_var.set("")
            start_time_var.set("")
            end_time_var.set("")
        else:
            messagebox.showwarning("Error", "All fields are required!")

    add_schedule_button = Button(schedule_frame, text="Add to Schedule", command=handle_add_schedule)
    add_schedule_button.pack(side="left", padx=5)





def add_calendar_ui(schedule_tab):
    """Add a button to open a calendar view and display tasks and schedules."""

    def open_calendar():
        """Open a new window containing the calendar and related task/schedule details."""
        calendar_window = Toplevel(schedule_tab)
        calendar_window.title("Calendar")
        calendar_window.geometry("500x500")

        # Add a Calendar widget
        try:
            calendar = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
            calendar.pack(fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            print(f"Error creating Calendar widget: {e}")
            messagebox.showerror("Error", f"Error loading calendar: {e}")
            return

        # Frame for task and schedule list
        list_frame = Frame(calendar_window)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        def update_task_and_schedule_list(selected_date):
            """Display tasks and schedules for the selected date."""
            # Clear the list frame
            for widget in list_frame.winfo_children():
                widget.destroy()

            # Fetch tasks for the selected date
            tasks = get_tasks_by_date(str(selected_date))
            if tasks:
                Label(list_frame, text="Tasks:", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=5)
                for task in tasks:
                    _, name, priority, subject, _, completed = task
                    task_status = "Done" if completed else "Pending"
                    task_label = Label(
                        list_frame,
                        text=f"• {name} (Priority: {priority}, Subject: {subject or 'None'}, Status: {task_status})",
                    )
                    task_label.pack(anchor="w")

            # Fetch schedules for the selected date
            schedules = get_schedule()
            if schedules:
                Label(list_frame, text="Schedules:", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=5)
                for schedule in schedules:
                    _, subject, day, start_time, end_time = schedule
                    schedule_label = Label(
                        list_frame,
                        text=f"• {subject} ({start_time} - {end_time}, {day})",
                    )
                    schedule_label.pack(anchor="w")

        def on_date_selected(event):
            """Handle date selection from the calendar."""
            selected_date = calendar.selection_get()
            update_task_and_schedule_list(selected_date)

        # Bind the calendar selection to the handler
        calendar.bind("<<CalendarSelected>>", on_date_selected)

    # Add a button to open the calendar
    open_calendar_button = Button(schedule_tab, text="Open Calendar", command=open_calendar)
    open_calendar_button.pack(pady=10)
