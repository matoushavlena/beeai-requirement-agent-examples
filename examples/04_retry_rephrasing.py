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
        "New York City": "NYC",
    }
    return rephrased_queries.get(original_query, f"alternative phrasing for: {original_query}")


@tool
def wikipedia_search_tool(query: str) -> str:
    """Tool to search Wikipedia."""
    # Simulate page not found for NYC (common abbreviation)
    if query == "New York City":
        return ""  # Empty result to trigger rephrasing
    if query == "NYC":
        return f"Wikipedia page for '{query}': New York City is the most populous city in the United States..."
    return f"Wikipedia page for '{query}': Article found with general information."


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
        tools=[rephrase_tool, wikipedia_search_tool],
        requirements=[
            RetryWithRephrasing(wikipedia_search_tool),
            ConditionalRequirement(wikipedia_search_tool, max_invocations=3),  # Max 3 search attempts
        ],
    )

    # The agent will search, get empty results, then rephrase and retry
    response = await agent.run("Find information about New York City on Wikipedia.").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
