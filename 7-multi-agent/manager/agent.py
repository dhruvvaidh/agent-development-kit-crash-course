from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time


# The manager Agent basically reads through the descriptions of all the other agents 
# to figure out which one should be selected to perform the Task

# Agents in ADK work in a different way, instead of using multiple agents to do one task, 
# it focuses on delegating the task to the best agent possible. 
# There are workarounds to this for adding complex workflows like parallel, sequential and loops.

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)

# We cannot use subagents with built-in tools with the root agent. 
# Therefore, we have to use AgentTool class to use the Sub agent as a tool call for thr root agent

# Agent-as-a-Tool: When Agent A calls Agent B as a tool (using Agent-as-a-Tool),
# Agent B's answer is passed back to Agent A, which then summarizes the answer
# and generates a response to the user. Agent A retains control and continues
# to handle future user input.

# We should add the following to the subagent instructions for better performance. 
# "If you are not able to fulfill the request by user, delegate it to the root agent"