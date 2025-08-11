"""Example 9: Ask user before using sensitive tools

Ask user before sending an email to their manager.
This implements human-in-the-loop for sensitive operations.
"""

import asyncio

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool, tool

from examples.utils import llm


@tool
def send_email_to_manager(subject: str, content: str) -> str:
    """Sensitive tool that sends emails to the user's manager."""
    return f"Email sent to manager - Subject: '{subject}' Content: '{content[:50]}...'"


@tool
def draft_report(topic: str) -> str:
    """Draft a report on the given topic. This is a safe, non-sensitive tool."""
    return "Q4 Sales Report: Revenue $3.2M (+15% YoY), 22K units sold, strong enterprise growth"


async def main():
    # Create agent with permission requirement for sensitive tool
    agent = RequirementAgent(
        llm=llm,
        tools=[send_email_to_manager, draft_report],
        requirements=[
            AskPermissionRequirement(
                send_email_to_manager,
                remember_choices=False,  # Ask permission every time
            )
        ],
    )

    response = await agent.run("Please draft a report on Q4 sales performance and send it to manager.").middleware(
        GlobalTrajectoryMiddleware(included=[Tool])
    )
    print(response.answer.text)


if __name__ == "__main__":
    asyncio.run(main())
