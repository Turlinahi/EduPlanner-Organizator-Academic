from tkinter import Label, Entry, Button, StringVar, Frame, OptionMenu, messagebox
from database import add_task, get_tasks_by_date, update_task_status
import datetime

def add_task_ui(task_input_frame, task_list_frame, date, update_progress):
    task_var = StringVar()
    priority_var = StringVar(value="Medium")
    subject_var = StringVar()

    task_entry = Entry(task_input_frame, textvariable=task_var, width=30)
    task_entry.pack(side="left", padx=5)

    priority_menu = OptionMenu(task_input_frame, priority_var, "High", "Medium", "Low")
    priority_menu.pack(side="left", padx=5)

    subject_entry = Entry(task_input_frame, textvariable=subject_var, width=15)
    subject_entry.pack(side="left", padx=5)

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
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks_by_date(str(date))
    for task in tasks:
        task_id, name, priority, subject, _, completed = task

        task_frame = Frame(task_list_frame)
        task_frame.pack(fill="x", pady=5)

        task_label = Label(task_frame, text=f"{name} (Priority: {priority}, Subject: {subject or 'None'})")
        task_label.pack(side="left")

        if not completed:
            complete_button = Button(task_frame, text="Mark Complete",
                                     command=lambda tid=task_id: mark_task_complete(tid, task_list_frame, date, update_progress))
            complete_button.pack(side="right", padx=5)

def mark_task_complete(task_id, task_list_frame, date, update_progress):
    update_task_status(task_id, True)
    update_task_list_ui(task_list_frame, date, update_progress)
    update_progress()
    messagebox.showinfo("Success", "Task marked as completed!")
