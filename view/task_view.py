import tkinter as tk
from tkinter import ttk, messagebox
from model.task_model import Priority, Status


class TaskView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Tytuł").grid(row=0, column=0)
        self.title_entry = tk.Entry(form_frame, width=20)
        self.title_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Opis").grid(row=1, column=0)
        self.desc_entry = tk.Entry(form_frame, width=20)
        self.desc_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Termin (YYYY-MM-DD HH:MM)").grid(row=2, column=0)
        self.due_entry = tk.Entry(form_frame, width=20)
        self.due_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Priorytet").grid(row=3, column=0)
        self.priority_combo = ttk.Combobox(form_frame, values=[p.value for p in Priority], state="readonly")
        self.priority_combo.grid(row=3, column=1)
        self.priority_combo.set(Priority.MEDIUM.value)

        self.add_button = tk.Button(form_frame, text="Dodaj zadanie", command=self.controller.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self, columns=('Tytuł', 'Termin', 'Priorytet', 'Status'), show='headings')
        self.tree.heading('Tytuł', text='Tytuł')
        self.tree.heading('Termin', text='Termin')
        self.tree.heading('Priorytet', text='Priorytet')
        self.tree.heading('Status', text='Status')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree.bind("<ButtonPress-1>", self.on_start_drag)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drop)

        self.dragging_item = None

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Oznacz jako wykonane", command=self.controller.mark_done).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Usuń zadanie", command=self.controller.remove_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Odśwież", command=self.controller.refresh_task_list).pack(side=tk.LEFT, padx=5)

        self.create_filters()

        tk.Button(btn_frame, text="Edytuj zadanie", command=self.controller.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eksportuj do CSV", command=self.controller.export_csv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Przełącz motyw", command=self.controller.toggle_theme).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Eksportuj do PDF", command=self.controller.export_pdf).pack(side=tk.LEFT, padx=5)



    def create_filters(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filtruj po priorytecie:").grid(row=0, column=0)
        self.priority_filter = ttk.Combobox(filter_frame, values=[""] + [p.value for p in Priority], state="readonly")
        self.priority_filter.grid(row=0, column=1)
        self.priority_filter.set("")

        tk.Label(filter_frame, text="Filtruj po statusie:").grid(row=1, column=0)
        self.status_filter = ttk.Combobox(filter_frame, values=[""] + [s.value for s in Status], state="readonly")
        self.status_filter.grid(row=1, column=1)
        self.status_filter.set("")

        self.today_var = tk.IntVar()
        tk.Checkbutton(filter_frame, text="Tylko na dziś", variable=self.today_var).grid(row=2, column=0, columnspan=2)

        tk.Button(filter_frame, text="Zastosuj filtr", command=self.controller.apply_filter).grid(row=3, column=0, columnspan=2, pady=5)

    def get_task_inputs(self):
        return {
            'title': self.title_entry.get(),
            'description': self.desc_entry.get(),
            'due_date': self.due_entry.get(),
            'priority': self.priority_combo.get()
        }

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.priority_combo.set(Priority.MEDIUM.value)

    def show_tasks(self, tasks):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in tasks:
            due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""
            self.tree.insert('', tk.END, values=(task.title, due, task.priority.value, task.status.value))

    def get_selected_task_title(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])['values'][0]

    def notify(self, message):
        messagebox.showinfo("Powiadomienie", message)

    def on_start_drag(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.dragging_item = item

    def on_drag_motion(self, event):
        pass

    def on_drop(self, event):
        target_item = self.tree.identify_row(event.y)
        if self.dragging_item and target_item and self.dragging_item != target_item:
            dragging_values = self.tree.item(self.dragging_item)['values']
            target_values = self.tree.item(target_item)['values']

            dragging_index = self.tree.index(self.dragging_item)
            target_index = self.tree.index(target_item)

            self.tree.move(self.dragging_item, '', target_index)

            self.controller.swap_tasks(dragging_index, target_index)

        self.dragging_item = None