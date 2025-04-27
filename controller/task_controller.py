from model.task_repository import TaskRepository
from model.task import Task

class TaskController:
    def __init__(self):
        self.tasks = TaskRepository.load_tasks()

    def add_task(self, title, due_date, priority="Średni", description=""):
        """ Dodawanie nowego zadania """
        task = Task(title, due_date, priority, description=description)
        self.tasks.append(task)
        TaskRepository.save_tasks(self.tasks)

    def delete_task(self, title):
        """ Usuwanie zadania według tytułu """
        self.tasks = [task for task in self.tasks if task.title != title]  # Filter out the task
        TaskRepository.save_tasks(self.tasks)  # Save updated task list


    def mark_completed(self, title):
        """ Oznaczanie zadania jako wykonane """
        for task in self.tasks:
            if task.title == title:
                task.status = "Wykonane"
        TaskRepository.save_tasks(self.tasks)

    def filter_tasks(self, status=None, priority=None):
        """ Filtracja według statusu lub priorytetu """
        return [task for task in self.tasks if (not status or task.status == status) and (not priority or task.priority == priority)]