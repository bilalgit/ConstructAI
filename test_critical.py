import asyncio
import json

from mcp import Client
from server import mcp


async def main():

    async with Client(mcp) as client:

        result = await client.call_tool(
            "critical_activities",
            {
                "project_id": 3
            }
        )

        print("\n========== MCP RESULT ==========")

        print(result)

        print("\n========== STRUCTURED CONTENT ==========")

        if hasattr(result, "structured_content"):
            print(
                json.dumps(
                    result.structured_content,
                    indent=2,
                    default=str
                )
            )

        print("\n========== CONTENT ==========")

        if hasattr(result, "content"):
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)
                else:
                    print(item)

        print("\n========================================")


if __name__ == "__main__":
    asyncio.run(main())