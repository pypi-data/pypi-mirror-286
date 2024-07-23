# flexiai/core/flexiai_client.py
import logging
from flexiai.assistant.task_manager import TaskManager
from flexiai.credentials.credential_manager import CredentialManager
from flexiai.core.flexi_managers.message_manager import MessageManager
from flexiai.core.flexi_managers.run_manager import RunManager
from flexiai.core.flexi_managers.session_manager import SessionManager
from flexiai.core.flexi_managers.thread_manager import ThreadManager
from flexiai.core.flexi_managers.vector_store_manager import VectorStoreManager
from flexiai.core.flexi_managers.multi_agent_system import MultiAgentSystemManager


class FlexiAI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.credential_manager = CredentialManager()
        self.client = self.credential_manager.client

        # Initialize TaskManager and load user-defined tasks
        self.task_manager = TaskManager()
        
        # Initialize other managers
        self.thread_manager = ThreadManager(self.client, self.logger)
        self.message_manager = MessageManager(self.client, self.logger, {}, {})
        self.run_manager = RunManager(self.client, self.logger, {}, {}, self.message_manager)
        
        # Initialize MultiAgentSystemManager
        self.multi_agent_system = MultiAgentSystemManager(
            self.client, self.logger, self.thread_manager, self.run_manager, self.message_manager
        )
        
        # Load user tasks after initializing all managers to ensure proper registration
        self.task_manager.load_user_tasks(self.multi_agent_system, self.run_manager)
        
        # Update function mappings after loading user tasks
        self.personal_function_mapping = self.task_manager.personal_function_mapping
        self.assistant_function_mapping = self.task_manager.assistant_function_mapping
        
        # Update the function mappings in run_manager and message_manager
        self.run_manager.personal_function_mapping = self.personal_function_mapping
        self.run_manager.assistant_function_mapping = self.assistant_function_mapping
        self.message_manager.personal_function_mapping = self.personal_function_mapping
        self.message_manager.assistant_function_mapping = self.assistant_function_mapping
        
        # Reinitialize run_manager and message_manager with updated mappings
        self.run_manager = RunManager(self.client, self.logger, self.personal_function_mapping, self.assistant_function_mapping, self.message_manager)
        self.message_manager = MessageManager(self.client, self.logger, self.personal_function_mapping, self.assistant_function_mapping)
        
        self.session_manager = SessionManager(self.client, self.logger)
        self.vector_store_manager = VectorStoreManager(self.client, self.logger)


    def create_thread(self):
        """
        Creates a new thread using the ThreadManager.

        Returns:
            str: The ID of the newly created thread.
        """
        return self.thread_manager.create_thread()


    def retrieve_thread(self, thread_id):
        """
        Retrieves details of a specific thread by its ID using the ThreadManager.

        Args:
            thread_id (str): The ID of the thread to retrieve.

        Returns:
            object: The thread object.
        """
        return self.thread_manager.retrieve_thread(thread_id)


    def update_thread(self, thread_id, metadata=None, tool_resources=None):
        """
        Updates a thread with the given details using the ThreadManager.

        Args:
            thread_id (str): The ID of the thread to update.
            metadata (dict, optional): Metadata to update for the thread.
            tool_resources (dict, optional): Tool resources to update for the thread.

        Returns:
            object: The updated thread object.
        """
        return self.thread_manager.update_thread(thread_id, metadata, tool_resources)


    def delete_thread(self, thread_id):
        """
        Deletes a thread by its ID using the ThreadManager.

        Args:
            thread_id (str): The ID of the thread to delete.

        Returns:
            bool: True if the thread was deleted successfully, False otherwise.
        """
        return self.thread_manager.delete_thread(thread_id)


    def attach_assistant_to_thread(self, assistant_id, thread_id):
        """
        Attaches an assistant to an existing thread using the ThreadManager.

        Args:
            assistant_id (str): The ID of the assistant.
            thread_id (str): The ID of the thread.

        Returns:
            object: The run object indicating the assistant has been attached.
        """
        return self.thread_manager.attach_assistant_to_thread(assistant_id, thread_id)

    
    def add_user_message(self, thread_id, user_message):
        """
        Adds a user message to a specified thread using the MessageManager.

        Args:
            thread_id (str): The ID of the thread.
            user_message (str): The content of the user's message.

        Returns:
            object: The message object that was added to the thread.
        """
        return self.message_manager.add_user_message(thread_id, user_message)


    def wait_for_run_completion(self, thread_id):
        """
        Waits for the completion of a run on a specified thread using the RunManager.

        Args:
            thread_id (str): The ID of the thread to wait for run completion.
        """
        self.run_manager.wait_for_run_completion(thread_id)


    def create_run(self, assistant_id, thread_id):
        """
        Creates a new run for a specified assistant and thread using the RunManager.

        Args:
            assistant_id (str): The ID of the assistant.
            thread_id (str): The ID of the thread.

        Returns:
            object: The run object if successful, None otherwise.
        """
        return self.run_manager.create_run(assistant_id, thread_id)


    def create_advanced_run(self, assistant_id, thread_id, user_message):
        """
        Creates an advanced run with a user message for a specified assistant and thread using the RunManager.

        Args:
            assistant_id (str): The ID of the assistant.
            thread_id (str): The ID of the thread.
            user_message (str): The user's message content.

        Returns:
            object: The run object if successful, None otherwise.
        """
        return self.run_manager.create_advanced_run(assistant_id, thread_id, user_message)

    
    def create_and_monitor_run(self, assistant_id, thread_id, user_message=None, role=None, metadata=None):
        """
        Creates and runs a thread with the specified assistant, optionally adding a user message,
        and monitors its status until completion or failure using the RunManager.

        Args:
            assistant_id (str): The ID of the assistant.
            thread_id (str): The ID of the thread.
            user_message (str, optional): The user's message content to add before creating the run.
            role (str, optional): The role of the message sender. Defaults to 'user'.
            metadata (dict, optional): Metadata to include with the message.

        Returns:
            None
        """
        return self.run_manager.create_and_monitor_run(assistant_id, thread_id, user_message, role, metadata)


    def retrieve_messages(self, thread_id, order='desc', limit=20):
        """
        Retrieves messages from a specified thread using the MessageManager.

        Args:
            thread_id (str): The ID of the thread.
            order (str, optional): The order in which to retrieve messages, either 'asc' or 'desc'. Defaults to 'desc'.
            limit (int, optional): The number of messages to retrieve. Defaults to 20.

        Returns:
            list: A list of dictionaries containing the message ID, role, and content of each message.
        """
        return self.message_manager.retrieve_messages(thread_id, order, limit)


    def retrieve_message_object(self, thread_id, order='asc', limit=20):
        """
        Retrieves message objects from a specified thread using the MessageManager.

        Args:
            thread_id (str): The ID of the thread.
            order (str, optional): The order in which to retrieve messages, either 'asc' or 'desc'. Defaults to 'asc'.
            limit (int, optional): The number of messages to retrieve. Defaults to 20.

        Returns:
            list: A list of message objects.
        """
        return self.message_manager.retrieve_message_object(thread_id, order, limit)

    
    def process_and_print_messages(self, messages):
        """
        Processes and prints the role and content of each message using the MessageManager.

        Args:
            messages (list): The list of message objects.
        """
        self.message_manager.process_and_print_messages(messages)
        
        
    def assistant_transformer(self, thread_id, new_assistant_id):
        """
        Attaches a new assistant to an existing thread and runs the thread to speak with the new assistant using the RunManager.

        Args:
            thread_id (str): The ID of the existing thread.
            new_assistant_id (str): The ID of the new assistant to attach.

        Returns:
            object: The final run object indicating the result of the interaction.
        """
        return self.run_manager.assistant_transformer(thread_id, new_assistant_id)


    def create_vector_store(self, name):
        """
        Creates a new vector store with a specified name using the VectorStoreManager.

        Args:
            name (str): The name of the vector store.

        Returns:
            object: The newly created vector store object.
        """
        return self.vector_store_manager.create_vector_store(name)


    def upload_files_and_poll(self, vector_store_id, file_paths):
        """
        Uploads files to a vector store and polls the status of the file batch for completion using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.
            file_paths (list): A list of file paths to upload.

        Returns:
            object: The file batch object after upload and completion.
        """
        return self.vector_store_manager.upload_files_and_poll(vector_store_id, file_paths)


    def update_assistant_with_vector_store(self, assistant_id, vector_store_id):
        """
        Updates an assistant to use the new vector store using the VectorStoreManager.

        Args:
            assistant_id (str): The ID of the assistant.
            vector_store_id (str): The ID of the vector store.

        Returns:
            object: The updated assistant object.
        """
        return self.vector_store_manager.update_assistant_with_vector_store(assistant_id, vector_store_id)


    def list_vector_stores(self):
        """
        Retrieves a list of all existing vector stores using the VectorStoreManager.

        Returns:
            list: A list of vector store objects.
        """
        return self.vector_store_manager.list_vector_stores()


    def retrieve_vector_store_details(self, vector_store_id):
        """
        Retrieves detailed information about a specific vector store using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.

        Returns:
            object: The vector store object with detailed information.
        """
        return self.vector_store_manager.retrieve_vector_store_details(vector_store_id)


    def delete_vector_store(self, vector_store_id):
        """
        Deletes a vector store using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.

        Returns:
            bool: True if the vector store was deleted successfully, False otherwise.
        """
        return self.vector_store_manager.delete_vector_store(vector_store_id)


    def list_files_in_vector_store(self, vector_store_id, batch_id):
        """
        Lists all files that have been uploaded to a specific vector store using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.
            batch_id (str): The ID of the file batch.

        Returns:
            list: A list of files in the vector store.
        """
        return self.vector_store_manager.list_files_in_vector_store(vector_store_id, batch_id)


    def retrieve_file_batch_details(self, vector_store_id, batch_id):
        """
        Retrieves the status and details of a specific file batch within a vector store using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.
            batch_id (str): The ID of the file batch.

        Returns:
            object: The file batch object with detailed information.
        """
        return self.vector_store_manager.retrieve_file_batch_details(vector_store_id, batch_id)


    def search_files_in_vector_store(self, vector_store_id, query):
        """
        Searches for files in a vector store based on a query using the VectorStoreManager.

        Args:
            vector_store_id (str): The ID of the vector store.
            query (str): The search query.

        Returns:
            list: A list of search results.
        """
        return self.vector_store_manager.search_files_in_vector_store(vector_store_id, query)


    def call_parallel_functions(self, tasks):
        """
        Wrapper to run parallel tool calls in an asynchronous event loop.

        Args:
            tasks (list): A list of dictionaries where each dictionary contains:
                - function_name (str): The name of the function to call.
                - parameters (dict): The parameters to pass to the function.

        Returns:
            list: A list of results from each function call.
        """
        return self.run_manager.call_parallel_functions(tasks)


    def add_messages_dynamically(self, thread_id, messages, role=None, metadata=None):
        """
        Adds multiple user messages to a specified thread dynamically with optional metadata.

        Args:
            thread_id (str): The ID of the thread.
            messages (list): A list of dictionaries containing the message content and optional metadata. 
                            Each dictionary should have the following structure:
                            {
                                "content": "Message content",
                                "metadata": {"key": "value"} (optional)
                            }
            role (str, optional): The role of the message sender. Defaults to None.
            metadata (dict, optional): Default metadata to include with each message if not provided in individual messages.

        Returns:
            list: A list of message objects that were added to the thread.

        Raises:
            OpenAIError: If the API call to add a message fails.
            Exception: If an unexpected error occurs.
        """
        return self.message_manager.add_messages_dynamically(thread_id, messages, role=role, metadata=metadata)


    def retrieve_messages_dynamically(self, thread_id, order='asc', limit=20, retrieve_all=False, last_retrieved_id=None):
        """
        Retrieves messages from a specified thread dynamically.

        Args:
            thread_id (str): The ID of the thread from which to retrieve messages.
            order (str, optional): The order in which to retrieve messages, either 'asc' or 'desc'. Defaults to 'asc'.
            limit (int, optional): The maximum number of messages to retrieve in a single request. Defaults to 20.
            retrieve_all (bool, optional): Whether to retrieve all messages in the thread. If False, only retrieves up to the limit. Defaults to False.
            last_retrieved_id (str, optional): The ID of the last retrieved message to fetch messages after it. Defaults to None.

        Returns:
            list: A list of message objects retrieved from the thread.

        Raises:
            OpenAIError: If the API call to retrieve messages fails.
            Exception: If an unexpected error occurs.
        """
        return self.message_manager.retrieve_messages_dynamically(thread_id, order, limit, retrieve_all, last_retrieved_id)
