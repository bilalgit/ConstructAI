import asyncio
import json
import time

import ollama

from mcp import Client
from server import mcp


MODEL = "qwen3:8b"


SYSTEM_PROMPT = """
You are ConstructAI, a Civil Engineering Project Control Assistant.

You have access to project-control tools through MCP.

IMPORTANT RULES:

1. MCP TOOL RESULTS ARE THE AUTHORITATIVE SOURCE.
   - Treat all data returned by an MCP tool as factual project data.
   - Never invent, estimate, guess, or modify project data.
   - Never change activity names, IDs, dates, durations, float values, progress values, or counts.

2. WHEN A TOOL RETURNS A LIST:
   - Preserve every relevant item from the tool result.
   - Do not omit items merely to make the answer shorter.
   - Do not add items that were not returned by the tool.
   - Preserve the order returned by the tool unless there is a clear reason to reorganize it.

3. COUNTS MUST MATCH THE TOOL RESULT.
   - If the tool says there are 18 critical activities, report 18.
   - Do not recalculate or reinterpret the count.

4. DATES AND NUMBERS:
   - Use exactly the dates and numbers returned by the MCP tool.
   - Do not calculate alternative dates unless the user explicitly asks for a calculation.
   - Do not describe an activity as critical unless the tool marks it as critical.

5. PROJECT-SPECIFIC QUESTIONS:
   - Always use the appropriate MCP tool when project data is required.
   - Do not answer from memory when the database/tool can provide the information.

6. TOOL RESULTS VS EXPLANATION:
   - The MCP tool provides the authoritative facts.
   - Your job is to explain those facts clearly to the user.
   - You may provide useful interpretation, but clearly distinguish interpretation from database facts.

7. IF THE USER ASKS FOR A COMPLETE LIST:
   - Provide the complete list.
   - Do not summarize it into only a few examples.

8. IF TOOL DATA IS MISSING:
   - Say that the required information is not available.
   - Do not fabricate an answer.

9. CONSTRUCTION CONTEXT:
   - Use practical civil/construction project-control terminology.
   - Explain technical information in simple language unless the user asks for technical detail.

10. ANSWER STYLE:

   - Be concise but complete.

   - Use tables or numbered lists when they make project information easier to understand.

   - Do not add irrelevant information.

11. NO UNSUPPORTED PROJECT FACTS:

   - Never introduce project facts that are not present in the current MCP tool result.

   - Do not invent dependencies, causes, delays, resources, quantities, dates, progress, or relationships.

   - If a dependency is needed, use the activity_dependencies tool.

   - If delay information is needed, use the delayed_activities or analyze_delay tool.

   - If risk information is needed, use the project_risk_analysis tool.

12. DO NOT INFER DATABASE RELATIONSHIPS:

   - Do not assume that one activity depends on another just because of construction sequence.

   - Do not state predecessor or successor relationships unless returned by an MCP tool.

   - Do not create causal relationships between activities without tool evidence.

13. DISTINGUISH FACT FROM INTERPRETATION:

   - Database/tool facts may be stated directly.

   - General construction knowledge may be used only as general explanation.

   - Never present general construction assumptions as facts about this project.

14. TOOL SELECTION:

   - Use one MCP tool when it fully answers the question.

   - Use additional MCP tools when the question requires information that is not available in the first tool result.

   - Never fill missing project information using assumptions.

15. STRICT MCP GROUNDING:

   - When answering a project-specific question, use ONLY facts explicitly present in the MCP tool results.

   - Do not add extra project-specific facts from general construction knowledge.

   - Do not mention dependencies, causes, resources, quantities, dates, delays, or relationships unless they are explicitly returned by an MCP tool.

   - If a factor is not present in the tool result, do not include it as a project-specific factor.

   - When explaining why an activity is high risk, use only the "Reasons", "Risk Score", "Critical", and "Total Float" fields returned by project_risk_analysis unless another MCP tool is explicitly called for additional information.

16. PROJECT IMPACT OUTPUT FORMAT:

   - When the MCP result contains "Project Impact", NEVER call it a "Project Impact Score".
   - "Project Impact" represents the number of days the project completion date is affected.
   - Always display it as:
     Project Impact: X days
   - If the MCP result contains "Priority", display it separately as:
     Priority: <value>
   - For example, if the tool returns:
     "Project Impact": 3,
     "Priority": "CRITICAL"
     the answer MUST say:
     Project Impact: 3 days
     Priority: CRITICAL
   - Never write "Project Impact Score".
   - Never describe the number 3 as "High priority".
   - Do not create any scoring system that is not explicitly provided by an MCP tool.
   """

