# MovieMate AI 🎬

MovieMate AI is an agentic movie recommendation assistant created for our Artificial Intelligence course project.

**Team members:**
- Dilay Selim
- Eda Selmani

The system helps users choose movies based on mood, genre, group type, runtime, and preferences. It combines a curated local movie-guide corpus with live web search, so it can provide both stable recommendation logic and current rating/review evidence when needed.

## Project Goal

Choosing a movie for a group can be difficult because people may have different moods, genres, time limits, and content preferences. MovieMate AI solves this by using an agentic workflow:

1. It retrieves relevant information from a local movie-guide knowledge base using RAG.
2. It decides whether current web information is needed.
3. If needed, it calls a web-search tool.
4. It generates final movie recommendations using both retrieved context and web evidence.

## Technologies Used

- Python
- LangGraph
- LangChain
- GitHub Models
- FAISS vector store
- HuggingFace embeddings
- Tavily web search
- python-dotenv

## Features

MovieMate AI can:
- recommend movies by genre
- recommend movies by mood
- consider group type such as friends, family, or date night
- consider runtime preferences
- avoid unwanted categories such as scary, sad, violent, or dark movies
- retrieve relevant movie-guide documents using RAG
- decide when live web search is needed
- use Tavily web search for current ratings, reviews, and web evidence
- show retrieved documents and web-search status in the terminal

## Architecture

text
User Query
   
RAG Retrieval Node
   
Web Search Decision Node
If current information is needed → Tavily Web Search Tool
 If current information is not needed → Skip web search
   
Recommendation Generation Node
   
Final Movie Recommendations


## LangGraph Workflow

The project uses a LangGraph `StateGraph` with multiple nodes and conditional branching.

Main nodes:

1. retrieve_movie_guides
   - Retrieves relevant documents from the FAISS vector store.

2. decide_web_search
   - Checks the user query for current-information keywords such as:
     - current
     - recent
     - latest
     - rating
     - reviews
     - IMDb
     - Rotten Tomatoes
     - streaming
     - availability

3. web_search_movies
   - Calls Tavily web search when the agent decides current web information is needed.

4. generate_recommendations
   - Uses the LLM to generate the final answer from the user query, RAG context, and optional web results.

The graph includes a conditional edge after `decide_web_search`, so the agent can choose between:
- RAG-only recommendation generation
- RAG + web-search recommendation generation

## RAG Corpus

The RAG corpus contains 25 curated movie-guide documents stored in the `data/` folder.

Example files:
- `action_guide.md`
- `adventure_guide.md`
- `animation_guide.md`
- `comedy_guide.md`
- `coming_of_age_guide.md`
- `cozy_movies_guide.md`
- `crime_guide.md`
- `date_night_guide.md`
- `documentary_guide.md`
- `drama_guide.md`
- `family_friendly_guide.md`
- `fantasy_guide.md`
- `feel_good_movies_guide.md`
- `group_movie_night_guide.md`
- `horror_guide.md`
- `movie_ratings_guide.md`
- `movies_to_avoid_by_mood.md`
- `movies_under_2_hours.md`
- `movies_under_90_minutes.md`
- `musical_guide.md`
- `mystery_guide.md`
- `romance_guide.md`
- `scifi_guide.md`
- `superhero_guide.md`
- `thriller_guide.md`

The corpus is embedded using HuggingFace embeddings and stored in a FAISS vector store.

## Setup Instructions

### 1. Clone the repository

bash
git clone https://github.com/Dilay22/moviemate-ai.git
cd moviemate-ai


### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` file

Create a `.env` file based on `.env.example`:

```env
GITHUB_TOKEN=your_github_models_token_here
MODEL_NAME=openai/gpt-4o-mini
BASE_URL=https://models.github.ai/inference
TAVILY_API_KEY=your_tavily_api_key_here
HF_TOKEN=your_huggingface_token_here
```

Important: do not commit the real `.env` file to GitHub.

### 6. Ingest the movie corpus

```bash
python src/ingest.py
```

Expected output:

```text
 Loading movie guide documents...
 Loaded 25 documents.
 Creating embeddings...
 Saving FAISS vector store...
 Ingestion complete. Vector store saved in vectorstore/
```

### 7. Run the application

```bash
python src/main.py
```

## Example Queries

### Example 1: RAG-only query

```text
Recommend a cozy movie for a relaxing night, not scary, under 2 hours.
```

Expected behavior:
- The system retrieves relevant movie-guide documents.
- The agent decides web search is not needed.
- The final answer is generated using the local RAG corpus.

Example terminal evidence:

```text
Using RAG: retrieving movie guides...
📄 Retrieved documents:
- data/cozy_movies_guide.md
- data/horror_guide.md
- data/date_night_guide.md
- data/movies_to_avoid_by_mood.md
 Web search not needed. Using RAG only.
```

### Example 2: RAG + web search query

```text
Recommend a drama movie for 2 friends for a movie night. Check current ratings before choosing.
```

Expected behavior:
- The system retrieves relevant movie-guide documents.
- The agent detects that current ratings are requested.
- The agent calls Tavily web search.
- The final answer includes movie recommendations and web evidence.

Example terminal evidence:

```text
📚 Using RAG: retrieving movie guides...
📄 Retrieved documents:
- data/movie_ratings_guide.md
- data/group_movie_night_guide.md
- data/movies_to_avoid_by_mood.md
- data/comedy_guide.md
🌐 Web search needed based on user query.
🔎 Running web search...
🌐 Web search returned results:
```

##Video Demo:
https://drive.google.com/file/d/18LmxbY58lSMoEyDTZ0dmGqZN_l44waut/view?usp=share_link

## Academic Integrity

AI assistance was used during development and is documented in `AI_USAGE.md`. All group members reviewed the final code and should be able to explain the implementation.
