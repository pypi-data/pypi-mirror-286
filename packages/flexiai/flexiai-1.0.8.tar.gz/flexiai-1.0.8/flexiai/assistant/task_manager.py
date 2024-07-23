# flexiai/assistant/task_manager.py
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from flexiai.assistant.function_mapping import FunctionMapping

class TaskManager:
    """
    TaskManager class handles the execution and management of tasks within the FlexiAI framework,
    including both predefined tasks and user-defined tasks. It utilizes asynchronous and synchronous
    execution to manage and run tasks efficiently, providing a flexible and extensible system for
    task management.

    Attributes:
        logger (logging.Logger): Logger for logging information and errors.
        function_mapper (FunctionMapping): Instance for mapping and registering functions.
        executor (ThreadPoolExecutor): Thread pool executor for concurrent task execution.
        personal_function_mapping (dict): Mapping of personal functions defined by the user.
        assistant_function_mapping (dict): Mapping of assistant functions defined by the user.
    """

    def __init__(self, max_workers=10):
        """
        Initializes the TaskManager instance, setting up the logger and user-defined tasks.
        Configures the ThreadPoolExecutor for managing concurrent task execution.

        Args:
            max_workers (int): The maximum number of worker threads for executing tasks concurrently.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing TaskManager")
        self.function_mapper = FunctionMapping()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.personal_function_mapping = {}
        self.assistant_function_mapping = {}

    async def run_task_async(self, func, *args, **kwargs):
        """
        Runs a given task asynchronously using the ThreadPoolExecutor.

        Args:
            func (callable): The function to execute.
            *args: Variable length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.

        Returns:
            Any: The result of the executed function.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, func, *args, **kwargs)

    def run_task(self, func, *args, **kwargs):
        """
        Runs a given task synchronously using the ThreadPoolExecutor.

        Args:
            func (callable): The function to execute.
            *args: Variable length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.

        Returns:
            Any: The result of the executed function.
        """
        future = self.executor.submit(func, *args, **kwargs)
        return future.result()

    def load_user_tasks(self, multi_agent_system, run_manager):
        """
        Loads user-defined tasks into the TaskManager, mapping them for personal and assistant use.
        Registers user functions from the FunctionMapping instance and updates the function mappings.

        Args:
            multi_agent_system (MultiAgentSystemManager): The multi-agent system manager instance.
            run_manager (RunManager): The run manager instance.

        Raises:
            Exception: If loading user-defined tasks fails.
        """
        try:
            self.function_mapper.register_user_functions(multi_agent_system, run_manager)
            self.personal_function_mapping = self.function_mapper.personal_function_mapping
            self.assistant_function_mapping = self.function_mapper.assistant_function_mapping
            self.logger.info("User-defined tasks loaded successfully")
            self.logger.info(f"Assistant function mapping: {self.assistant_function_mapping}")
            self.logger.info(f"Personal function mapping: {self.personal_function_mapping}")
        except Exception as e:
            self.logger.error(f"Failed to load user-defined tasks: {str(e)}", exc_info=True)
            raise e
