import sqlite3
from tkinter import (
    Label,
    Entry,
    Button,
    StringVar,
    IntVar,
    Frame,
    OptionMenu,
    Checkbutton,
    messagebox,
    Toplevel,
    Scrollbar,
    Listbox,
    END,
)
from ttkbootstrap.widgets import DateEntry
from database import (
    add_task,
    get_tasks_by_date,
    update_task_status,
    delete_task,
    edit_task,
    get_all_tasks,
)
import datetime

# --------------------
# Add Task UI
# --------------------
def add_task_ui(task_input_frame, task_list_frame, date, update_progress):
    """Create the task input UI with date selection."""
    task_var = StringVar()
    priority_var = StringVar(value="Medium")
    subject_var = StringVar()

    # Task Name
    Label(task_input_frame, text="Task Name:", font=("Helvetica", 10)).pack(side="left", padx=5)
    task_entry = Entry(task_input_frame, textvariable=task_var, width=30)
    task_entry.pack(side="left", padx=5)

    # Priority
    Label(task_input_frame, text="Priority:", font=("Helvetica", 10)).pack(side="left", padx=5)
    priority_menu = OptionMenu(task_input_frame, priority_var, "High", "Medium", "Low")
    priority_menu.pack(side="left", padx=5)

    # Subject
    Label(task_input_frame, text="Subject:", font=("Helvetica", 10)).pack(side="left", padx=5)
    subject_entry = Entry(task_input_frame, textvariable=subject_var, width=15)
    subject_entry.pack(side="left", padx=5)

    # Date Picker
    Label(task_input_frame, text="Date:", font=("Helvetica", 10)).pack(side="left", padx=5)
    task_date_entry = DateEntry(task_input_frame, width=15, bootstyle="primary")
    task_date_entry.pack(side="left", padx=5)

    # Add Task Button
    def handle_add_task():
        task = task_var.get().strip()
        priority = priority_var.get()
        subject = subject_var.get().strip()
        task_date = task_date_entry.entry.get()

        if task and priority and task_date:
            add_task(task, priority, subject, task_date)
            task_var.set("")
            priority_var.set("Medium")
            subject_var.set("")
            task_date_entry.entry.delete(0, "end")
            task_date_entry.entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
            messagebox.showinfo("Success", "Task added successfully!")
            update_task_list_ui(task_list_frame, date, update_progress)
            update_progress()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    add_task_button = Button(task_input_frame, text="Add Task", command=handle_add_task)
    add_task_button.pack(side="left", padx=5)

# --------------------
# Update Task List UI
# --------------------
def update_task_list_ui(task_list_frame, date, update_progress):
    """Update the task list UI, sorting by date and priority."""
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    tasks = sorted(
        get_tasks_by_date(str(date)),
        key=lambda x: (x[4], {"High": 0, "Medium": 1, "Low": 2}[x[2]]),
    )

    for task in tasks:
        task_id, name, priority, subject, task_date, completed = task

        task_frame = Frame(task_list_frame)
        task_frame.pack(fill="x", pady=5)

        # Task Label
        task_label = Label(
            task_frame,
            text=f"{name} (Priority: {priority}, Subject: {subject or 'None'}, Date: {task_date})"
        )
        task_label.pack(side="left")

        # Mark Complete Button
        if not completed:
            complete_button = Button(
                task_frame,
                text="Mark Complete",
                command=lambda tid=task_id: mark_task_complete(tid, task_list_frame, date, update_progress)
            )
            complete_button.pack(side="right", padx=5)

        # Delete Button
        delete_button = Button(
            task_frame,
            text="Delete",
            command=lambda tid=task_id: delete_task_ui(tid, task_list_frame, date, update_progress)
        )
        delete_button.pack(side="right", padx=5)

        # Edit Button
        edit_button = Button(
            task_frame,
            text="Edit",
            command=lambda tid=task_id, tname=name, tpriority=priority, tsubject=subject, tcompleted=completed, tdate=task_date:
                edit_task_ui(tid, tname, tpriority, tsubject, tcompleted, tdate, task_list_frame, date, update_progress)
        )
        edit_button.pack(side="right", padx=5)

# --------------------
# Task Operations
# --------------------
def delete_task_ui(task_id, task_list_frame, date, update_progress):
    """Handle the deletion of a task."""
    delete_task(task_id)
    update_task_list_ui(task_list_frame, date, update_progress)
    update_progress()
    messagebox.showinfo("Success", "Task deleted successfully!")

