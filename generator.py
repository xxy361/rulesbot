from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    
    fallback = (
        "I couldn't find anything relevant in the loaded rule books. "
        "Try rephrasing your question — or check that your ingestion pipeline is working."
    )

    if not retrieved_chunks:
        return fallback

    # Filter out weak matches
    relevant = [c for c in retrieved_chunks if c["distance"] <= 0.6]
    if not relevant:
        return fallback

    # Format each chunk as a labeled block, separated by a delimiter
    context = "\n---\n".join(
        f"[Source: {c['game']}]\n{c['text']}" for c in relevant
    )

    system_message = (
        "You are RulesBot, a board game rules assistant. Answer the user's "
        "question using ONLY the rule text provided. Do not use any prior "
        "knowledge about board games.\n\n"
        "Use the game name given in the source labels. If your answer draws "
        "on rules from a specific game, begin or end with a clear citation of "
        'that game (e.g. "According to the Catan rules: ..."). If multiple '
        "games' rules appear in the context, only cite the one(s) you "
        "actually used."
    )

    user_message = f"{query}\n\nContext:\n{context}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
