"""Example 1: Require context before tool use

Ensure agent gets user location before querying weather.
This prevents the weather tool from being used without proper context.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool

from examples.utils import llm


@tool
def fetch_user_location() -> str:
    """Tool to fetch user's location."""
    return "User location: San Francisco, CA"


@tool
def weather_tool(location: str) -> str:
    """Tool to fetch weather data from OpenMeteo API."""
    return f"Weather for {location}: 22°C, partly cloudy"


async def main():
    # Create agent with constraint: weather tool can only be used after location is fetched
    agent = RequirementAgent(
        llm=llm,
        tools=[fetch_user_location, weather_tool],
        requirements=[ConditionalRequirement(weather_tool, only_after=[fetch_user_location])],
    )

    # The agent will automatically fetch location before checking weather
    response = await agent.run("What's the weather like?").middleware(GlobalTrajectoryMiddleware(included=[Tool]))
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
