"""Example 6: ReAct loop control

Alternate tools and reasoning, avoid consecutive thinking.
This implements the ReAct (Reasoning + Acting) pattern with constraints.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool
from beeai_framework.tools.think import ThinkTool

from examples.utils import llm


@tool
def wikipedia_tool(query: str) -> str:
    """Tool to search Wikipedia for information."""
    return f"Wikipedia search for '{query}': Found comprehensive article with background information."


@tool
def weather_tool(location: str) -> str:
    """Tool to get weather information."""
    return f"Weather data for {location}: Current conditions and forecast available."

 
async def main():
    # Create agent with ReAct constraints
    agent = RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), wikipedia_tool, weather_tool],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,  # Must start with thinking
                force_after=[Tool],  # Force thinking after any tool
                consecutive_allowed=False,  # Prevent consecutive thinking
            )
        ],
    )

    # The agent will follow ReAct pattern: Reason -> Act -> Reason -> Act...
    response = await agent.run("What's the weather like in Paris and what can you tell me about the city?").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
