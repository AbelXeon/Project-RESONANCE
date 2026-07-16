from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """Runs a web search and returns a compact text summary of results,
    formatted so the model can read and cite it."""
    try:
        results = DDGS().text(query, max_results=max_results)
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return "No results found."

    lines = []
    for r in results:
        title = r.get("title", "")
        body = r.get("body", "")
        href = r.get("href", "")
        lines.append(f"- {title}: {body} ({href})")

    return "\n".join(lines)


# Tool schema Groq needs to know when/how to call this
WEB_SEARCH_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": (
            "Search the web for current information: news, prices, recent events, "
            "software versions, or anything that could have changed since training. "
            "Use whenever the user asks about something time-sensitive or you're unsure "
            "if your knowledge is current."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query.",
                }
            },
            "required": ["query"],
        },
    },
}