def convert_mcp_tool_to_ollama(tool):
    """
    Convert an MCP tool definition into the format
    expected by Ollama.
    """

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.input_schema,
        },
    }

def serialize_tool_result(result):
    """
    Convert MCP tool results into clean Python data
    before sending them back to the local LLM.
    """

    # MCP structured content
    if hasattr(result, "structuredContent") and result.structuredContent:
        return result.structuredContent

    if hasattr(result, "structured_content") and result.structured_content:
        return result.structured_content

    # MCP text content
    content = getattr(result, "content", [])

    output = []

    for item in content:

        if hasattr(item, "text"):

            text = item.text

            # Try to convert JSON text into real Python data
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                output.append(text)

        else:
            output.append(str(item))

    return output


async def ask_constructai(question: str):

    async with Client(mcp) as mcp_client:

        # -------------------------------------------------
        # Get all MCP tools
        # -------------------------------------------------

        tools_result = await mcp_client.list_tools()

        ollama_tools = [
            convert_mcp_tool_to_ollama(tool)
            for tool in tools_result.tools
        ]

        print(
            f"\nLoaded {len(ollama_tools)} MCP tools."
        )

        # -------------------------------------------------
        # Initial conversation
        # -------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        # -------------------------------------------------
        # Tool-calling loop
        # -------------------------------------------------

        while True:
            start_time = time.time()
            response = await asyncio.to_thread(
                ollama.chat,
                model=MODEL,
                messages=messages,
                tools=ollama_tools,
                options={
        "temperature": 0,
    },

            )

            assistant_message = response["message"]

            # Add assistant response
            messages.append(assistant_message)

            # -------------------------------------------------
            # No tool call → final answer
            # -------------------------------------------------

            tool_calls = assistant_message.get("tool_calls")

            if not tool_calls:

                return assistant_message.get(
                    "content",
                    ""
                )

            # -------------------------------------------------
            # Execute requested MCP tools
            # -------------------------------------------------

            for tool_call in tool_calls:

                tool_name = tool_call["function"]["name"]

                arguments = tool_call["function"].get(
                    "arguments",
                    {}
                )

                print(
                    f"\n🔧 MCP Tool: {tool_name}"
                )

                print(
                    f"Arguments: {arguments}"
                )

                # Call MCP tool
                result = await mcp_client.call_tool(
                    tool_name,
                    arguments,
                )

                tool_output = serialize_tool_result(
                    result
                )
                print("\n========== RAW MCP RESULT ==========")
                print(json.dumps(tool_output, indent=2, default=str))
                print("====================================")
                print(
                    "✓ Tool executed"
                )

                # Send result back to LLM
                messages.append(
                    {
                        "role": "tool",
                        "content": json.dumps(
                            tool_output,
                            default=str,
                        ),
                    }
                )


async def main():

    print()

    print("=" * 60)

    print(
        "              CONSTRUCTAI"
    )

    print(
        "       AI PROJECT CONTROL ASSISTANT"
    )

    print("=" * 60)

    print(
        "\nLocal model: Qwen3 8B"
    )

    print(
        "API cost: ₹0"
    )

    while True:

        question = input(
            "\nConstructAI > "
        )

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "\nGoodbye!"
            )

            break

        try:

            answer = await ask_constructai(
                question
            )

            print()

            print(
                "ConstructAI:"
            )

            print(
                answer
            )

        except Exception:

            import traceback

            print()

            print(
                "ERROR:"
            )

            traceback.print_exc()


if __name__ == "__main__":

    asyncio.run(main())