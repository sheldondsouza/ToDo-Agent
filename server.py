from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TodoServer")

todos = []

@mcp.tool()
def add_todo(task: str) -> str:
    """Add a new task to the to-do list"""
    todos.append(task)
    return f"Added: '{task}'. You now have {len(todos)} tasks."

@mcp.tool()
def list_todos() -> str:
    """List all current to-do tasks"""
    if not todos:
        return "Your to-do list is empty."
    return "\n".join(f"{i+1}. {t}" for i, t in enumerate(todos))

@mcp.tool()
def remove_todo(task_number: int) -> str:
    """Remove a task by its number in the list"""
    if 1 <= task_number <= len(todos):
        removed = todos.pop(task_number - 1)
        return f"Removed: '{removed}'"
    return "Invalid task number."

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather forecast for a city"""
    
    fake_forecasts = {
        "mysuru": "Rain expected, 80% chance, 24°C",
        "bengaluru": "Partly cloudy, 20% chance of rain, 27°C",
    }
    return fake_forecasts.get(city.lower(), f"No data for {city}, assume clear skies.")

if __name__ == "__main__":
    mcp.run()