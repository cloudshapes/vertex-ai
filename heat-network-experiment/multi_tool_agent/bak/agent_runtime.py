# agent_runtime.py

from vertexai import init
from vertexai.generative_models import GenerativeModel, ChatSession
from heat_news_agent.agent import root_agent  # from our simplified agent.py

# Step 1: Initialize Vertex AI
init(
    project="gemini-agent-lab",
    location="us-central1"  # adjust if you're using a different region
)

# Step 2: Load Gemini model with system instruction + tool
model = GenerativeModel(
    model_name=root_agent["model"],
    system_instruction=root_agent["instruction"],
    tools=root_agent["tools"]
)

# Step 3: Start a chat session
chat: ChatSession = model.start_chat()

# Step 4: Define helper to call the agent
def call_agent(prompt: str):
    response = chat.send_message(prompt)
    print("\n🤖 Agent:\n" + response.text.strip())

# Step 5: CLI loop
if __name__ == "__main__":
    print("🧠 Gemini Agent CLI — Ask me about heat networks, mine water geothermal, or district heating.")
    while True:
        user_input = input("\n🧍 You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        call_agent(user_input)


