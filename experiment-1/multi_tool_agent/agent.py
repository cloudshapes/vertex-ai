from google.adk.agents import Agent

import requests

def get_latest_news(topic: str) -> dict:
    """Returns recent news articles about a given topic."""
    api_key = "238d94566ef74956b67c0756f3579e88"  # Secure via env var ideally
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=5&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "error_message": f"Failed to fetch articles: {response.text}"}

    articles = response.json().get("articles", [])
    if not articles:
        return {"status": "success", "report": f"No articles found for {topic}."}

    summaries = [
        f"{a['title']} ({a['source']['name']}) - {a['url']}" for a in articles
    ]

    return {"status": "success", "report": "\n".join(summaries)}

root_agent = Agent(
    name="heat_news_agent",
    model="gemini-2.0-flash",
    description="Agent that provides updates on low carbon heating and district energy systems.",
    instruction="I can find you recent news about heat networks, district heating, and geothermal energy.",
    tools=[get_latest_news]
) 
