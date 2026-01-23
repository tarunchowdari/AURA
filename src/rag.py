from google import genai
from src.prompts import SYSTEM_PROMPT, build_user_prompt

class AuraRAG:
    def __init__(self, api_key: str, model="models/gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def answer(self, query, retrieved_chunks):
        prompt = build_user_prompt(query, retrieved_chunks)
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

        resp = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )

        return resp.text
