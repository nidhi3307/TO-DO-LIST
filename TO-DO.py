import tkinter as tk
from tkinter import messagebox
import os

TASK_FILE = "tasks.txt"

def load_tasks():
    tasks = []
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    task, status = line.rsplit("|", 1)
                    tasks.append({"task": task, "completed": status == "done"})
    return tasks

def save_tasks():
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        for t in tasks:
            status = "done" if t["completed"] else "pending"
            f.write(f"{t['task']}|{status}\n")

def refresh_listbox():
    listbox.delete(0, tk.END)
    for t in tasks:
        status = "✓" if t["completed"] else " "
        listbox.insert(tk.END, f"[{status}] {t['task']}")

def add_task():
    task_text = entry.get().strip()
    if task_text:
        tasks.append({"task": task_text, "completed": False})
        save_tasks()
        refresh_listbox()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        task_name = tasks[idx]["task"]
        del tasks[idx]
        save_tasks()
        refresh_listbox()
        messagebox.showinfo("Removed", f"Task '{task_name}' removed!")
    else:
        messagebox.showwarning("Warning", "Select a task to remove.")

def complete_task():
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        tasks[idx]["completed"] = True
        save_tasks()
        refresh_listbox()
    else:
        messagebox.showwarning("Warning", "Select a task to complete.")

# Load tasks
tasks = load_tasks()

# GUI setup
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=15)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

entry = tk.Entry(root, width=35)
entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

add_btn = tk.Button(btn_frame, text="Add Task", width=12, command=add_task)
add_btn.grid(row=0, column=0, padx=5)

remove_btn = tk.Button(btn_frame, text="Remove Task", width=12, command=remove_task)
remove_btn.grid(row=0, column=1, padx=5)

complete_btn = tk.Button(btn_frame, text="Complete Task", width=12, command=complete_task)
complete_btn.grid(row=0, column=2, padx=5)

refresh_listbox()
root.mainloop()
