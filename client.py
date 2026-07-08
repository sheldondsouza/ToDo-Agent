import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types

load_dotenv()  

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


ALLOWED_KEYS = {"type", "description", "properties", "required", "items", "enum"}

def clean_schema(schema: dict) -> dict:
    if not isinstance(schema, dict):
        return schema
    cleaned = {}
    for key, value in schema.items():
        if key not in ALLOWED_KEYS:
            continue
        if key == "properties" and isinstance(value, dict):
            cleaned[key] = {k: clean_schema(v) for k, v in value.items()}
        elif key == "items":
            cleaned[key] = clean_schema(value)
        else:
            cleaned[key] = value
    return cleaned

async def mcp_tools_to_gemini_format(session):
    tools_result = await session.list_tools()
    function_declarations = []
    for tool in tools_result.tools:
        function_declarations.append(
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters=clean_schema(tool.inputSchema),
            )
        )
    return function_declarations

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            function_declarations = await mcp_tools_to_gemini_format(session)
            print("Connected. Available tools:", [f.name for f in function_declarations])

            tool = types.Tool(function_declarations=function_declarations)
            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(tools=[tool]),
            )

            print("\nType a message (or 'quit' to exit):")
            while True:
                user_input = input("You: ")
                if user_input.lower() == "quit":
                    break

                response = chat.send_message(user_input)

               
                max_steps = 8
                steps = 0
                while True:
                    steps += 1
                    if steps > max_steps:
                        print("Agent: (stopped -- too many steps)")
                        break

                    part = response.candidates[0].content.parts[0]

                    if part.function_call:
                        fn_name = part.function_call.name
                        fn_args = dict(part.function_call.args)
                        print(f"[Agent step: calling {fn_name}({fn_args})]")

                        result = await session.call_tool(fn_name, fn_args)
                        tool_output = result.content[0].text
                        print(f"[Observation: {tool_output}]")

                        response = chat.send_message(
                            types.Part.from_function_response(
                                name=fn_name,
                                response={"result": tool_output},
                            )
                        )
                    else:
                       
                        print("Agent:", part.text)
                        break

if __name__ == "__main__":
    asyncio.run(main())