import autogen      # "pip install pyautogen" first
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config_list = [
  {
    "model": "gpt-35-turbo",
    "api_type": "azure",
    "api_key": os.getenv("API_KEY"),
    "base_url": "https://hkust.azure-api.net",
    "api_version": "2023-05-15"
  }
]

llm_config = {
    "config_list": config_list,
    "cache_seed": 41,  # seed for caching and reproducibility
    "temperature": 0.5,  # temperature for sampling
}

# executor agent
executor = autogen.AssistantAgent(
    name="executor",
    system_message="""Your role as an Executor Agent involves implementing algorithms, performing computations, 
    and executing automated actions within the system. Your responsibilities include task execution, algorithmic 
    processing, resource management, error handling, and effective communication with other agents. Your efficient 
    task execution and accurate results contribute to the overall success of our multi-agent system. """,
    llm_config=llm_config,
    code_execution_config={
        "use_docker": False,
    },
)

# observer agent
observer = autogen.AssistantAgent(
    name="observer",
    system_message="""As an Observer Agent, you are responsible for observing, analyzing, and reporting on various 
    aspects of the system and its interactions. Your main responsibilities include system monitoring, 
    data collection, and analysis the responses from the executor agent. By identifying potential issues, anomalies, 
    and patterns, you help maintain system stability and performance.""",
    llm_config=llm_config,
)

# user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",       # Never ask for human input
    system_message="A human admin.",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "use_docker": False,
    },
)

# 3 group member agents and 1 manager agent
groupChat = autogen.GroupChat(agents=[user_proxy, observer, executor], messages=[], max_round=4)

# group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupChat,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
)

chat_res = user_proxy.initiate_chat(
    manager,
    message="""Find a latest paper about gpt-4 on arxiv and find its potential applications in software.""",
    summary_method="reflection_with_llm",
)

print("Chat history:", chat_res.chat_history)
print("Summary:", chat_res.summary)
print("Cost info:", chat_res.cost)
