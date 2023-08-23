import time
import json
import requests
import threading
import tkinter as tk
from tkinter import ttk

class RealTimeDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Data Analytics")
        
        self.source_label = ttk.Label(root, text="Data Source:")
        self.source_label.pack(padx=10, pady=5)
        
        self.source_entry = ttk.Entry(root)
        self.source_entry.pack(padx=10, pady=5)
        
        self.metrics_label = ttk.Label(root, text="Metrics:")
        self.metrics_label.pack(padx=10, pady=5)
        
        self.metrics_text = tk.Text(root, height=5, width=30)
        self.metrics_text.pack(padx=10, pady=5)
        
        self.listen_button = ttk.Button(root, text="Start Listening", command=self.start_listening)
        self.listen_button.pack(padx=10, pady=5)
        
        self.data_text = tk.Text(root, height=10, width=50)
        self.data_text.pack(padx=10, pady=5)
        
        self.listen_thread = None

    def update_metrics(self):
        source = self.source_entry.get().strip()
        if source:
            metrics_url = f"http://localhost:5000/metrics/{source}"
            response = requests.get(metrics_url)
            if response.status_code == 200:
                metrics_data = response.json()
                self.metrics_text.delete('1.0', tk.END)
                self.metrics_text.insert(tk.END, f"Average: {metrics_data['average']:.2f}\n")
                self.metrics_text.insert(tk.END, f"Sum: {metrics_data['sum']:.2f}\n")
                self.metrics_text.insert(tk.END, f"Count: {metrics_data['count']}\n")
            else:
                self.metrics_text.delete('1.0', tk.END)
                self.metrics_text.insert(tk.END, "Error fetching metrics.")

    def start_listening(self):
        source = self.source_entry.get().strip()
        if source:
            self.data_text.delete('1.0', tk.END)
            self.listen_thread = threading.Thread(target=self.listen_updates, args=(source,))
            self.listen_thread.start()

    def listen_updates(self, source):
        listen_url = f"http://localhost:5000/listen/{source}"
        response = requests.get(listen_url, stream=True)
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                self.data_text.insert(tk.END, f"Timestamp: {data['timestamp']} | Value: {data['value']:.2f}\n")
                self.data_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeDataApp(root)
    root.mainloop()
