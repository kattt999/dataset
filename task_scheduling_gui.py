import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox

class TaskManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management App")

        self.task_entries = {}
        self.selected_task_id = None

        self.create_ui()

    def create_ui(self):
        self.create_frame = ttk.LabelFrame(self.root, text="Create Task")
        self.create_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.title_label = ttk.Label(self.create_frame, text="Title:")
        self.title_label.grid(row=0, column=0, sticky="e")
        self.title_entry = ttk.Entry(self.create_frame)
        self.title_entry.grid(row=0, column=1, sticky="w")

        self.due_date_label = ttk.Label(self.create_frame, text="Due Date:")
        self.due_date_label.grid(row=1, column=0, sticky="e")
        self.due_date_entry = ttk.Entry(self.create_frame)
        self.due_date_entry.grid(row=1, column=1, sticky="w")

        self.priority_label = ttk.Label(self.create_frame, text="Priority:")
        self.priority_label.grid(row=2, column=0, sticky="e")
        self.priority_entry = ttk.Entry(self.create_frame)
        self.priority_entry.grid(row=2, column=1, sticky="w")

        self.create_button = ttk.Button(self.create_frame, text="Create Task", command=self.create_task)
        self.create_button.grid(row=3, columnspan=2)

        self.task_listbox = tk.Listbox(self.root)
        self.task_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

        self.progress_frame = ttk.LabelFrame(self.root, text="Task Progress")
        self.progress_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="w")

        self.progress_label = ttk.Label(self.progress_frame, text="Progress:")
        self.progress_label.grid(row=0, column=0, sticky="e")
        self.progress_entry = ttk.Entry(self.progress_frame)
        self.progress_entry.grid(row=0, column=1, sticky="w")

        self.update_progress_button = ttk.Button(self.progress_frame, text="Update Progress", command=self.update_progress)
        self.update_progress_button.grid(row=1, columnspan=2)

        self.update_task_list()

    def create_task(self):
        title = self.title_entry.get()
        due_date = self.due_date_entry.get()
        priority = int(self.priority_entry.get())
        data = {
            'title': title,
            'due_date': due_date,
            'priority': priority
        }
        response = requests.post('http://127.0.0.1:5000/tasks', json=data)
        if response.status_code == 201:
            self.title_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.update_task_list()
            self.selected_task_id = None
            self.progress_entry.delete(0, tk.END)
            self.update_progress_button["state"] = "disabled"
            self.show_message("Task created successfully", "Success")
        else:
            self.show_message("Failed to create task", "Error")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        response = requests.get('http://127.0.0.1:5000/tasks')
        tasks = response.json().get('tasks', [])
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task['title']} (ID: {task['id']})")

    def on_task_select(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_text = self.task_listbox.get(selected_index)
            task_id = int(selected_text.split("ID: ")[1][:-1])
            self.selected_task_id = task_id
            self.progress_entry.delete(0, tk.END)
            self.update_progress_button["state"] = "normal"

    def update_progress(self):
        if self.selected_task_id is not None:
            progress = int(self.progress_entry.get())
            data = {
                'progress': progress
            }
            response = requests.put(f'http://127.0.0.1:5000/tasks/{self.selected_task_id}/progress', json=data)
            if response.status_code == 200:
                self.show_message("Task progress updated successfully", "Success")
                self.update_progress_button["state"] = "disabled"
                self.progress_entry.delete(0, tk.END)
            else:
                self.show_message("Failed to update task progress", "Error")

    def show_message(self, message, title):
        messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagementApp(root)
    root.mainloop()