def mark_task_complete(task_id, task_list_frame, date, update_progress):
    """Mark a task as complete."""
    update_task_status(task_id, True)
    update_task_list_ui(task_list_frame, date, update_progress)
    update_progress()
    messagebox.showinfo("Success", "Task marked as completed!")

def edit_task_ui(task_id, current_name, current_priority, current_subject, current_completed, current_date, task_list_frame, date, update_progress):
    """Open a window to edit a task."""
    edit_window = Toplevel()
    edit_window.title("Edit Task")
    edit_window.geometry("400x400")

    # Task Name
    Label(edit_window, text="Task Name:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_var = StringVar(value=current_name)
    name_entry = Entry(edit_window, textvariable=name_var, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Priority
    Label(edit_window, text="Priority:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    priority_var = StringVar(value=current_priority)
    priority_menu = OptionMenu(edit_window, priority_var, "High", "Medium", "Low")
    priority_menu.grid(row=1, column=1, padx=10, pady=10)

    # Subject
    Label(edit_window, text="Subject:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    subject_var = StringVar(value=current_subject)
    subject_entry = Entry(edit_window, textvariable=subject_var, width=30)
    subject_entry.grid(row=2, column=1, padx=10, pady=10)

    # Date
    Label(edit_window, text="Date:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    date_entry = DateEntry(edit_window, width=15, bootstyle="primary")
    date_entry.entry.delete(0, "end")
    date_entry.entry.insert(0, current_date)
    date_entry.grid(row=3, column=1, padx=10, pady=10)

    # Task Done Checkbox
    Label(edit_window, text="Task Done?", font=("Helvetica", 12)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    completed_var = IntVar(value=current_completed)
    completed_checkbox = Checkbutton(edit_window, variable=completed_var)
    completed_checkbox.grid(row=4, column=1, padx=10, pady=10)

    # Save Changes Button
    def save_changes():
        new_name = name_var.get().strip()
        new_priority = priority_var.get()
        new_subject = subject_var.get().strip()
        new_date = date_entry.entry.get()
        is_completed = completed_var.get()
        if new_name and new_priority and new_date:
            edit_task(task_id, new_name, new_priority, new_subject, new_date)
            update_task_status(task_id, bool(is_completed))
            update_task_list_ui(task_list_frame, date, update_progress)
            update_progress()
            messagebox.showinfo("Success", "Task updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=5, column=0, columnspan=2, pady=20)

# --------------------
# All Tasks UI
# --------------------
def all_tasks_ui(parent_frame):
    """Add the 'All Tasks' button to view tasks for different periods."""
    def show_all_tasks():
        # Create a popup to select the time period
        popup = Toplevel()
        popup.title("View All Tasks")
        popup.geometry("400x300")

        Label(popup, text="Select a period:", font=("Helvetica", 12)).pack(pady=10)

        def fetch_tasks(period):
            tasks = get_all_tasks(period)
            show_tasks_window(tasks)
            popup.destroy()

        Button(popup, text="This Week", command=lambda: fetch_tasks("week")).pack(pady=5)
        Button(popup, text="This Month", command=lambda: fetch_tasks("month")).pack(pady=5)
        Button(popup, text="This Year", command=lambda: fetch_tasks("year")).pack(pady=5)

    def show_tasks_window(tasks):
        """Display tasks in a new window."""
        tasks_window = Toplevel()
        tasks_window.title("All Tasks")
        tasks_window.geometry("600x400")

        if tasks:
            for task in tasks:
                Label(tasks_window, text=f"{task[1]} (Priority: {task[2]}, Date: {task[4]})", anchor="w").pack(fill="x", padx=10, pady=5)
        else:
            Label(tasks_window, text="No tasks found for the selected period.", font=("Helvetica", 12)).pack(pady=20)

    # Add the "All Tasks" button to the main frame
    all_tasks_button = Button(parent_frame, text="All Tasks", command=show_all_tasks)
    all_tasks_button.pack(side="bottom", pady=10)

def display_tasks(window, tasks):
    """Display tasks in a scrollable list."""
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="All Tasks", font=("Helvetica", 14, "bold")).pack()

    if not tasks:
        Label(window, text="No tasks found for the selected period.").pack()
        return

    frame = Frame(window)
    frame.pack(fill="both", expand=True)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    task_listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    for task in tasks:
        task_id, name, priority, subject, task_date, completed = task
        task_listbox.insert(
            END,
            f"{name} (Priority: {priority}, Subject: {subject or 'None'}, Date: {task_date}, Completed: {'Yes' if completed else 'No'})"
        )
    task_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=task_listbox.yview)
