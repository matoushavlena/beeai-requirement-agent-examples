"""Example 3: Start with analysis, only once

Analyze task before taking any action, and only once.
This forces the agent to think before acting and prevents repeated analysis.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


@tool
def analyze_task(task: str) -> str:
    """Tool to analyze the given task before taking action."""
    return f"Task analysis: {task} requires data gathering, processing, and reporting."


async def main():
    # Create agent with constraint: analysis must happen at step 1 and only once
    agent = RequirementAgent(
        llm=llm,
        tools=[analyze_task],
        requirements=[
            ConditionalRequirement(
                analyze_task,
                force_at_step=1,  # Must be the first tool used
                max_invocations=1,  # Can only be used once
            )
        ],
    )

    # The agent will automatically analyze the task first, and only once
    response = await agent.run("What analysis steps are needed for creating a marketing campaign?").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
