import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Task:
    def __init__(self, title, description, priority, status="To Do"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def update_status(self, new_status):
        self.status = new_status
        self.updated_at = datetime.datetime.now()

class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.master.geometry("800x600")
        self.tasks = []

        self.set_dark_theme()
        self.create_widgets()

    def set_dark_theme(self):
        self.master.configure(bg='#2E2E2E')
        style = ttk.Style(self.master)
        style.theme_use('clam')
        
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        style.configure('TButton', background='#4A4A4A', foreground='#FFFFFF')
        style.map('TButton', background=[('active', '#5A5A5A')])
        style.configure('TEntry', fieldbackground='#3E3E3E', foreground='#FFFFFF')
        style.configure('TCombobox', fieldbackground='#3E3E3E', background='#4A4A4A', foreground='#FFFFFF')
        
        style.configure('Treeview', 
                        background='#3E3E3E', 
                        fieldbackground='#3E3E3E', 
                        foreground='#FFFFFF')
        style.configure('Treeview.Heading', 
                        background='#4A4A4A', 
                        foreground='#FFFFFF')
        style.map('Treeview', background=[('selected', '#5A5A5A')])

    def create_widgets(self):
        # Task List
        self.tree = ttk.Treeview(self.master, columns=('Title', 'Priority', 'Status', 'Created', 'Updated'), show='headings')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Created', text='Created')
        self.tree.heading('Updated', text='Updated')
        self.tree.column('Title', width=200)
        self.tree.column('Priority', width=100)
        self.tree.column('Status', width=100)
        self.tree.column('Created', width=150)
        self.tree.column('Updated', width=150)
        self.tree.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Description Text
        self.desc_text = tk.Text(self.master, height=3, bg='#3E3E3E', fg='#FFFFFF')
        self.desc_text.pack(fill=tk.X, padx=10, pady=5)
        self.desc_text.config(state=tk.DISABLED)

        # Add Task Frame
        add_frame = ttk.Frame(self.master)
        add_frame.pack(pady=10)

        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.title_entry = ttk.Entry(add_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.desc_entry = ttk.Entry(add_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.priority_var = tk.StringVar()
        priority_options = ['Low', 'Medium', 'High']
        ttk.Combobox(add_frame, textvariable=self.priority_var, values=priority_options).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)

        # Update Status Frame
        update_frame = ttk.Frame(self.master)
        update_frame.pack(pady=10)

        self.status_var = tk.StringVar()
        status_options = ['To Do', 'In Progress', 'Done']
        ttk.Label(update_frame, text="New Status:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(update_frame, textvariable=self.status_var, values=status_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(update_frame, text="Update Status", command=self.update_task_status).grid(row=0, column=2, padx=5, pady=5)

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        priority = self.priority_var.get()
        if title and description and priority:
            task = Task(title, description, priority)
            self.tasks.append(task)
            self.update_task_list()
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.priority_var.set('')
        else:
            messagebox.showwarning("Invalid Input", "Please enter title, description, and priority.")

    def update_task_status(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_index = self.tree.index(selected_item)
            new_status = self.status_var.get()
            if new_status:
                self.tasks[task_index].update_status(new_status)
                self.update_task_list()
            else:
                messagebox.showwarning("Invalid Input", "Please select a status.")
        else:
            messagebox.showwarning("No Selection", "Please select a task to update.")

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            self.tree.insert('', tk.END, values=(task.title, task.priority, task.status, 
                                                 task.created_at.strftime("%Y-%m-%d %H:%M"),
                                                 task.updated_at.strftime("%Y-%m-%d %H:%M")))

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            task_index = self.tree.index(selected_item)
            task = self.tasks[task_index]
            self.desc_text.config(state=tk.NORMAL)
            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(tk.END, f"Description: {task.description}")
            self.desc_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()