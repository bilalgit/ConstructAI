import asyncio

from mcp import Client
from server import mcp


async def main():

    async with Client(mcp) as client:

        result = await client.list_tools()

        print("\nConstructAI MCP Tools:")
        print("----------------------")

        for tool in result.tools:
            print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())