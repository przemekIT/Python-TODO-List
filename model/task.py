import json
from datetime import datetime

class Task:
    def __init__(self, title, due_date, priority="Średni", status="Oczekujące", description=""):
        self.title = title
        self.description = description
        self.due_date = due_date  # Format: "YYYY-MM-DD HH:MM"
        self.priority = priority
        self.status = status

    def to_dict(self):
        """ Konwersja obiektu na słownik do zapisu w JSON """
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """ Tworzenie obiektu Task z JSON """
        return Task(data["title"], data["due_date"], data.get("priority"), data.get("status"), data.get("description"))