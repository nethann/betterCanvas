import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox
from canvasapi import Canvas
from datetime import datetime
import pytz 


# Load API token
load_dotenv()
API_KEY = os.getenv("CANVAS_API_TOKEN")
API_URL = "https://gatech.instructure.com"

canvas = Canvas(API_URL, API_KEY)
courses = list(canvas.get_courses(enrollment_state='active'))

# Tkinter App
root = tk.Tk()
root.title("Canvas Course Assignments")
root.geometry("700x500")

# Course List
course_listbox = tk.Listbox(root, height=15, font=("Segoe UI", 12))
course_listbox.pack(fill=tk.X, padx=10, pady=10)

# Scrollable frame for assignments
assignments_text = tk.Text(root, height=15, font=("Consolas", 11))
assignments_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

def on_course_select(event):
    selection = course_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    course = courses[index]

    try:
        assignments = list(course.get_assignments())

        est = pytz.timezone("US/Eastern")
        now = datetime.now(est)

        # Only keep assignments due today or later
        upcoming = []
        for a in assignments:
            if a.due_at:
                due_utc = datetime.strptime(a.due_at, "%Y-%m-%dT%H:%M:%SZ")
                due_local = due_utc.replace(tzinfo=pytz.utc).astimezone(est)

                if due_local.date() >= now.date():  # today or future
                    upcoming.append((a.name, due_local))

        # Sort by due date ascending
        upcoming.sort(key=lambda x: x[1])

        assignments_text.delete(1.0, tk.END)
        assignments_text.insert(tk.END, f"Upcoming Assignments for: {course.name}\n\n")

        for name, due_local in upcoming:
            due_str = due_local.strftime("%B %d, %Y at %I:%M %p %Z")
            assignments_text.insert(tk.END, f"- {name}\n  Due: {due_str}\n\n")

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch assignments: {e}")

# Populate course list
for c in courses:
    course_listbox.insert(tk.END, c.name)

course_listbox.bind("<<ListboxSelect>>", on_course_select)

root.mainloop()
