from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def main():
    print("📚 Loading movie guide documents...")

    loader = DirectoryLoader(
        "data",
        glob="*.md",
        loader_cls=TextLoader
    )

    documents = loader.load()

    if not documents:
        raise ValueError("No documents found in data folder.")

    print(f"✅ Loaded {len(documents)} documents.")

    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder=".cache/huggingface"
    )

    print("💾 Saving FAISS vector store...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local("vectorstore")

    print("✅ Ingestion complete. Vector store saved in vectorstore/")


if __name__ == "__main__":
    main()