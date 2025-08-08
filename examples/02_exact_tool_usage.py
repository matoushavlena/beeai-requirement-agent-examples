"""Example 2: Require tool use exactly once at any time

Must use price_estimator once, anytime in the flow.
This ensures the tool is used exactly once - no more, no less.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


@tool
def price_estimator(item: str) -> str:
    """Tool to estimate pricing for a service or product."""
    return f"Estimated price for {item}: $49.99"


async def main():
    # Create agent with constraint: price estimator must be used exactly once
    agent = RequirementAgent(
        llm=llm,
        tools=[price_estimator],
        requirements=[
            ConditionalRequirement(
                price_estimator,
                min_invocations=1,  # Must use at least once
                max_invocations=1,  # Cannot use more than once
            )
        ],
    )

    # The agent must use price_estimator exactly once during the conversation
    response = await agent.run("I need to buy a laptop. Can you help me with pricing and recommendations?").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
