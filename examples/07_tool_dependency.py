"""Example 7: Require one tool to run before another

Must search for flights before booking them.
This demonstrates a natural workflow dependency."""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool

from examples.utils import llm


@tool
def search_flights(departure: str, destination: str) -> str:
    """Search for available flights between two cities."""
    flights = [
        f"Flight AA123: {departure} to {destination} at 9:00 AM - $299",
        f"Flight UA456: {departure} to {destination} at 2:00 PM - $340",
        f"Flight DL789: {departure} to {destination} at 6:00 PM - $275",
    ]
    import random

    return random.choice(flights)


@tool
def book_flight(flight_info: str) -> str:
    """Book a specific flight after searching for options."""
    return f"Successfully booked: {flight_info}. Confirmation number: ABC123. Check-in opens 24 hours before departure."


async def main():
    # Create agent with dependency constraint
    agent = RequirementAgent(
        llm=llm,
        tools=[search_flights, book_flight],
        requirements=[
            ConditionalRequirement(
                book_flight,
                only_after=[search_flights],  # Must search flights before booking
            )
        ],
    )

    # The agent will search flights before booking
    response = await agent.run("Book me a flight from New York to Los Angeles.").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
