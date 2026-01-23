import os
import pandas as pd
from dotenv import load_dotenv

from src.indexer import AuraIndexer
from src.rag import AuraRAG

def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(" GEMINI_API_KEY is missing in .env")

    # Load processed CSV
    df = pd.read_csv("data/processed/ifixit_steps.csv")
    rows = df.to_dict(orient="records")

    # Build vector index
    retriever = AuraIndexer("all-MiniLM-L6-v2")
    retriever.build_index(rows)

    # Gemini model (stable + fast)
    aura = AuraRAG(api_key=api_key, model="models/gemini-2.0-flash")

    print("\nAURA is ready. Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break

        retrieved = retriever.search(query, top_k=6)

        if not retrieved:
            print("\nAURA: I couldn't find a relevant guide. Which exact device model is it?\n")
            continue

        answer = aura.answer(query, retrieved)
        print("\nAURA:\n" + answer + "\n")

if __name__ == "__main__":
    main()
