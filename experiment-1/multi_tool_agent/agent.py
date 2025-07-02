from google.adk.agents import Agent
from google.cloud import secretmanager

import requests

def get_secret(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project_id = "verdant-art-463815-h7"
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def get_latest_news(topic: str) -> dict:
    """Returns recent news articles about a given topic."""
    api_key = get_secret("NEWSAPI_KEY")
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=5&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "error_message": f"Failed to fetch articles: {response.text}"}

    articles = response.json().get("articles", [])
    if not articles:
        return {"status": "success", "report": f"No articles found for {topic}."}

    entries = [
        {
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"]
        } for a in articles
    ]

    return {"status": "success", "report": entries}


root_agent = Agent(
    name="heat_news_agent",
    model="gemini-2.0-flash",
    description="Agent that provides updates on low carbon heating and district energy systems.",
    instruction=(
        "You are an expert assistant focused on low carbon heating technologies. "
        "When the user asks about heat networks, district heating, mine water geothermal, or related topics, "
        "use the `get_latest_news` tool to return only relevant articles. "
        "Summarise the results clearly as a bulleted list with titles and clickable links. "
        "Avoid unrelated or off-topic articles. Keep your response factual and up to date."
    ),
    tools=[get_latest_news]
) 
