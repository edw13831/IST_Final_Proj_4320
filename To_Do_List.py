import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime

# ---------- Config ----------
TASK_FILE = "tasks.json"
quotes = [
    "You got this!", "Keep going!", "Small steps, big wins.",
    "You're doing amazing!", "Finish strong!", "Make today count!"
]

category_colors = {
    "School": "blue",
    "Work": "green",
    "Personal": "purple",
    "Urgent": "red"
}

task_data = {}  # {task_id: {text, category, deadline, checked}}

# ---------- Functions ----------
def add_task():
    task_text = task_entry.get()
    category = category_combobox.get()
    deadline = deadline_entry.get()

    if not task_text or category == "Select" or not deadline:
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    try:
        datetime.strptime(deadline, "%Y-%m-%d")  # validate format
    except ValueError:
        messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
        return

    task_id = f"{task_text}-{deadline}-{random.randint(1000,9999)}"
    task_data[task_id] = {
        "text": task_text,
        "category": category,
        "deadline": deadline,
        "checked": False
    }
    refresh_task_list()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)
    category_combobox.set("Select")
    message_label.config(text=random.choice(quotes))

def refresh_task_list():
    task_listbox.delete(0, tk.END)
    for task_id, info in task_data.items():
        display = f"[{'✓' if info['checked'] else ' '}] {info['text']} ({info['category']}) - Due {info['deadline']}"
        task_listbox.insert(tk.END, display)
        color = category_colors.get(info['category'], "black")
        task_listbox.itemconfig(tk.END, {'fg': color})
    task_count_label.config(text=f"Total Tasks: {len(task_data)}")

def toggle_task():
    index = task_listbox.curselection()
    if index:
        selected_id = list(task_data.keys())[index[0]]
        task_data[selected_id]['checked'] = not task_data[selected_id]['checked']
        refresh_task_list()

def delete_task():
    index = task_listbox.curselection()
    if index:
        selected_id = list(task_data.keys())[index[0]]
        del task_data[selected_id]
        refresh_task_list()
    else:
        messagebox.showinfo("No Selection", "Select a task to delete.")

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(task_data, f)
    messagebox.showinfo("Saved", "Tasks saved successfully!")

def load_tasks():
    global task_data
    try:
        with open(TASK_FILE, "r") as f:
            task_data = json.load(f)
        refresh_task_list()
        message_label.config(text=random.choice(quotes))
    except FileNotFoundError:
        messagebox.showinfo("No File", "No saved task file found.")

# ---------- UI Setup ----------
root = tk.Tk()
root.title("Enhanced To-Do List App")
root.geometry("480x600")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

# Header
tk.Label(root, text="📝 My To-Do List", font=("Arial", 18, "bold"), bg="#f2f2f2").pack(pady=10)

# Task entry
entry_frame = tk.Frame(root, bg="#f2f2f2")
entry_frame.pack(pady=5)

tk.Label(entry_frame, text="Task:", bg="#f2f2f2").grid(row=0, column=0, sticky="w")
task_entry = tk.Entry(entry_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(entry_frame, text="Category:", bg="#f2f2f2").grid(row=1, column=0, sticky="w")
category_combobox = ttk.Combobox(entry_frame, values=list(category_colors.keys()), state="readonly")
category_combobox.set("Select")
category_combobox.grid(row=1, column=1, padx=5, pady=2)

tk.Label(entry_frame, text="Deadline (YYYY-MM-DD):", bg="#f2f2f2").grid(row=2, column=0, sticky="w")
deadline_entry = tk.Entry(entry_frame)
deadline_entry.grid(row=2, column=1, padx=5, pady=2)

# Buttons
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Task", bg="#4CAF50", fg="white", width=12, command=add_task).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Mark Done", bg="#2196F3", fg="white", width=12, command=toggle_task).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Task", bg="#f44336", fg="white", width=12, command=delete_task).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Save", bg="#9C27B0", fg="white", width=12, command=save_tasks).grid(row=1, column=0, pady=5)
tk.Button(button_frame, text="Load", bg="#FF9800", fg="white", width=12, command=load_tasks).grid(row=1, column=1, pady=5)

# Task listbox
task_listbox = tk.Listbox(root, width=60, height=15, selectbackground="lightblue")
task_listbox.pack(pady=10)

# Info
message_label = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="darkorange", bg="#f2f2f2")
message_label.pack()

task_count_label = tk.Label(root, text="Total Tasks: 0", font=("Arial", 10), bg="#f2f2f2")
task_count_label.pack()

# Load on start
load_tasks()

root.mainloop()
