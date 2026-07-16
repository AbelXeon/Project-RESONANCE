import json
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, VIVI_SYSTEM_PROMPT
from search_tool import web_search, WEB_SEARCH_TOOL_SCHEMA

client = Groq(api_key=GROQ_API_KEY)

# Very simple in-memory history per chat_id. Fine for a first bot;
# swap for a real DB later if you want it to survive restarts.
_history = {}

MAX_TURNS = 10  # how many past messages to keep per chat
MAX_TOOL_HOPS = 3  # safety cap on search -> search -> search loops


def get_history(chat_id: int):
    if chat_id not in _history:
        _history[chat_id] = []
    return _history[chat_id]


def ask_vivi(chat_id: int, user_text: str) -> str:
    history = get_history(chat_id)
    history.append({"role": "user", "content": user_text})

    messages = [{"role": "system", "content": VIVI_SYSTEM_PROMPT}] + history[-MAX_TURNS:]

    for _ in range(MAX_TOOL_HOPS):
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=[WEB_SEARCH_TOOL_SCHEMA],
            temperature=0.7,
            max_tokens=512,
        )
        choice = response.choices[0].message

        if choice.tool_calls:
            # Model wants to search before answering. Run the tool(s),
            # feed results back in, and let it try again.
            messages.append(choice)
            for call in choice.tool_calls:
                args = json.loads(call.function.arguments)
                result = web_search(args.get("query", ""))
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                })
            continue

        reply = choice.content
        history.append({"role": "assistant", "content": reply})
        return reply

    # Fallback if it somehow keeps looping
    return "Okay that search rabbit hole went nowhere — can you ask me that a different way?"