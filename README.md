```markdown
# Todo MCP Agent

A learning project demonstrating MCP (Model Context Protocol) combined with
an agentic reasoning loop, powered by Google Gemini.

## What this is
- `server.py` — an MCP server exposing tools: add_todo, list_todos, remove_todo, get_weather
- `client.py` — an MCP client + Gemini-powered agent that can call those tools,
  chaining multiple tool calls together to complete a task

## Prerequisites
- Python 3.10+
- A Gemini API key from https://aistudio.google.com/apikey

## Setup

1. Clone/download this project and open a terminal in the project folder.

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install mcp google-genai python-dotenv
   ```

4. Create a `.env` file in the project folder with your API key:
   ```
   GEMINI_API_KEY=your-key-here
   ```

5. Add `.env` and `venv/` to `.gitignore` if using git, so the key never gets committed.

## Running server.py separately (for testing/debugging only)

You can run the server on its own to confirm it works, without any AI model involved:

```bash
npx @modelcontextprotocol/inspector python server.py
```

This opens a browser-based Inspector UI where you can manually call each tool
(e.g. add_todo with task="buy milk") and see the raw responses. Useful for
confirming your server logic works before adding the agent on top.

Note: running `python server.py` directly (without the Inspector) will just
sit waiting for stdio input — it's designed to be launched BY a client, not
used standalone in a normal terminal.

## Running server.py and client.py together (the actual agent)

You do NOT need to manually start server.py first — client.py starts it
automatically as a subprocess when it runs.

Just run:
```bash
python client.py
```

You should see:
```
Connected. Available tools: ['add_todo', 'list_todos', 'remove_todo', 'get_weather']

Type a message (or 'quit' to exit):
You:
```

## Example prompts to try

```
add buy milk to my todo list
what's on my todo list
Add a task to water my plants, and if it's going to rain in Mysuru today, remind me to bring an umbrella instead
quit
```

Watch for lines like `[Agent step: calling ...]` and `[Observation: ...]` —
these show the agent reasoning through multiple tool calls in sequence.

## Notes
- Todos are stored in memory only — they reset every time you restart client.py.
- Free-tier Gemini API has rate limits (a few requests/minute). If you hit a
  429 error, wait ~40 seconds and try again.
- Rotate your API key immediately if it's ever pasted somewhere public
  (chat, GitHub, etc.) — treat any exposed key as compromised.
```
