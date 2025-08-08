"""Example 8: Enforce final action before answer

Must send a summary report before returning the final answer.
This ensures proper documentation and closure.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.tools import Tool, tool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware

from examples.utils import llm


@tool
def send_email_summary(report_content: str) -> str:
    """Tool to send summary report via email."""
    return f"Summary report sent via email: {report_content[:50]}..."


async def main():
    # Create agent with final action constraint
    agent = RequirementAgent(
        llm=llm,
        tools=[send_email_summary],
        requirements=[
            ConditionalRequirement(send_email_summary, min_invocations=1, max_invocations=1),
            ConditionalRequirement(
                "final_answer",
                force_after=send_email_summary,  # Final answer only after summary is sent
            ),
        ],
    )

    # The agent must send a summary before providing the final answer
    response = await agent.run("Analyze our quarterly sales data and prepare a report.").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
