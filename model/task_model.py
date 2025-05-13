import json
import os
from datetime import datetime
from enum import Enum


class Priority(Enum):
    HIGH = "wysoki"
    MEDIUM = "średni"
    LOW = "niski"


class Status(Enum):
    PENDING = "oczekujące"
    DONE = "wykonane"


class Task:
    def __init__(self, title, description="", due_date=None, priority=Priority.MEDIUM, status=Status.PENDING):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority.value,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data):
        due_date = datetime.fromisoformat(data["due_date"]) if data["due_date"] else None
        return Task(
            title=data["title"],
            description=data["description"],
            due_date=due_date,
            priority=Priority(data["priority"]),
            status=Status(data["status"])
        )


class TaskRepository:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save()

    def remove_task(self, task: Task):
        self.tasks.remove(task)
        self.save()

    def mark_done(self, task: Task):
        task.status = Status.DONE
        self.save()

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            self.tasks = []
            return
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]

    def filter_tasks(self, priority=None, status=None, due_today=False):
        result = self.tasks
        if priority:
            result = [t for t in result if t.priority == priority]
        if status:
            result = [t for t in result if t.status == status]
        if due_today:
            today = datetime.now().date()
            result = [t for t in result if t.due_date and t.due_date.date() == today]
        return sorted(result, key=lambda t: (t.due_date or datetime.max))