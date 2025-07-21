import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

class ModernToDo:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern To-Do List")
        self.master.geometry("400x500")
        self.master.configure(bg="light gray")

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="light gray")
        style.configure("TButton", padding=6, font=("Helvetica", 10))
        style.configure("TEntry", padding=6, font=("Helvetica", 10))
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        # Main Frame
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(expand=True, fill="both")

        # Task Entry Field and Add Button
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=33)
        self.task_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=1, padx=5, pady=5)

        # Task List Display (Treeview)
        self.task_tree = ttk.Treeview(self.frame, columns=("Tasks",), show="headings", height=15)
        self.task_tree.heading("Tasks", text="Tasks")
        self.task_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.task_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Delete, Edit, and Save Buttons
        delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        edit_button = ttk.Button(self.frame, text="Edit Task", command=self.edit_task)
        edit_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(self.frame, text="Save Tasks", command=self.save_tasks)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Configuring Grid to Expand
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.load_tasks()

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.task_tree.insert("", "end", values=(task,))
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please enter a task")

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            self.task_tree.delete(selected_item)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete")

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            current_task = self.task_tree.item(selected_item)["values"][0]
            self.task_var.set(current_task)  # Set the current task in the entry field
            self.delete_task()  # Remove the current task from the list
        else:
            messagebox.showwarning("Warning", "Please select a task to edit")

    def save_tasks(self):
        tasks = [self.task_tree.item(child)["values"] for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                for task in tasks:
                    self.task_tree.insert("", "end", values=(task,))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernToDo(root)
    root.mainloop()
