SYSTEM_PROMPT = """You are AURA, a repair assistant.
Rules:
1) Use ONLY the provided iFixit/MyFixit context.
2) If context is insufficient, say so and ask a clarifying question.
3) Give steps in a clear numbered format.
4) Include tools if mentioned in the context.
"""

def build_user_prompt(query, chunks):
    context = "\n\n".join(
        [
            f"[{i+1}] Device: {c.get('device')}\n"
            f"Guide: {c.get('title')}\n"
            f"Step {c.get('step_number')}:\n{c.get('text')}\n"
            f"Guide Tools: {c.get('tools')}\n"
            f"Step Tools: {c.get('step_tools')}\n"
            f"URL: {c.get('url')}\n"
            for i, c in enumerate(chunks)
        ]
    )

    return f"""User query:
{query}

Retrieved iFixit context:
{context}

Answer format:
- Summary (1-2 lines)
- Steps (numbered)
- Tools (if available)
- Source guide link(s)
- If missing info: ask 1 clarifying question
"""
