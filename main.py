import datetime
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Notebook, Progressbar, Label, Button
from database import init_db, get_tasks_by_date
from task_manager import add_task_ui, update_task_list_ui
from schedule_manager import add_schedule_ui, add_calendar_ui
from task_manager import add_task_ui, update_task_list_ui, all_tasks_ui




# Global variables
selected_date = datetime.date.today()

# Initialize the database
init_db()

# Initialize the app
style = Style("darkly")
root = style.master
root.title("Planificator Academic")
root.geometry("900x700")

# --------------------
# Helper Functions
# --------------------

# Update progress bar
def actualizeaza_progres():
    tasks = get_tasks_by_date(selected_date)
    if tasks:
        completed_tasks = len([task for task in tasks if task[5] == 1])  # Check if completed == 1
        procent = (completed_tasks / len(tasks)) * 100
    else:
        procent = 0
    progres_bar["value"] = procent
    progres_percent.config(text=f"{int(procent)}%")

# Update the date and task list
def update_date(delta):
    global selected_date
    selected_date += datetime.timedelta(days=delta)
    date_label.config(text=selected_date.strftime("%A, %d %B %Y"))
    update_task_list_ui(task_list_frame, selected_date, actualizeaza_progres)
    actualizeaza_progres()

# --------------------
# UI Construction
# --------------------

# Create tabs
tabs = Notebook(root)
tabs.pack(fill="both", expand=True)

# Tasks Tab
tasks_tab = Frame(tabs)
tabs.add(tasks_tab, text="Tasks")

# Schedule Tab
schedule_tab = Frame(tabs)
tabs.add(schedule_tab, text="Schedule")

# Task Management Section
main_frame = Frame(tasks_tab, padding=10)
main_frame.pack(fill="both", expand=True)

# Date Navigation Section
date_frame = Frame(main_frame)
date_frame.pack(fill="x", pady=10)

# Previous Day Button
prev_day_button = Button(date_frame, text="← Previous", command=lambda: update_date(-1))
prev_day_button.pack(side="left", padx=10)

# Current date label
date_label = Label(date_frame, text=selected_date.strftime("%A, %d %B %Y"), font=("Helvetica", 16, "bold"))
date_label.pack(side="left", expand=True)

# Next Day Button
next_day_button = Button(date_frame, text="Next →", command=lambda: update_date(1))
next_day_button.pack(side="right", padx=10)

# Task List (Initialize before passing to add_task_ui)
task_list_frame = Frame(main_frame)
task_list_frame.pack(fill="both", expand=True)

# Task Input
task_input_frame = Frame(main_frame, padding=10)
task_input_frame.pack(fill="x", pady=10)

add_task_ui(task_input_frame, task_list_frame, selected_date, actualizeaza_progres)

# Update the task list immediately
update_task_list_ui(task_list_frame, selected_date, actualizeaza_progres)

# Progress Bar
progress_frame = Frame(main_frame, padding=10, relief="solid", borderwidth=1)
progress_frame.pack(fill="x", pady=10)

progress_label = Label(progress_frame, text="Progress", font=("Helvetica", 14, "bold"))
progress_label.pack(anchor="w")

progres_bar = Progressbar(progress_frame, value=0, length=200, bootstyle="success-striped")
progres_bar.pack(pady=10)

progres_percent = Label(progress_frame, text="0%", font=("Helvetica", 12))
progres_percent.pack()

# Schedule Management Section
schedule_frame = Frame(schedule_tab, padding=10)
schedule_frame.pack(fill="both", expand=True)

add_schedule_ui(schedule_frame)
add_calendar_ui(schedule_tab)
all_tasks_ui(main_frame)

# --------------------
# Final Setup
# --------------------
# Initialize progress bar
actualizeaza_progres()

# Run Application
root.mainloop()
