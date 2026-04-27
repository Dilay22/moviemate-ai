import os
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from rag import build_retriever
from tools import search_web
from prompts import RECOMMENDATION_PROMPT


class MovieState(TypedDict):
    user_query: str
    rag_context: str
    needs_web_search: bool
    web_results: str
    web_search_used: str
    final_answer: str


llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("GITHUB_TOKEN"),
    base_url=os.getenv("BASE_URL")
)

retriever = build_retriever()


def retrieve_movie_guides(state: MovieState) -> MovieState:
    print("📚 Using RAG: retrieving movie guides...")
    docs = retriever.invoke(state["user_query"])

    rag_context = "\n\n".join(doc.page_content for doc in docs)

    print("📄 Retrieved documents:")
    for doc in docs:
        print("-", doc.metadata.get("source", "Unknown source"))

    state["rag_context"] = rag_context
    return state


def decide_web_search(state: MovieState) -> MovieState:
    query = state["user_query"].lower()

    web_keywords = [
        "current",
        "recent",
        "latest",
        "trending",
        "rating",
        "ratings",
        "review",
        "reviews",
        "new",
        "available",
        "availability",
        "streaming",
        "netflix",
        "disney",
        "hbo",
        "prime",
        "imdb",
        "rotten tomatoes"
    ]

    state["needs_web_search"] = any(word in query for word in web_keywords)

    if state["needs_web_search"]:
        print("🌐 Web search needed based on user query.")
    else:
        print("✅ Web search not needed. Using RAG only.")

    return state


def route_web_search(state: MovieState) -> str:
    if state["needs_web_search"]:
        return "web_search_movies"

    return "generate_recommendations"

def web_search_movies(state: MovieState) -> MovieState:
    print("🔎 Running web search...")
    results = search_web(state["user_query"])

    state["web_results"] = results

    if "unavailable" in results.lower() or "missing" in results.lower():
        state["web_search_used"] = (
            "Web search was needed, but it was unavailable because "
            "the Tavily API key is missing or invalid."
        )
    else:
        state["web_search_used"] = "Yes, web search was used."
        print("🌐 Web search returned results:")
        preview = results.split("\n\n")[:3]
        for item in preview:
            first_line = item.split("\n")[0]
            print("-", first_line)

    return state



def generate_recommendations(state: MovieState) -> MovieState:
    prompt = ChatPromptTemplate.from_template(RECOMMENDATION_PROMPT)
    chain = prompt | llm

    response = chain.invoke({
        "user_query": state["user_query"],
        "rag_context": state["rag_context"],
        "web_results": state.get("web_results", "No web search used."),
        "web_search_used": state.get("web_search_used", "No, web search was not used.")
    })

    state["final_answer"] = response.content
    return state


def build_graph():
    graph = StateGraph(MovieState)

    graph.add_node("retrieve_movie_guides", retrieve_movie_guides)
    graph.add_node("decide_web_search", decide_web_search)
    graph.add_node("web_search_movies", web_search_movies)
    graph.add_node("generate_recommendations", generate_recommendations)

    graph.set_entry_point("retrieve_movie_guides")

    graph.add_edge("retrieve_movie_guides", "decide_web_search")

    graph.add_conditional_edges(
        "decide_web_search",
        route_web_search,
        {
            "web_search_movies": "web_search_movies",
            "generate_recommendations": "generate_recommendations"
        }
    )

    graph.add_edge("web_search_movies", "generate_recommendations")
    graph.add_edge("generate_recommendations", END)

    return graph.compile()