import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_folder=".cache/huggingface"
    )


def build_retriever():
    embeddings = get_embeddings()

    if os.path.exists("vectorstore"):
        print("⚡ Loading saved FAISS vector store...")
        vectorstore = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("⚠️ No saved vector store found. Building from data folder...")

        loader = DirectoryLoader(
            "data",
            glob="*.md",
            loader_cls=TextLoader
        )

        documents = loader.load()

        if len(documents) == 0:
            raise ValueError(
                "No documents found in the data folder. "
                "Add your .md movie guide files first."
            )

        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local("vectorstore")
        print("✅ Vector store created and saved.")

    return vectorstore.as_retriever(search_kwargs={"k": 4})