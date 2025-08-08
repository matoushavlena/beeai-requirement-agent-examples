"""Example 5: Multi-agent handoff with constraints

Use DestinationExpert agent before calling WeatherExpert agent.
This demonstrates controlled agent-to-agent handoffs.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


@tool
def destination_expert(location_query: str) -> str:
    """Expert agent for destination recommendations and information."""
    destinations = {
        "beach vacation": "Recommended: Maldives, Hawaii, Bali",
        "city break": "Recommended: Tokyo, Paris, New York",
        "adventure": "Recommended: Nepal, New Zealand, Patagonia",
    }
    for key in destinations:
        if key in location_query.lower():
            return destinations[key]
    return f"Destination info for: {location_query}"


@tool
def weather_expert(location: str) -> str:
    """Expert agent for weather information and forecasts."""
    weather_data = {
        "Maldives": "30°C, sunny with light breeze",
        "Tokyo": "18°C, partly cloudy",
        "Nepal": "12°C, clear mountain weather",
    }
    for location_key in weather_data:
        if location_key.lower() in location.lower():
            return weather_data[location_key]
    return f"Weather for {location}: varies by season"


async def main():
    # Create agent with handoff constraint: WeatherExpert only after DestinationExpert
    agent = RequirementAgent(
        llm=llm,
        tools=[destination_expert, weather_expert],
        requirements=[
            ConditionalRequirement(
                weather_expert,
                only_after=[destination_expert],  # Weather expert only after destination expert
            )
        ],
    )

    # The agent will use destination_expert before weather_expert
    response = await agent.run(
        "I want to plan a beach vacation. Can you help me with destinations and weather?"
    ).middleware(GlobalTrajectoryMiddleware(included=[Tool]))
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
