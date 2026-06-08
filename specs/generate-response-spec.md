# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Each chunk is rendered as a labeled block: a header line naming the game, followed by the chunk text. Blocks are separated by a clear delimiter.
Example structure: [Source: Catan]\n<chunk text>\n---\n[Source: Ticket to Ride]\n<chunk text>.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are RulesBot, a board game rules assistant. Answer the user's question using ONLY the rule text provided. Do not use any prior knowledge about board games.
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
Use the game name given in the source labels. If your answer draws on rules from a specific game, begin or end with a clear citation of that game (e.g. "According to the Catan rules: ..."). If multiple games' rules appear in the context, only cite the one(s) you actually used.
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
I couldn't find anything in the loaded rule books that answers that question. Make sure the relevant game's rules have been
added, and try rephrasing your question with more specific terms.
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
Filter out chunks with distance above a threshold (~0.5, per the cosine guidance in the system design) before building context. If all chunks are filtered out, return the fallback message rather than feeding weak context to the model. The tradeoff is that filtering could drop a borderline-relevant chunk. However, a confident wrong answer is worse than no answer.
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
The system message contains the grounding and citation instructions. The user message contains the user's actual question and the formatted context following the user's question.
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: "How does the Spymaster give clues in Codenames?"
Response: "According to the Codenames rules: The Spymaster gives clues by saying a word followed by a number. The word hints at the meaning of one or more codenames the Spymaster wants their team to guess, and the number tells the team how many codenames are related to that clue."
Correctly grounded? [yes / no]: yes
Cited the right game? [yes / no]: yes
```

**One thing you changed from your original spec after seeing the actual output:**

```
I changed the distance filter from 0.5 to 0.6, because the question "How do you set up the board in Catan" doesn't generate a response. The queried chunk texts have distance 0.581 and 0.592, which was filtered out by the 0.5 filter.
```
