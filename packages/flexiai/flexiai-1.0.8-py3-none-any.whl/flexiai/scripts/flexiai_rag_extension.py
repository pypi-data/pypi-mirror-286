# flexiai/scripts/flexiai_rag_extension.py
import os
from pathlib import Path

def _detect_project_root():
    """
    Detects the project root directory based on a known file or structure.

    Returns:
        str: The detected project root directory path.
    """
    current_dir = Path.cwd()
    project_root = current_dir
    return str(project_root)

def create_logs_folder(project_root):
    log_folder = os.path.join(project_root, 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
        print(f"Created directory: {log_folder}")

def create_user_flexiai_rag_folder(project_root):
    dst_folder = os.path.join(project_root, 'user_flexiai_rag')
    data_folder = os.path.join(dst_folder, 'data')
    
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created directory: {data_folder}")
    
    files_content = {
        '__init__.py': "# user_flexiai_rag/__init__.py\n",
        'user_function_mapping.py': (
            "# user_flexiai_rag/user_function_mapping.py\n"
            "import logging\n"
            "from user_flexiai_rag.user_task_manager import UserTaskManager\n\n"
            "logger = logging.getLogger(__name__)\n\n"
            "def register_user_tasks(multi_agent_system, run_manager):\n"
            "    \"\"\"\n"
            "    Registers user-defined tasks with the FlexiAI framework.\n\n"
            "    This function initializes the UserTaskManager and sets up mappings for personal and assistant functions.\n"
            "    It logs the registration process and returns the function mappings.\n\n"
            "    Args:\n"
            "        multi_agent_system (MultiAgentSystemManager): The multi-agent system manager instance.\n"
            "        run_manager (RunManager): The run manager instance.\n\n"
            "    Returns:\n"
            "        tuple: A tuple containing two dictionaries:\n"
            "            - user_personal_functions (dict): Mapping of personal function names to their implementations.\n"
            "            - user_assistant_functions (dict): Mapping of assistant function names to their implementations.\n"
            "    \"\"\"\n"
            "    task_manager = UserTaskManager(multi_agent_system, run_manager)\n\n"
            "    user_personal_functions = {\n"
            "        # MAS functions for each agent:\n"
            "        'save_processed_content': task_manager.save_processed_content,\n"
            "        'load_processed_content': task_manager.load_processed_content,\n"
            "        'initialize_agent': task_manager.initialize_agent,\n"
            "        # Functions used by your assistants\n"
            "        'search_youtube': task_manager.search_youtube,\n"
            "    }\n\n"
            "    user_assistant_functions = {\n"
            "       'communicate_with_assistant': task_manager.continue_conversation_with_assistant,\n"
            "       # Other designs for MAS or other assistants\n"
            "    }\n\n"
            "    logger.info(\"Registering user tasks\")\n"
            "    logger.debug(f\"User personal functions: {list(user_personal_functions.keys())}\")\n"
            "    logger.debug(f\"User assistant functions: {list(user_assistant_functions.keys())}\")\n\n"
            "    return user_personal_functions, user_assistant_functions\n"
        ),
        'user_helpers.py': "# user_flexiai_rag/user_helpers.py\n",
        'user_task_manager.py': (
            "# user_flexiai_rag/user_task_manager.py\n"
            "import logging\n"
            "import urllib.parse\n"
            "import subprocess\n"
            "from threading import Lock\n"
            "from flexiai.core.flexi_managers.run_manager import RunManager\n"
            "from flexiai.core.flexi_managers.thread_manager import ThreadManager\n"
            "from flexiai.core.flexi_managers.message_manager import MessageManager\n"
            "from flexiai.core.flexi_managers.multi_agent_system import MultiAgentSystemManager\n\n\n"
            "class UserTaskManager:\n"
            "    \"\"\"\n"
            "    UserTaskManager class handles user-defined tasks for AI assistants, enabling \n"
            "    Retrieval-Augmented Generation (RAG) capabilities and interaction within the \n"
            "    Multi-Agent System.\n\n"
            "    This class provides methods to save and load processed content, continue conversations \n"
            "    with assistants, initialize agents, and perform specific tasks such as YouTube searches.\n"
            "    \"\"\"\n\n"
            "    def __init__(self, multi_agent_system: MultiAgentSystemManager, run_manager: RunManager):\n"
            "        \"\"\"\n"
            "        Initializes the UserTaskManager instance, setting up the logger and a lock for thread safety.\n\n"
            "        Args:\n"
            "            multi_agent_system (MultiAgentSystemManager): The multi-agent system manager instance.\n"
            "            run_manager (RunManager): The run manager instance.\n"
            "        \"\"\"\n"
            "        self.logger = logging.getLogger(__name__)\n"
            "        self.lock = Lock()\n"
            "        self.multi_agent_system = multi_agent_system\n"
            "        self.run_manager = run_manager\n"
            "        self.message_manager = multi_agent_system.message_manager\n\n\n"
            "    def log_function_call(self, func_name, params=None):\n"
            "        \"\"\"\n"
            "        Logs the function call.\n"
            "        \n"
            "        Args:\n"
            "            func_name (str): The name of the function being called.\n"
            "            params (dict, optional): Parameters passed to the function.\n"
            "        \"\"\"\n"
            "        param_str = f\" with params: {params}\" if params else \"\"\n"
            "        self.logger.info(f\"Function called: {func_name}{param_str}\")\n\n\n"
            "    def save_processed_content(self, from_assistant_id, to_assistant_id, processed_content):\n"
            "        \"\"\"\n"
            "        Saves the processed user content for RAG purposes, allowing AI assistants to \n"
            "        store and retrieve contextual information.\n\n"
            "        Args:\n"
            "            from_assistant_id (str): The assistant identifier from which the content originates.\n"
            "            to_assistant_id (str): The assistant identifier to which the content is directed.\n"
            "            processed_content (str): The processed content to store.\n\n"
            "        Returns:\n"
            "            bool: True if content is saved successfully, False otherwise.\n"
            "        \"\"\"\n"
            "        return self.multi_agent_system.save_processed_content(from_assistant_id, to_assistant_id, processed_content)\n\n\n"
            "    def load_processed_content(self, from_assistant_id, to_assistant_id, multiple_retrieval):\n"
            "        \"\"\"\n"
            "        Loads the stored processed user content, enabling AI assistants to access \n"
            "        previously stored information for enhanced context and continuity in RAG.\n\n"
            "        Args:\n"
            "            from_assistant_id (str): The assistant identifier from which the content originates.\n"
            "            to_assistant_id (str): The assistant identifier to which the content is directed.\n"
            "            multiple_retrieval (bool): Whether to retrieve content from all sources, not just the specified to_assistant_id.\n\n"
            "        Returns:\n"
            "            list: A list of stored user content if found, otherwise an empty list.\n"
            "        \"\"\"\n"
            "        return self.multi_agent_system.load_processed_content(from_assistant_id, to_assistant_id, multiple_retrieval)\n\n\n"
            "    def continue_conversation_with_assistant(self, assistant_id, user_content):\n"
            "        \"\"\"\n"
            "        Continues the conversation with an assistant by submitting user content \n"
            "        and managing the resulting run, allowing dynamic and contextually aware interactions.\n\n"
            "        Args:\n"
            "            assistant_id (str): The unique identifier for the assistant.\n"
            "            user_content (str): The content submitted by the user.\n\n"
            "        Returns:\n"
            "            tuple: A tuple containing a success status, a message detailing the outcome, and the processed content.\n"
            "        \"\"\"\n"
            "        return self.multi_agent_system.continue_conversation_with_assistant(assistant_id, user_content)\n\n\n"
            "    def initialize_agent(self, assistant_id):\n"
            "        \"\"\"\n"
            "        Initializes an agent for the given assistant ID. If a thread already exists for the assistant ID,\n"
            "        it returns a message indicating the existing thread. Otherwise, it creates a new thread and returns\n"
            "        a message indicating successful initialization.\n\n"
            "        Args:\n"
            "            assistant_id (str): The unique identifier for the assistant.\n\n"
            "        Returns:\n"
            "            str: A message indicating the result of the initialization.\n"
            "        \"\"\"\n"
            "        return self.multi_agent_system.initialize_agent(assistant_id)\n\n\n"
            "    def search_youtube(self, query):\n"
            "        \"\"\"\n"
            "        Searches YouTube for the given query and opens the search results page\n"
            "        in the default web browser. This function demonstrates integration with \n"
            "        external services as part of RAG capabilities.\n\n"
            "        Args:\n"
            "            query (str): The search query string.\n\n"
            "        Returns:\n"
            "            dict: A dictionary containing the status, message, and result (URL)\n"
            "        \"\"\"\n"
            "        self.log_function_call('search_youtube', {'query': query})\n\n"
            "        if not query:\n"
            "            return {\n"
            "                \"status\": False,\n"
            "                \"message\": \"Query cannot be empty.\",\n"
            "                \"result\": None\n"
            "            }\n\n"
            "        try:\n"
            "            # Normalize spaces to ensure consistent encoding\n"
            "            query_normalized = query.replace(\" \", \"+\")\n"
            "            query_encoded = urllib.parse.quote(query_normalized)\n"
            "            youtube_search_url = (\n"
            "                f\"https://www.youtube.com/results?search_query={query_encoded}\"\n"
            "            )\n"
            "            self.logger.info(f\"Opening YouTube search for query: {query}\")\n\n"
            "            # Use PowerShell to open the URL\n"
            "            subprocess.run(\n"
            "                ['powershell.exe', '-Command', 'Start-Process', youtube_search_url],\n"
            "                check=True\n"
            "            )\n"
            "            self.logger.info(\"YouTube search page opened successfully.\")\n"
            "            return {\n"
            "                \"status\": True,\n"
            "                \"message\": \"YouTube search page opened successfully.\",\n"
            "                \"result\": youtube_search_url\n"
            "            }\n"
            "        except subprocess.CalledProcessError as e:\n"
            "            error_message = f\"Subprocess error: {str(e)}\"\n"
            "            self.logger.error(error_message, exc_info=True)\n"
            "            return {\n"
            "                \"status\": False,\n"
            "                \"message\": error_message,\n"
            "                \"result\": None\n"
            "            }\n"
            "        except Exception as e:\n"
            "            error_message = f\"Failed to open YouTube search for query: {query}. Error: {str(e)}\"\n"
            "            self.logger.error(error_message, exc_info=True)\n"
            "            return {\n"
            "                \"status\": False,\n"
            "                \"message\": error_message,\n"
            "                \"result\": None\n"
            "            }\n"
        ),
    }
    
    for filename, content in files_content.items():
        file_path = os.path.join(dst_folder, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Created file: {file_path}")

def create_env_file(project_root):
    env_file = os.path.join(project_root, '.env')
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(
                "# ============================================================================================ #\n"
                "#                                      OpenAI Configuration                                    #\n"
                "# ============================================================================================ #\n"
                "# Replace 'your_openai_api_key_here' with your actual OpenAI API key.\n"
                "OPENAI_API_KEY=your_openai_api_key_here\n\n"
                "# Replace 'your_openai_api_version_here' with your actual OpenAI API version.\n"
                "# Example for OpenAI: 2020-11-07\n"
                "OPENAI_API_VERSION=your_openai_api_version_here\n\n"
                "# Replace 'your_openai_organization_id_here' with your actual OpenAI Organization ID.\n"
                "OPENAI_ORGANIZATION_ID=your_openai_organization_id_here\n\n"
                "# Replace 'your_openai_project_id_here' with your actual OpenAI Project ID.\n"
                "OPENAI_PROJECT_ID=your_openai_project_id_here\n\n"
                "# Replace 'your_openai_assistant_version_here' with your actual OpenAI Assistant version.\n"
                "# Example for Assistant: v1 or v2\n"
                "OPENAI_ASSISTANT_VERSION=your_openai_assistant_version_here\n\n\n"
                "# ============================================================================================ #\n"
                "#                                      Azure OpenAI Configuration                              #\n"
                "# ============================================================================================ #\n"
                "# Replace 'your_azure_openai_api_key_here' with your actual Azure OpenAI API key.\n"
                "AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here\n\n"
                "# Replace 'your_azure_openai_endpoint_here' with your actual Azure OpenAI endpoint.\n"
                "AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here\n\n"
                "# Replace 'your_azure_openai_api_version_here' with your actual Azure OpenAI API version.\n"
                "# Example for Azure: 2024-05-01-preview\n"
                "AZURE_OPENAI_API_VERSION=your_azure_openai_api_version_here\n\n\n"
                "# ============================================================================================ #\n"
                "#                                      General Configuration                                   #\n"
                "# ============================================================================================ #\n"
                "# Set this to 'openai' if you are using OpenAI, or 'azure' if you are using Azure OpenAI.\n"
                "CREDENTIAL_TYPE=openai\n"
            )
        print(f"Created file: {env_file}")

def create_requirements_file(project_root):
    requirements_file = os.path.join(project_root, 'requirements.txt')
    if not os.path.exists(requirements_file):
        with open(requirements_file, 'w') as f:
            f.write(
                "annotated-types==0.7.0\n"
                "anyio==4.4.0\n"
                "azure-common==1.1.28\n"
                "azure-core==1.30.2\n"
                "azure-identity==1.17.1\n"
                "azure-mgmt-core==1.4.0\n"
                "azure-mgmt-resource==23.1.1\n"
                "blinker==1.8.2\n"
                "certifi==2024.7.4\n"
                "cffi==1.16.0\n"
                "charset-normalizer==3.3.2\n"
                "click==8.1.7\n"
                "cryptography==43.0.0\n"
                "distro==1.9.0\n"
                "Flask==3.0.3\n"
                "glob2==0.7\n"
                "h11==0.14.0\n"
                "httpcore==1.0.5\n"
                "httpx==0.27.0\n"
                "idna==3.7\n"
                "iniconfig==2.0.0\n"
                "isodate==0.6.1\n"
                "itsdangerous==2.2.0\n"
                "Jinja2==3.1.4\n"
                "MarkupSafe==2.1.5\n"
                "msal==1.30.0\n"
                "msal-extensions==1.2.0\n"
                "nest-asyncio==1.6.0\n"
                "openai==1.35.0\n"
                "packaging==24.1\n"
                "platformdirs==3.7.0\n"
                "pluggy==1.5.0\n"
                "portalocker==2.10.1\n"
                "pycparser==2.22\n"
                "pydantic==2.7.4\n"
                "pydantic-settings==2.3.3\n"
                "pydantic_core==2.18.4\n"
                "PyJWT==2.8.0\n"
                "pytest==8.3.1\n"
                "python-dotenv==1.0.1\n"
                "requests==2.32.3\n"
                "six==1.16.0\n"
                "sniffio==1.3.1\n"
                "tqdm==4.66.4\n"
                "typing_extensions==4.12.2\n"
                "urllib3==2.2.2\n"
                "Werkzeug==3.0.3\n"
            )
        print(f"Created file: {requirements_file}")

def setup_project():
    project_root = _detect_project_root()
    create_logs_folder(project_root)
    create_user_flexiai_rag_folder(project_root)
    create_env_file(project_root)
    create_requirements_file(project_root)

if __name__ == '__main__':
    setup_project()
