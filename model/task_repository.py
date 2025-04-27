import json
import os
from model.task import Task

TASKS_FILE = "data/tasks.json"

class TaskRepository:
    @staticmethod
    def load_tasks():
        """ Wczytanie zadań z pliku JSON """
        if not os.path.exists(TASKS_FILE):
            return []

        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Task.from_dict(task) for task in data]

    @staticmethod
    def save_tasks(tasks):
        """ Zapisanie listy zadań do pliku JSON """
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, indent=4)