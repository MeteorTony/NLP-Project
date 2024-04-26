import autogen      # "pip install pyautogen" first
import os

# TODO: just temporary, not working
key = "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"

config_list = [{"model": "gpt-4", "api_key": key}]

llm_config = {
    "config_list": config_list,
    "cache_seed": 41,  # seed for caching and reproducibility
    "temperature": 0.5,  # temperature for sampling

}

executor = autogen.AssistantAgent(
    name="executor",
    system_message="""
   You love telling jokes. After Alice feedback improve 
   the joke. Say 'TERMINATE' when you have improved the joke.
""",
    llm_config=llm_config,
)

observer = autogen.AssistantAgent(
    name="observer",
    system_message="""
   You should make sure the joke created by the executor is funny enough.
""",
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",       # Never ask for human input
    max_consecutive_auto_reply=10,
    system_message="A human admin.",
    is_termination_msg=lambda msg: msg.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },
)

groupchat = autogen.GroupChat(agents=[user_proxy, observer, executor], messages=[], max_round=6)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
#
# assistant receives a message from user_proxy (contains task description)
chat_res = user_proxy.initiate_chat(
    manager,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
    summary_method="reflection_with_llm",
    max_turns=6,
)

print("Chat history:", chat_res.chat_history)

print("Summary:", chat_res.summary)
print("Cost info:", chat_res.cost)
