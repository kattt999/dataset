import tkinter as tk
from tkinter import messagebox
import requests

# Define the API URLs
CREATE_EVENT_URL = 'http://127.0.0.1:5000/create_event'
UPDATE_EVENT_URL = 'http://127.0.0.1:5000/update_event'
USER_EVENTS_URL = 'http://127.0.0.1:5000/user_events'

class EventApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Scheduler")

        self.title_label = tk.Label(root, text="Event Title:")
        self.title_label.pack()

        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.pack()

        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.time_label = tk.Label(root, text="Time (HH:MM):")
        self.time_label.pack()

        self.time_entry = tk.Entry(root)
        self.time_entry.pack()

        self.duration_label = tk.Label(root, text="Duration (hours):")
        self.duration_label.pack()

        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()

        self.description_label = tk.Label(root, text="Description:")
        self.description_label.pack()

        self.description_entry = tk.Text(root, height=5, width=30)
        self.description_entry.pack()

        self.create_button = tk.Button(root, text="Create Event", command=self.create_event)
        self.create_button.pack()

        self.update_button = tk.Button(root, text="Update Event", command=self.update_event)
        self.update_button.pack()

        self.events_listbox = tk.Listbox(root, height=10, width=40)
        self.events_listbox.pack()

        self.refresh_button = tk.Button(root, text="Refresh Events", command=self.refresh_events)
        self.refresh_button.pack()

    def create_event(self):
        event_data = {
            "title": self.title_entry.get(),
            "description": self.description_entry.get("1.0", tk.END),
            "date": self.date_entry.get(),
            "time": self.time_entry.get(),
            "duration": int(self.duration_entry.get())
        }

        response = requests.post(CREATE_EVENT_URL, json=event_data)

        if response.status_code == 200:
            messagebox.showinfo("Success", "Event created successfully.")
        else:
            messagebox.showerror("Error", "Failed to create event.")

    def update_event(self):
        selected_event = self.events_listbox.get(tk.ACTIVE)
        if not selected_event:
            return

        event_id = int(selected_event.split()[0])

        event_data = {
            "title": self.title_entry.get(),
            "description": self.description_entry.get("1.0", tk.END),
            "date": self.date_entry.get(),
            "time": self.time_entry.get(),
            "duration": int(self.duration_entry.get())
        }

        response = requests.put(f"{UPDATE_EVENT_URL}/{event_id}", json=event_data)

        if response.status_code == 200:
            messagebox.showinfo("Success", "Event updated successfully.")
        else:
            messagebox.showerror("Error", "Failed to update event.")

    def refresh_events(self):
        response = requests.get(USER_EVENTS_URL)
        if response.status_code == 200:
            events = response.json().get("events", [])
            self.events_listbox.delete(0, tk.END)
            for event in events:
                self.events_listbox.insert(tk.END, f"{event['id']} - {event['title']} - {event['date']} {event['time']}")
        else:
            messagebox.showerror("Error", "Failed to fetch events.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()
