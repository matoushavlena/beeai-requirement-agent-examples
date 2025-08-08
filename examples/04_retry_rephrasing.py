"""Example 4: Retry search with rephrasing, up to 3 times

Rephrase the query and retry search if output is empty (max 3 attempts).
This implements intelligent retry logic with query rephrasing.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.agents.experimental.requirements.requirement import Requirement, Rule
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


@tool
def rephrase_tool(original_query: str) -> str:
    """Tool to rephrase search queries for better results."""
    rephrased_queries = {
        "python tutorial": "learn python programming basics",
        "weather today": "current weather conditions",
        "best restaurants": "top rated dining establishments",
    }
    return rephrased_queries.get(original_query, f"alternative phrasing for: {original_query}")


@tool
def duckduckgo_search_tool(query: str) -> str:
    """Tool to search using DuckDuckGo."""
    # Simulate occasional empty results for demonstration
    if query == "obscure topic":
        return ""  # Empty result to trigger rephrasing
    return f"Search results for '{query}': Found 10 relevant articles."


# Temporary fix for the bug in the framework
rephrase_tool.input_schema.model_config["extra"] = "forbid"
duckduckgo_search_tool.input_schema.model_config["extra"] = "forbid"


class RetryWithRephrasing(Requirement):
    """Custom requirement to retry search with rephrasing if results are empty."""

    def __init__(self, target_tool):
        super().__init__()
        self.target_tool = target_tool
        self.enabled = True

    async def run(self, state, **kwargs):
        """Check if last output is empty and force rephrasing if needed."""
        # Check if we have any steps and the last one returned empty results
        if state.steps:
            try:
                last_step = state.steps[-1].output.get_text_content()
                # Check if output is empty string (our trigger condition)
                if last_step == "":
                    return [Rule(target="rephrase_tool", forced=True)]
            except (AttributeError, IndexError):
                pass
        return []


async def main():
    # Create agent with retry logic
    agent = RequirementAgent(
        llm=llm,
        tools=[rephrase_tool, duckduckgo_search_tool],
        requirements=[
            RetryWithRephrasing(duckduckgo_search_tool),
            ConditionalRequirement(duckduckgo_search_tool, max_invocations=3),  # Max 3 search attempts
        ],
    )

    # The agent will search, get empty results, then rephrase and retry
    response = await agent.run("Use the search tool with query: obscure topic").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
