import sqlite3

DB_NAME = "planner.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            priority TEXT NOT NULL,
            subject TEXT,
            date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_task(task_name, priority, subject, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (task_name, priority, subject, date, completed)
        VALUES (?, ?, ?, ?, ?)
    ''', (task_name, priority, subject, date, 0))
    conn.commit()
    conn.close()

def get_tasks_by_date(date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE date = ?', (date,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, completed=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET completed = ? WHERE id = ?
    ''', (1 if completed else 0, task_id))
    conn.commit()
    conn.close()
    
def delete_task(task_id):
    """Delete a task from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def edit_task(task_id, task_name, priority, subject):
    """Edit a task in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET task_name = ?, priority = ?, subject = ? WHERE id = ?
    ''', (task_name, priority, subject, task_id))
    conn.commit()
    conn.close()


def add_schedule(subject, day, start_time, end_time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO schedule (subject, day, start_time, end_time)
        VALUES (?, ?, ?, ?)
    ''', (subject, day, start_time, end_time))
    conn.commit()
    conn.close()

def get_schedule():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schedule')
    schedules = cursor.fetchall()
    conn.close()
    return schedules
