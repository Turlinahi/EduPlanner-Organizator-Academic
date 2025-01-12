from tkinter import Label, Entry, Button, StringVar, IntVar, Frame, OptionMenu, Checkbutton, messagebox, Toplevel
from database import add_task, get_tasks_by_date, update_task_status, delete_task, edit_task
import datetime

def add_task_ui(task_input_frame, task_list_frame, date, update_progress):
    """Create the task input UI."""
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

    # Add Task Button
    def handle_add_task():
        task = task_var.get().strip()
        priority = priority_var.get()
        subject = subject_var.get().strip()
        if task and priority:
            add_task(task, priority, subject, str(date))
            task_var.set("")
            priority_var.set("Medium")
            subject_var.set("")
            messagebox.showinfo("Success", "Task added successfully!")
            update_task_list_ui(task_list_frame, date, update_progress)
            update_progress()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    add_task_button = Button(task_input_frame, text="Add Task", command=handle_add_task)
    add_task_button.pack(side="left", padx=5)


def update_task_list_ui(task_list_frame, date, update_progress):
    """Update the task list UI for a specific date."""
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks_by_date(str(date))
    for task in tasks:
        task_id, name, priority, subject, _, completed = task

        task_frame = Frame(task_list_frame)
        task_frame.pack(fill="x", pady=5)

        # Task Label
        task_label = Label(task_frame, text=f"{name} (Priority: {priority}, Subject: {subject or 'None'})")
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
            command=lambda tid=task_id, tname=name, tpriority=priority, tsubject=subject, tcompleted=completed: 
                edit_task_ui(tid, tname, tpriority, tsubject, tcompleted, task_list_frame, date, update_progress)
        )
        edit_button.pack(side="right", padx=5)


def delete_task_ui(task_id, task_list_frame, date, update_progress):
    """Handle the deletion of a task."""
    delete_task(task_id)
    update_task_list_ui(task_list_frame, date, update_progress)
    update_progress()
    messagebox.showinfo("Success", "Task deleted successfully!")

def edit_task_ui(task_id, current_name, current_priority, current_subject, current_completed, task_list_frame, date, update_progress):
    """Open a window to edit a task."""
    edit_window = Toplevel()
    edit_window.title("Edit Task")
    edit_window.geometry("400x350")  # Ensure enough space for all widgets

    # Task Name
    Label(edit_window, text="Task Name:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_var = StringVar()  # Initialize a new StringVar for this task
    name_var.set(current_name)  # Set the current value
    name_entry = Entry(edit_window, textvariable=name_var, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Priority
    Label(edit_window, text="Priority:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    priority_var = StringVar()  # Initialize a new StringVar for this task
    priority_var.set(current_priority)  # Set the current value
    priority_menu = OptionMenu(edit_window, priority_var, "High", "Medium", "Low")
    priority_menu.grid(row=1, column=1, padx=10, pady=10)

    # Subject
    Label(edit_window, text="Subject:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    subject_var = StringVar()  # Initialize a new StringVar for this task
    subject_var.set(current_subject)  # Set the current value
    subject_entry = Entry(edit_window, textvariable=subject_var, width=30)
    subject_entry.grid(row=2, column=1, padx=10, pady=10)

    # Task Done Checkbox
    Label(edit_window, text="Task Done?", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    completed_var = IntVar()  # Initialize a new IntVar for this task
    completed_var.set(current_completed)  # Set the current value (1 if done, 0 otherwise)
    completed_checkbox = Checkbutton(edit_window, variable=completed_var)
    completed_checkbox.grid(row=3, column=1, padx=10, pady=10)

    # Save Changes Button
    def save_changes():
        new_name = name_var.get().strip()
        new_priority = priority_var.get()
        new_subject = subject_var.get().strip()
        is_completed = completed_var.get()  # 1 for done, 0 for not done
        if new_name and new_priority:
            # Update task in the database
            edit_task(task_id, new_name, new_priority, new_subject)
            # Update task status if "Task Done?" was toggled
            update_task_status(task_id, bool(is_completed))
            # Refresh UI
            update_task_list_ui(task_list_frame, date, update_progress)
            update_progress()
            messagebox.showinfo("Success", "Task updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    # Add Save Button
    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Configure window layout
    edit_window.grid_columnconfigure(0, weight=1)
    edit_window.grid_columnconfigure(1, weight=1)

def mark_task_complete(task_id, task_list_frame, date, update_progress):
    """Mark a task as complete."""
    update_task_status(task_id, True)
    update_task_list_ui(task_list_frame, date, update_progress)
    update_progress()
    messagebox.showinfo("Success", "Task marked as completed!")
