# flexiai/__init__.py
from flexiai.assistant.task_manager import TaskManager
from flexiai.config.config import Config
from flexiai.core.flexiai_client import FlexiAI

# Initialize TaskManager
task_manager = TaskManager()

__all__ = [
    'TaskManager',
    'task_manager',
    'Config',
    'FlexiAI'
]
