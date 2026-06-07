# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[your answer here]
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
{
    "text": "On your turn, you may either draw two cards or claim a route...",   # from documents[0][i]
    "game": "Ticket to Ride",                                                    # from metadatas[0][i]["game"]
    "distance": 0.41,                                                            # from distances[0][i]
}
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
query() is built to handle multiple queries at once, so it returns one inner list per query. results["documents"] is list[list[str]]. Since one query is sent,  results are at index [0]: results["documents"][0].
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
Using n_results is the easiest and always gives LLM something, but it might feed garbarge context, where distance score is high but still being top n-th. This can be avoided using max distance cutoff, but might return less than n or even empty results. 
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a) Return empty list []
(b) Poor match still returns 3 results, just with high distances
(c) Results naturally interleave games, as they are ranked purely by distance. The "game" field would ensure the generated response points to the right game.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: How do you set up the board in Catan?
Top result game: Catan
Distance score: 0.581
Does it make sense? yes
```

**One thing about the query results that surprised you:**

```
Trying the same query returns different results. Occassionly getting different games or a result like:
[Catan] (dist: 0.380) CATAN — OFFICIAL RULES SUMMARY
```
