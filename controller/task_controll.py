from datetime import datetime, timedelta
from tkinter import messagebox
from model.task_model import Task, TaskRepository, Priority, Status
from view.task_view import TaskView
import tkinter as tk
from tkinter import ttk
import csv
from fpdf import FPDF
from pathlib import Path
from datetime import datetime
import unicodedata


class TaskController:
    theme_loaded = False
    def __init__(self, root):
        self.repo = TaskRepository()
        self.view = TaskView(root, self)
        
        self.schedule_notifications()
        self.refresh_task_list()

    def add_task(self):
        inputs = self.view.get_task_inputs()
        title = inputs['title']
        desc = inputs['description']
        due_str = inputs['due_date']
        priority_str = inputs['priority']

        if not title:
            messagebox.showerror("Błąd", "Tytuł jest wymagany!")
            return

        try:
            if due_str:
                due_date = datetime.strptime(due_str, "%Y-%m-%d")
                now = datetime.now()
                due_date = due_date.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=0)
            else:
                due_date = None
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty!")
            return

        priority = Priority(priority_str)

        task = Task(title, desc, due_date, priority)
        self.repo.add_task(task)
        self.view.clear_inputs()
        self.refresh_task_list()

    def refresh_task_list(self):
        tasks = self.repo.tasks
        self.view.show_tasks(tasks)

    def get_task_by_title(self, title):
        for task in self.repo.tasks:
            if task.title == title:
                return task
        return None

    def mark_done(self):
        title = self.view.get_selected_task_title()
        if not title:
            messagebox.showwarning("Uwaga", "Wybierz zadanie!")
            return
        task = self.get_task_by_title(title)
        self.repo.mark_done(task)
        self.refresh_task_list()

    def remove_task(self):
        title = self.view.get_selected_task_title()
        if not title:
            messagebox.showwarning("Uwaga", "Wybierz zadanie!")
            return
        task = self.get_task_by_title(title)
        self.repo.remove_task(task)
        self.refresh_task_list()

    def check_notifications(self):
        now = datetime.now()
        for task in self.repo.tasks:
            if task.status == Status.PENDING and task.due_date:
                if task.due_date.date() == now.date():
                    delta = task.due_date - now
                    if timedelta(minutes=0) <= delta <= timedelta(hours=1):
                        self.view.notify(f"Zbliża się termin zadania: {task.title}")

    def schedule_notifications(self):
        self.check_notifications()
        self.view.master.after(60000, self.schedule_notifications)

    def apply_filter(self):
        priority_val = self.view.priority_filter.get()
        status_val = self.view.status_filter.get()
        due_today = bool(self.view.today_var.get())

        priority = Priority(priority_val) if priority_val else None
        status = Status(status_val) if status_val else None

        tasks = self.repo.filter_tasks(priority=priority, status=status, due_today=due_today)
        self.view.show_tasks(tasks)
        
    def edit_task(self):
        title = self.view.get_selected_task_title()
        if not title:
            messagebox.showwarning("Uwaga", "Wybierz zadanie!")
            return

        task = self.get_task_by_title(title)
        inputs = self.view.get_task_inputs()

        if not inputs['title']:
            messagebox.showerror("Błąd", "Tytuł jest wymagany!")
            return

        description = inputs['description'] if inputs['description'] else task.description

        try:
            if inputs['due_date']:
                due_date = datetime.strptime(inputs['due_date'], "%Y-%m-%d")
                now = datetime.now()
                due_date = due_date.replace(hour=now.hour, minute=now.minute, second=now.second, microsecond=0)
            else:
                due_date = task.due_date
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty!")
            return

        try:
            priority = Priority(inputs['priority']) if inputs['priority'] else task.priority
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy priorytet!")
            return

        task.title = inputs['title']
        task.description = description
        task.due_date = due_date
        task.priority = priority

        self.repo.save()
        self.view.clear_inputs()
        self.refresh_task_list()


    def export_csv(self):
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / "assets" / "tasks_export.csv").resolve()

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Tytuł', 'Opis', 'Termin', 'Priorytet', 'Status'])
                for task in self.repo.tasks:
                    due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""
                    writer.writerow([task.title, task.description, due, task.priority.value, task.status.value])
            messagebox.showinfo("Eksport", f"Zadania wyeksportowane do {file_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować pliku:\n{e}")

    def swap_tasks(self, index1, index2):
        self.repo.tasks[index1], self.repo.tasks[index2] = self.repo.tasks[index2], self.repo.tasks[index1]
        self.repo.save()
    
    def toggle_theme(self):
        current_theme = self.view.master.tk.call('ttk::style', 'theme', 'use')
        new_theme = "light" if "dark" in current_theme else "dark"
        TaskController.enable_theme(self.view.master, new_theme)

    @staticmethod
    def enable_theme(root, mode="dark"):
        style = ttk.Style(root)
        basePath = Path(__file__).parent
        file_path = (basePath / ".." / "assets/themes/azure.tcl" ).resolve()

        if not TaskController.theme_loaded:
            root.tk.call("source", file_path)
            TaskController.theme_loaded = True

        if mode == "dark":
            style.theme_use("azure-dark")
        else:
            style.theme_use("azure-light")

    def clean_text(self, text):
        return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

    def export_pdf(self):
        basePath = Path(__file__).parent
        pdf_path = (basePath / ".." / "assets" / "tasks_export.pdf").resolve()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Lista zadan", ln=True, align='C')
        pdf.ln(5)

        for task in self.repo.tasks:
            due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""

            title = self.clean_text(task.title)
            desc = self.clean_text(task.description)
            priority = self.clean_text(task.priority.value)
            status = self.clean_text(task.status.value)

            pdf.multi_cell(0, 10,
                f"Tytul: {title}\nOpis: {desc}\nTermin: {due}\nPriorytet: {priority}\nStatus: {status}\n---"
            )

        try:
            pdf.output(str(pdf_path))
            messagebox.showinfo("Eksport", f"Zadania wyeksportowane do {pdf_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować pliku:\n{e}")

    def run(self):
        self.root.mainloop()