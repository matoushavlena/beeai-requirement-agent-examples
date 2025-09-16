"""Example 11: MCP Server Integration

Demonstrates how to integrate RequirementAgent with an MCP (Model Context Protocol) server,
allowing the agent to be exposed as a service with conditional tool usage constraints.
The weather tool can only be used after the user's location is fetched.
"""

from beeai_framework.adapters.mcp.serve.server import MCPServer, MCPServerConfig
from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools import tool

from examples.utils import llm


@tool
def fetch_user_location() -> str:
    """Tool to fetch user's location."""
    return "User location: San Francisco, CA"


@tool
def weather_tool(location: str) -> str:
    """Tool to fetch weather data from OpenMeteo API."""
    return f"Weather for {location}: 22°C, partly cloudy"


def main():
    # Create agent with constraint: weather tool can only be used after location is fetched
    agent = RequirementAgent(
        llm=llm,
        tools=[fetch_user_location, weather_tool],
        requirements=[ConditionalRequirement(weather_tool, only_after=[fetch_user_location])],
    )

    server = MCPServer(config=MCPServerConfig(transport="streamable-http"))
    server.register(agent)
    server.serve()


if __name__ == "__main__":
    main()
