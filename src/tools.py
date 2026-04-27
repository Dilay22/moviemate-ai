import os
from tavily import TavilyClient


def search_web(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key or api_key == "your_tavily_api_key_here":
        return "Web search unavailable: TAVILY_API_KEY is missing or invalid."

    client = TavilyClient(api_key=api_key)

    search_query = (
        query
        + " site:imdb.com OR site:rottentomatoes.com OR site:metacritic.com "
        + "rating reviews runtime"
    )

    results = client.search(
        query=search_query,
        max_results=6,
        search_depth="advanced",
        include_answer=True
    )

    formatted_results = []

    answer = results.get("answer")
    if answer:
        formatted_results.append(f"Search answer summary: {answer}")

    for item in results.get("results", []):
        title = item.get("title", "No title")
        url = item.get("url", "No URL")
        content = item.get("content", "No content")

        formatted_results.append(
            f"Title: {title}\nURL: {url}\nSummary: {content}"
        )

    if not formatted_results:
        return "Web search ran, but no useful results were returned."

    return "\n\n".join(formatted_results)