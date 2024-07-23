# flexiai/assistant/__init__.py
from flexiai.assistant.task_manager import TaskManager

# Initialize TaskManager
task_manager = TaskManager()

__all__ = [
    'TaskManager',
    'task_manager',
]
