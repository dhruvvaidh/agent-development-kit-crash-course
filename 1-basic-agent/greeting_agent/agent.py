from google.adk.agents import Agent


# We need to have a root agent, as it serves as the entry point to the application
# We need to ensure that the root agent name is same as the directory name

root_agent = Agent(
    name="greeting_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """,
)
