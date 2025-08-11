"""Example 5: Multi-agent handoff with constraints

Use HandoffTool to delegate to DestinationExpert before WeatherExpert.
This demonstrates controlled agent-to-agent handoffs.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool
from beeai_framework.tools.handoff import HandoffTool

from examples.utils import llm


# Create expert agents with simple instructions
@tool
def get_destination_info(location_query: str) -> str:
    """Get destination recommendations."""
    if "beach" in location_query.lower():
        return "Top beach destinations: Maldives, Bali, Hawaii"
    return "No destination recommendations available"


@tool
def get_weather_info(location: str) -> str:
    """Get current weather."""
    weather_data = {
        "Maldives": "32°C, sunny, light breeze",
        "Bali": "29°C, partly cloudy, warm",
        "Hawaii": "26°C, clear skies, calm",
    }
    for loc in weather_data:
        if loc.lower() in location.lower():
            return weather_data[loc]
    return f"Weather for {location}: pleasant conditions"


destination_expert = RequirementAgent(
    llm=llm,
    tools=[get_destination_info],
    instructions="You are a destination expert. Only provide destination recommendations. Keep responses brief and focused.",
)

weather_expert = RequirementAgent(
    llm=llm,
    tools=[get_weather_info],
    instructions="You are a weather expert. Only provide current weather information. Keep responses brief and focused.",
)


async def main():
    # Create agent with handoff tools
    handoff_destination = HandoffTool(
        target=destination_expert,
        name="transfer_to_destination_expert",
        description="Transfer to destination expert for travel recommendations",
    )

    handoff_weather = HandoffTool(
        target=weather_expert,
        name="transfer_to_weather_expert",
        description="Transfer to weather expert for climate information",
    )

    agent = RequirementAgent(
        llm=llm,
        tools=[handoff_destination, handoff_weather],
        requirements=[
            ConditionalRequirement(
                handoff_weather,
                only_after=[handoff_destination],  # Weather expert only after destination expert
            )
        ],
    )

    # The agent will handoff to DestinationExpert before WeatherExpert
    response = await agent.run(
        "I want to plan a beach vacation. Can you help me with destinations and weather?"
    ).middleware(GlobalTrajectoryMiddleware(included=[Tool]))
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
