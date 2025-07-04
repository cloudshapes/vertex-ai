# agent.py

from vertexai.generative_models.tools import FunctionTool
import requests
from google.cloud import secretmanager

# 🔐 Helper to fetch API key securely
def get_secret(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project_id = "gemini-agent-lab"
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


# 🔎 Core tool function
def get_latest_news(topic: str) -> dict:
    """Fetch recent news about low carbon heating.

    Args:
        topic (str): Search topic, e.g. 'district heating'

    Returns:
        dict: Dictionary with articles or error message.
    """
    api_key = get_secret("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=5&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "error_message": f"Failed to fetch articles: {response.text}"}

    articles = response.json().get("articles", [])
    if not articles:
        return {"status": "success", "report": f"No articles found for '{topic}'."}

    entries = [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"]
        } for a in articles
    ]

    return {"status": "success", "report": entries}


# 🛠 Register tool using Vertex AI's FunctionTool
latest_news_tool = FunctionTool(get_latest_news)

# 🧠 Agent configuration (dict instead of ADK Agent class)
root_agent = {
    "name": "heat_news_agent",
    "model": "gemini-2.5-flash",
    "instruction": (
        "You are an expert on low carbon heating systems. "
        "When the user asks about district heating, mine water geothermal, or heat networks, "
        "use the `get_latest_news` tool. "
        "Summarize the results with titles and clickable links. Avoid off-topic results."
    ),
    "tools": [latest_news_tool]
}


