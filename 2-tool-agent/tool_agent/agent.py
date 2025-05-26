from google.adk.agents import Agent
from google.adk.tools import google_search


# When using tools, return the result as a json string for easier use
# Setting Default values doesn't work in ADK tools
# def get_current_time() -> dict:
#     """
#     Get the current time in the format YYYY-MM-DD HH:MM:SS
#     """
#     return {
#         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

# ADK Built In Tools only work with Google Models, 
# if we need to use others we will have to use LangChain or CrewAI

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search],
    # tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
)


# We can only use one built-in tool at a time. we cannot use more

# For some weird reason, when we use built in with custom tools in ADK, it breaks, (need to test this once)
# tools=[google_search, get_current_time], # <--- Doesn't work