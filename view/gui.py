import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
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

        today = datetime.today()
        tk.Label(root, text="Termin:").pack()

        self.entry_due_date = tk.Entry(root)
        self.entry_due_date.insert(0, today.strftime("%Y-%m-%d"))  # Set current date as default
        self.entry_due_date.pack()

        self.btn_open_calendar = tk.Button(root, text="Otwórz kalendarz", command=self.toggle_calendar)
        self.btn_open_calendar.pack()

        # Calendar (Initially Hidden)
        self.calendar = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day)
        self.calendar.bind("<<CalendarSelected>>", self.update_entry_due_date)

        tk.Label(root, text="Priorytet:").pack()
        self.priority_var = tk.StringVar(value="Średni")
        tk.OptionMenu(root, self.priority_var, "Wysoki", "Średni", "Niski").pack()

        # Create Frame for Task List & Scrollbar
        frame_list = tk.Frame(root)
        frame_list.pack(fill=tk.BOTH, expand=True)

        # Add Scrollbar
        scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create Canvas for Task List (linked to scrollbar)
        self.canvas = tk.Canvas(frame_list, width=500, height=300, bg="white", yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        # Create Scrollable Frame within Canvas
        self.task_frame = tk.Frame(self.canvas)
        self.task_frame.pack(fill=tk.BOTH, expand=True)
        self.task_window = self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw", width=self.canvas.winfo_width())

        # Ensure the scrollbar updates dynamically
        self.task_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Buttons (Side by Side)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_add = tk.Button(button_frame, text="➕ Dodaj Zadanie", command=self.add_task)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)

        self.btn_delete = tk.Button(button_frame, text="🗑 Usuń Zadanie", command=self.delete_task)
        self.btn_delete.grid(row=0, column=1, padx=5, pady=5)

        self.btn_complete = tk.Button(button_frame, text="✅ Oznacz jako wykonane", command=self.mark_completed)
        self.btn_complete.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Toggle Button for Showing/Hiding Task List
        self.btn_toggle_list = tk.Button(button_frame, text="📋 Pokaż/Ukryj listę", command=self.toggle_list)
        self.btn_toggle_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Ensure tasks load after UI finishes setting up
        self.root.after(100, self.load_tasks)

    def add_task(self):
        """Adds a new task to the list."""
        title = self.entry_title.get().strip()
        due_date = self.entry_due_date.get().strip()
        priority = self.priority_var.get()

        # Validate input
        if not title:
            messagebox.showwarning("Błąd", "Tytuł jest wymagany!")
            return
        if not due_date:
            messagebox.showwarning("Błąd", "Termin jest wymagany!")
            return
        if not self.validate_date(due_date):
            messagebox.showerror("Niepoprawna data", "Podaj poprawną datę w formacie YYYY-MM-DD!")
            return

        # Check for duplicate tasks
        for task in self.controller.tasks:
            if task.title.lower() == title.lower():
                messagebox.showerror("Błąd", "Zadanie o tym tytule już istnieje")
                return 

        # Add task if valid
        self.controller.add_task(title, due_date, priority)
        self.load_tasks()

    def load_tasks(self):
        """ Reloads tasks inside the scrollable frame and ensures tasks appear. """

        for widget in self.task_frame.winfo_children():
            widget.destroy()  # Clear previous tasks

        print("Loading tasks into UI...")
        print("Current tasks:", [task.title for task in self.controller.tasks])

        if not self.controller.tasks:
            print("No tasks found!")
            return  # Prevent unnecessary updates if task list is empty

        for idx, task in enumerate(self.controller.tasks):
            checkbox = "🗹" if task.status == "Wykonane" else "☐"

            task_label = tk.Label(
                self.task_frame,
                text=f"{checkbox} {task.title}\n📅 {task.due_date} | 🎯 {task.priority}",
                font=("Arial", 12),
                anchor="w",
                justify="left",
                bg="white",
                padx=10,
                pady=5
            )
            task_label.grid(row=idx, column=0, sticky="ew", padx=5, pady=5)

            # Fix event binding to allow proper selection
            task_label.bind("<Button-1>", lambda event, label=task_label, title=task.title: self.select_task(event, label, title))

            print(f"Created label for: {task.title}")

        # Ensure task list updates properly inside the canvas
        self.canvas.itemconfig(self.task_window, width=self.canvas.winfo_width())  
        self.task_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.update()

    def select_task(self, event, task_label, task_name):
        """ Highlights the selected task and stores its title for deletion/completion. """

        for widget in self.task_frame.winfo_children():
            widget.config(bg="white")

        task_label.config(bg="lightblue")  # ✅ Highlight the clicked task
        self.selected_task_title = task_name  # Store selected task

        print(f"Selected task: {task_name}")

    def mark_completed(self):
        if hasattr(self, "selected_task_title"):
            self.controller.mark_completed(self.selected_task_title)
            self.load_tasks()
        else:
            messagebox.showwarning("Błąd", "Najpierw wybierz zadanie do oznaczenia jako wykonane!")

    def toggle_list(self):
        self.list_visible = not self.list_visible
        self.canvas.pack() if self.list_visible else self.canvas.pack_forget()

    def toggle_calendar(self):
        self.calendar.pack_forget() if self.calendar.winfo_ismapped() else self.calendar.pack(after=self.btn_open_calendar)

    def update_entry_due_date(self, event):
        self.entry_due_date.delete(0, tk.END)
        self.entry_due_date.insert(0, self.calendar.get_date())

    def delete_task(self):
        if hasattr(self, "selected_task_title"):
            self.controller.delete_task(self.selected_task_title)
            self.load_tasks()
        else:
            messagebox.showwarning("Błąd", "Najpierw wybierz zadanie do usunięcia!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()