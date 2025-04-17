import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox
from canvasapi import Canvas
from datetime import datetime
import pytz 
import threading


# Load API token
load_dotenv()
API_KEY = os.getenv("CANVAS_API_TOKEN")
API_URL = "https://gatech.instructure.com"

canvas = Canvas(API_URL, API_KEY)
courses = list(canvas.get_courses(enrollment_state='active'))

# Tkinter App
root = tk.Tk()
root.title("Canvas Course Assignments")
root.geometry("800x1000")

# Course List
course_listbox = tk.Listbox(root, height=15, font=("Segoe UI", 12))
course_listbox.pack(fill=tk.X, padx=10, pady=10)

# Scrollable frame for assignments
assignments_text = tk.Text(root, height=15, font=("Consolas", 11))
assignments_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))


def on_course_select(event):
    def fetch_assignments():
        selection = course_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        course = courses[index]

        # Show loading message (on main thread)
        assignments_text.after(0, lambda: assignments_text.delete(1.0, tk.END))
        assignments_text.after(0, lambda: assignments_text.insert(
            tk.END, f"Loading assignments for: {course.name}...\n"))

        try:
            assignments = list(course.get_assignments())

            est = pytz.timezone("US/Eastern")
            now = datetime.now(est)

            upcoming = []
            for a in assignments:
                if a.due_at:
                    due_utc = datetime.strptime(a.due_at, "%Y-%m-%dT%H:%M:%SZ")
                    due_local = due_utc.replace(tzinfo=pytz.utc).astimezone(est)
                    if due_local.date() >= now.date():
                        upcoming.append((a.name, due_local))

            upcoming.sort(key=lambda x: x[1])

            def display_results():
                assignments_text.delete(1.0, tk.END)
                assignments_text.insert(
                    tk.END, f"Upcoming Assignments for: {course.name}\n\n")

                for name, due_local in upcoming:
                    due_str = due_local.strftime("%B %d, %Y at %I:%M %p %Z")
                    assignments_text.insert(tk.END, f"- {name}\n  Due: {due_str}\n\n")

                if not upcoming:
                    assignments_text.insert(tk.END, "No upcoming assignments.\n")

            # Replace loading text with results
            assignments_text.after(0, display_results)

        except Exception as e:
            assignments_text.after(0, lambda: messagebox.showerror(
                "Error", f"Could not fetch assignments: {e}"))

    # Start loading assignments in a new thread
    threading.Thread(target=fetch_assignments, daemon=True).start()

# Populate course list
for c in courses:
    course_listbox.insert(tk.END, c.name)

course_listbox.bind("<<ListboxSelect>>", on_course_select)

root.mainloop()
