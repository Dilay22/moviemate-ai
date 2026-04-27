from dotenv import load_dotenv

# Load environment variables before importing graph.py
# because graph.py uses the API keys when it creates the LLM.
load_dotenv()

from graph import build_graph


def main():
    app = build_graph()

    print("🎬 Welcome to MovieMate AI!")
    print("Ask for a movie recommendation.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye! 🎬")
            break

        if not user_query:
            print("Please type a movie request.\n")
            continue

        initial_state = {
            "user_query": user_query,
            "rag_context": "",
            "needs_web_search": False,
            "web_results": "",
            "web_search_used": "No, web search was not used.",
            "final_answer": ""
        }

        try:
            result = app.invoke(initial_state)

            print("\nMovieMate AI:")
            print(result["final_answer"])
            print("\n" + "-" * 50 + "\n")

        except Exception as error:
            print("\nOops, something went wrong:")
            print(error)
            print("\nCheck your API keys, .env file, and data folder, then try again.")
            print("-" * 50 + "\n")


if __name__ == "__main__":
    main()