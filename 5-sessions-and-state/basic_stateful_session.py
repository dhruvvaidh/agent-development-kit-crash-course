import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# Sessions are basically stateful chat histories for the application
# There are 3 types of sessions in ADK:
# 1. InMemorySessionService: All the coversation we have with our agent are stored in this one, when we close the application, we will lose all the conversations.
# 2. DatabaseSessionService: Every conversation with the agent is stored in a database, if we want to pickup from where we left, this is the way to go
# 3. VertexAISessionService: If we want to save the session onto the cloud

# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Dhruv Vaidh",
    "user_preferences": """
        I like to watch Football, Cricket, and Formula One.
        My favorite food is Indian.
        My favorite TV show is Brooklyn Nine-Nine.
        Loves it when people like and subscribe to his YouTube channel.
    """,
}

# Create a NEW session
# App name and User ID is compulsory, Providing the state is not although, it is advisable to create the state to provide the Agent with somee more context
APP_NAME = "Dhruv Bot"
USER_ID = "dhruv_vaidh"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

# Runner is defined for every application. 
# It consists of Agents and Session which are used to provide the user with an intelligent answer. 
# When a Runner gets a request from the user, it will have it's selection of agents to choose from. 
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

# When we have to create a message to be passed to the Agent, we use types.Content
new_message = types.Content(
    role="user", parts=[types.Part(text="What is Dhruv's favorite TV show?")]
)

# Every message is registered as an event in the session database, every event is being run by the runner
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")



# When we are creating our own application, we will have to manage the memory, sessions and runners therefore this script is important