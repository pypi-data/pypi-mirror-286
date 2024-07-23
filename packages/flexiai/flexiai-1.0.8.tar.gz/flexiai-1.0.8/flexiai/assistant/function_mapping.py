# flexiai/assistant/function_mapping.py
import importlib
import logging
import os
import sys
import glob
from pathlib import Path

logger = logging.getLogger(__name__)

class FunctionMapping:
    """
    Class to handle the function mappings for personal and assistant functions,
    including both internal and user-defined functions.
    """

    def __init__(self):
        """
        Initializes the FunctionMapping instance, automatically detecting the path to user-defined functions.
        """
        self.user_directory = self._detect_user_directory()
        self.personal_function_mapping = {}
        self.assistant_function_mapping = {}
        logger.info(f"User directory detected: {self.user_directory}")

    def _detect_user_directory(self):
        """
        Detects the user directory path where user-defined functions are stored.

        Returns:
            str: The detected user directory path.
        """
        # Detect the current working directory
        current_dir = Path.cwd()
        # Determine the project root directory based on a known file or structure
        project_root = current_dir
        user_directory = project_root / 'user_flexiai_rag'

        if not user_directory.is_dir():
            raise FileNotFoundError(f"User directory {user_directory} not found")
        return str(user_directory)

    def register_user_functions(self, multi_agent_system, run_manager):
        """
        Register user-defined functions by merging them with existing function mappings.

        Args:
            multi_agent_system (MultiAgentThreadsManager): The multi-agent threads manager instance.
            run_manager (RunManager): The run manager instance.
        """
        try:
            user_modules = self._load_user_modules()
            for module in user_modules:
                if hasattr(module, 'register_user_tasks'):
                    user_personal_functions, user_assistant_functions = module.register_user_tasks(multi_agent_system, run_manager)
                    self.personal_function_mapping.update(user_personal_functions)
                    self.assistant_function_mapping.update(user_assistant_functions)
                    logger.info(f"Successfully registered user functions from {module.__name__}")
                    logger.debug(f"Updated personal functions: {list(self.personal_function_mapping.keys())}")
                    logger.debug(f"Updated assistant functions: {list(self.assistant_function_mapping.keys())}")

        except Exception as e:
            logger.error(f"Failed to register user functions: {e}", exc_info=True)
            raise

    def _load_user_modules(self):
        """
        Load user modules dynamically from the user directory.

        Returns:
            list: A list of loaded user modules.
        """
        sys.path.insert(0, self.user_directory)
        module_files = glob.glob(os.path.join(self.user_directory, "*.py"))
        modules = []
        for module_file in module_files:
            module_name = os.path.splitext(os.path.basename(module_file))[0]
            if module_name != "__init__":
                try:
                    module = importlib.import_module(module_name)
                    modules.append(module)
                    logger.info(f"Attempting to import module: {module_name}")
                except ImportError as e:
                    logger.warning(f"Failed to import module {module_name}: {e}")
        return modules
