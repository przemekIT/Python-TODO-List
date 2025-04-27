import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from controller.task_controller import TaskController

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.controller = TaskController()
        self.list_visible = True  # Boolean flag for toggling visibility

        # UI Elements
        tk.Label(root, text="Tytuł zadania:").pack()
        self.entry_title = tk.Entry(root)
        self.entry_title.pack()

        tk.Label(root, text="Termin: (YYYY-MM-DD)").pack()  # Adjusted format hint
        self.entry_due_date = tk.Entry(root)
        self.entry_due_date.pack()

        tk.Label(root, text="Priorytet:").pack()
        self.priority_var = tk.StringVar(value="Średni")
        tk.OptionMenu(root, self.priority_var, "Wysoki", "Średni", "Niski").pack()

        self.btn_add = tk.Button(root, text="Dodaj Zadanie", command=self.add_task)
        self.btn_add.pack()

        # **Canvas for Task List**
        self.canvas = tk.Canvas(root, width=500, height=300, bg="white")
        self.canvas.pack()

        # **Toggle Button (Show/Hide Task List)**
        self.btn_toggle_list = tk.Button(root, text="Ukryj listę", command=self.toggle_list)
        self.btn_toggle_list.pack()

        self.btn_complete = tk.Button(root, text="Oznacz jako wykonane", command=self.mark_completed)
        self.btn_complete.pack()

        self.btn_delete = tk.Button(root, text="Usuń zadanie", command=self.delete_task)
        self.btn_delete.pack()

        self.load_tasks()

    def validate_date(self, date_str):
        """Sprawdza, czy podana data jest w formacie YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")  # Check format

            current_date = datetime.now().date()  # Get today's date

            if date_str <= current_date:
                return False  # Invalid date (must be in the future)
            return True
        
        except ValueError:
            return False

    def toggle_list(self):
        """ Toggles the visibility of the task list """
        if self.list_visible:
            self.canvas.pack_forget()  # Hide the Canvas
            self.btn_toggle_list.config(text="Pokaż listę")  # Update button label
        else:
            self.canvas.pack()  # Show the Canvas
            self.btn_toggle_list.config(text="Ukryj listę")  # Update button label

        self.list_visible = not self.list_visible  # Toggle the flag

    def add_task(self):
        title = self.entry_title.get()
        due_date = self.entry_due_date.get()
        priority = self.priority_var.get()

        # Validate input
        if not title or not due_date:
            messagebox.showwarning("Błąd", "Tytuł i termin są wymagane!")
            return

        # Validate date format
        if not self.validate_date(due_date):
            messagebox.showerror("Niepoprawna data", "Podaj poprawną datę w formacie YYYY-MM-DD!")
            return

        self.controller.add_task(title, due_date, priority)
        self.load_tasks()

    def delete_task(self):
        selected = self.canvas.find_withtag("selected")
        if selected:
            task_text = self.canvas.itemcget(selected[0], "text")
            title = task_text.split(" (")[0]  # Extract title
            self.controller.delete_task(title)
            self.load_tasks()

    def mark_completed(self):
        selected = self.canvas.find_withtag("selected")
        if selected:
            task_text = self.canvas.itemcget(selected[0], "text")
            title = task_text.split(" (")[0]  # Extract title
            self.controller.mark_completed(title)
            self.load_tasks()

    def load_tasks(self):
        """ Reloads tasks inside Canvas """
        self.canvas.delete("all")  # Clear existing text
        y_position = 20  # Starting position for text items

        for task in self.controller.tasks:
            text_item = self.canvas.create_text(
                250, y_position, text=f"{task.title} ({task.due_date}) [{task.priority}] - {task.status}",
                font=("Arial", 12), tags="task"
            )
            y_position += 30  # Move down for next item

        # Make tasks selectable (Click to highlight)
        self.canvas.tag_bind("task", "<Button-1>", self.select_task)

    def select_task(self, event):
        """ Selects a task by clicking on it """
        self.canvas.itemconfig("task", fill="black")  # Reset colors
        selected_task = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfig(selected_task, fill="blue")  # Highlight selected task
        self.canvas.addtag_withtag("selected", selected_task)

# Start
if __name__ == "__main__":   # Ensure it's only run when executed directly
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()